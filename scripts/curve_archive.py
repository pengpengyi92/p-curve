"""Offline, no-overwrite sovereign-curve snapshot renderer (standard library only).

Input is an explicitly sourced JSON snapshot, not a live-price request. No source
is fetched and no missing annual tenors are invented. Permission decisions are
provided by the snapshot producer and must be reviewed independently.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime
from html import escape
import json
import math
import os
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import urlsplit


def _text(value: object, field: str, limit: int = 2000) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"{field} must be nonempty text (max {limit})")
    if any(ord(c) < 32 and c not in "\n\t" for c in value):
        raise ValueError(f"{field} contains control characters")
    return value


def _timestamp(value: object, field: str) -> datetime:
    raw = _text(value, field, 80)
    # Python3.10's fromisoformat accepts 3/6 fractional digits, whereas newer
    # versions accept (and truncate) longer fractions such as PowerShell's7.
    # Normalize only this temporary comparison value to datetime's microsecond
    # precision. The original metadata string is never rewritten.
    normalized = re.sub(
        r"(\d{2}:\d{2}:\d{2})\.(\d+)(?=Z$|[+-]\d{2}:\d{2}$)",
        lambda match: match.group(1) + "." + (match.group(2) + "000000")[:6],
        raw,
    )
    try:
        result = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO8601") from exc
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError(f"{field} must include a UTC offset")
    return result


def _url(value: object, field: str) -> str:
    value = _text(value, field, 4000)
    if any(c.isspace() for c in value):
        raise ValueError(f"{field} must not contain whitespace")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError(f"{field} must be an HTTPS URL without embedded credentials")
    return value


def _number(value: object, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise ValueError(f"{field} must be a finite JSON number")
    try:
        number = float(value)
    except OverflowError as exc:
        raise ValueError(f"{field} outside float range") from exc
    if not math.isfinite(number):
        raise ValueError(f"{field} must be finite")
    return number


def _keys(value: object, allowed: set[str], required: set[str], field: str) -> None:
    if not isinstance(value, dict) or not required.issubset(value):
        raise ValueError(f"{field} lacks required keys")
    if set(value) - allowed:
        raise ValueError(f"{field} has unreviewed keys: {sorted(set(value) - allowed)}")


def _safe_id(value: object, field: str, lower: bool = False) -> str:
    value = _text(value, field, 64)
    pattern = r"[a-z][a-z0-9_-]{0,39}" if lower else r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}"
    reserved = {"con", "prn", "aux", "nul", *[f"com{i}" for i in range(1, 10)],
                *[f"lpt{i}" for i in range(1, 10)]}
    if not re.fullmatch(pattern, value) or value.lower() in reserved:
        raise ValueError(f"{field} must be a safe portable identifier")
    return value


def validate_snapshot(snapshot: object, public: bool = False) -> dict:
    top = {"schema_version", "snapshot_id", "title", "generated_at", "markets", "notes"}
    _keys(snapshot, top, top - {"notes"}, "snapshot")
    if snapshot["schema_version"] != "1.0.0":
        raise ValueError("unsupported snapshot schema")
    _safe_id(snapshot["snapshot_id"], "snapshot_id")
    _text(snapshot["title"], "title", 300)
    generated = _timestamp(snapshot["generated_at"], "generated_at")
    if not isinstance(snapshot["markets"], list) or not snapshot["markets"]:
        raise ValueError("snapshot must contain at least one market")
    seen = set()
    for market in snapshot["markets"]:
        required = {"id", "title", "currency", "market_date", "asof", "retrieved_at",
                    "source_url", "curve_type", "units", "status", "rights", "nodes"}
        _keys(market, required | {"notes"}, required, "market")
        market_id = _safe_id(market["id"], "market.id", lower=True)
        if market_id in seen:
            raise ValueError("duplicate market identifier")
        seen.add(market_id)
        _text(market["title"], "market.title", 300)
        if not re.fullmatch(r"[A-Z]{3}", _text(market["currency"], "currency", 3)):
            raise ValueError("currency must be a three-letter uppercase code")
        _text(market["asof"], "asof", 500)
        _text(market["curve_type"], "curve_type", 500)
        if market["units"] != "percent_per_annum":
            raise ValueError("only explicit percent_per_annum input is supported")
        _url(market["source_url"], "source_url")
        retrieved = _timestamp(market["retrieved_at"], "retrieved_at")
        if retrieved > generated:
            raise ValueError("retrieved_at cannot follow generated_at")
        market_date = market["market_date"]
        if market_date is not None:
            if not isinstance(market_date, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", market_date):
                raise ValueError("market_date must be YYYY-MM-DD or null")
            try:
                parsed_date = date.fromisoformat(market_date)
            except (ValueError, TypeError) as exc:
                raise ValueError("market_date must be YYYY-MM-DD or null") from exc
            if parsed_date > retrieved.date():
                raise ValueError("market_date cannot be after local retrieval date")
        if market["status"] not in {"AVAILABLE", "UNAVAILABLE"}:
            raise ValueError("market status must be AVAILABLE or UNAVAILABLE")
        rights = market["rights"]
        _keys(rights, {"status", "source_url", "reason"}, {"status", "source_url", "reason"}, "rights")
        if rights["status"] not in {"APPROVED_PUBLIC_DISPLAY", "HOLD"}:
            raise ValueError("unrecognized rights status")
        _url(rights["source_url"], "rights.source_url")
        _text(rights["reason"], "rights.reason", 4000)
        if public and rights["status"] != "APPROVED_PUBLIC_DISPLAY":
            raise ValueError(f"public archive blocked by rights HOLD: {market_id}")
        nodes = market["nodes"]
        if not isinstance(nodes, list):
            raise ValueError("nodes must be a list")
        previous, tenors, finite_count = 0.0, set(), 0
        for node in nodes:
            _keys(node, {"tenor", "years", "yield_pct"}, {"tenor", "years", "yield_pct"}, "node")
            tenor = _text(node["tenor"], "tenor", 40)
            years = _number(node["years"], "years")
            if tenor in tenors or years <= previous or years > 100:
                raise ValueError("tenors must be unique and years strictly increasing within (0,100]")
            tenors.add(tenor)
            previous = years
            if node["yield_pct"] is not None:
                value = _number(node["yield_pct"], "yield_pct")
                if not -100 <= value <= 100:
                    raise ValueError("yield_pct outside supported [-100,100] range")
                finite_count += 1
        if market["status"] == "AVAILABLE" and (not finite_count or market_date is None):
            raise ValueError("AVAILABLE requires dated actual values")
        if market["status"] == "UNAVAILABLE" and finite_count:
            raise ValueError("UNAVAILABLE cannot contain apparently valid yields")
        if not isinstance(market.get("notes", []), list):
            raise ValueError("market notes must be a list")
        for note in market.get("notes", []):
            _text(note, "market note", 4000)
    if not isinstance(snapshot.get("notes", []), list):
        raise ValueError("notes must be a list")
    for note in snapshot.get("notes", []):
        _text(note, "snapshot note", 4000)
    return snapshot


def _e(value: object) -> str:
    return escape(str(value), quote=True)


def render_svg(snapshot: dict, market: dict, public: bool = False) -> str:
    width, height, left, right, top, bottom = 1100, 680, 85, 35, 145, 155
    w, h = width - left - right, height - top - bottom
    numeric = [n for n in market["nodes"] if n["yield_pct"] is not None]
    xmax = max((n["years"] for n in market["nodes"]), default=30)
    vals = [n["yield_pct"] for n in numeric]
    lo, hi = (min(vals), max(vals)) if vals else (0.0, 1.0)
    pad = max((hi - lo) * .12, .15)
    lo, hi = lo - pad, hi + pad
    x = lambda t: left + float(t) / xmax * w
    y = lambda v: top + (hi - float(v)) / (hi - lo) * h
    mode = "PUBLIC DISPLAY — producer-reviewed source rights" if public else "LOCAL RESEARCH — NOT APPROVED FOR PUBLIC REDISTRIBUTION"
    bits = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">',
            f'<title id="title">{_e(market["title"])}</title>',
            f'<desc id="description">{_e(snapshot["title"])}. Market date {_e(market["market_date"])}. Generated {_e(snapshot["generated_at"])}. Source nodes only; no missing yields filled.</desc>',
            '<rect width="1100" height="680" fill="#f8fafc"/>',
            '<g font-family="Arial,sans-serif" fill="#172033">',
            f'<text x="{left}" y="35" font-size="23" font-weight="bold">{_e(market["title"][:100])}</text>',
            f'<text x="{left}" y="60" font-size="13">Market date: {_e(market["market_date"] or "UNAVAILABLE")} | Generated: {_e(snapshot["generated_at"])}</text>',
            f'<text x="{left}" y="83" font-size="13">{_e(market["currency"])} | {_e(market["curve_type"][:130])}</text>',
            f'<text x="{left}" y="107" font-size="12" fill="#934500">{_e(mode)}</text>']
    for i in range(6):
        value = lo + (hi - lo) * i / 5
        yp = y(value)
        bits += [f'<line x1="{left}" y1="{yp:.3f}" x2="{width-right}" y2="{yp:.3f}" stroke="#d6dee9"/>',
                 f'<text x="{left-12}" y="{yp+4:.3f}" text-anchor="end" font-size="12">{value:.3f}</text>']
    ticks = [0, 1, 2, 3, 5, 7, 10, 15, 20, 25, 30, 40, 50, 75, 100]
    for tick in ticks:
        if tick > xmax:
            continue
        xp = x(tick)
        bits += [f'<line x1="{xp:.3f}" y1="{top}" x2="{xp:.3f}" y2="{height-bottom}" stroke="#e3e8ef"/>',
                 f'<text x="{xp:.3f}" y="{height-bottom+22}" text-anchor="middle" font-size="12">{tick}</text>']
    path, connected = [], False
    for node in market["nodes"]:
        if node["yield_pct"] is None:
            connected = False
            continue
        path.append(f'{"L" if connected else "M"}{x(node["years"]):.3f},{y(node["yield_pct"]):.3f}')
        connected = True
    if path:
        bits.append(f'<path d="{" ".join(path)}" fill="none" stroke="#176b9e" stroke-width="2.5"/>')
    for node in numeric:
        bits.append(f'<circle cx="{x(node["years"]):.3f}" cy="{y(node["yield_pct"]):.3f}" r="3" fill="#176b9e"><title>{_e(node["tenor"])}: {_e(node["yield_pct"])}%</title></circle>')
    if not numeric:
        bits.append(f'<text x="{left+w/2}" y="{top+h/2}" text-anchor="middle" font-size="23" fill="#934500">UNAVAILABLE — no verified yield nodes</text>')
    footer = ["Maturity (caller-supplied years); source yields in percent per annum",
              f'Retrieved: {market["retrieved_at"]} | As-of: {market["asof"]}',
              "All supplied source nodes plotted. Lines are visual guides, not additional quotes or calibrated interpolation.",
              "Not a live executable quote, trading recommendation, zero-curve conversion or PIT backtest.",
              f'Rights: {market["rights"]["status"]} — {market["rights"]["reason"]}']
    for i, text in enumerate(footer):
        bits.append(f'<text x="{left}" y="{height-bottom+48+i*18}" font-size="11">{_e(text[:165])}</text>')
    bits.append(f'<a href="{_e(market["source_url"])}" target="_blank" rel="noopener noreferrer"><text x="{left}" y="{height-12}" font-size="10" fill="#176b9e">Source: {_e(market["source_url"][:165])}</text></a>')
    bits += ['</g>', '</svg>']
    return "\n".join(bits)


def render_html(snapshot: dict, public: bool = False) -> str:
    mode = "PUBLIC DISPLAY" if public else "LOCAL RESEARCH — NOT APPROVED FOR PUBLIC REDISTRIBUTION"
    pieces = ['<!doctype html><html lang="en"><head><meta charset="utf-8">',
              '<meta name="viewport" content="width=device-width,initial-scale=1">',
              f'<title>{_e(snapshot["title"])}</title>',
              '<style>body{font:16px system-ui,sans-serif;margin:2rem auto;max-width:1200px;padding:0 1rem;background:#f1f5f9;color:#172033}section{background:white;padding:1rem;margin:1.5rem 0;border-radius:12px}img{width:100%;height:auto}table{border-collapse:collapse;width:100%;font-size:14px}td,th{border-bottom:1px solid #d6dee9;padding:.4rem;text-align:left}.warn{background:#fff0d1;padding:1rem}a{color:#176b9e}code{overflow-wrap:anywhere}details{margin-top:1rem}</style></head><body>',
              f'<h1>{_e(snapshot["title"])}</h1><p>Generated: <code>{_e(snapshot["generated_at"])}</code> · Snapshot: <code>{_e(snapshot["snapshot_id"])}</code></p>',
              f'<p class="warn">{_e(mode)}. Market dates and curve definitions differ. No missing tenor is filled or treated as zero. Source data is not a live executable quote.</p>',
              '<p><a href="snapshot.json">Immutable input metadata and source nodes (JSON)</a></p>']
    for note in snapshot.get("notes", []):
        pieces.append(f'<p>{_e(note)}</p>')
    for market in snapshot["markets"]:
        pieces += [f'<section id="{market["id"]}"><h2>{_e(market["title"])}</h2>',
                   f'<p>Market date: <strong>{_e(market["market_date"] or "UNAVAILABLE")}</strong> · {_e(market["currency"])} · {_e(market["curve_type"])}</p>',
                   f'<p>Retrieved: {_e(market["retrieved_at"])} · As-of: {_e(market["asof"])}</p>',
                   f'<p><a href="{_e(market["source_url"])}" rel="noopener noreferrer">Primary source</a> · <a href="{_e(market["rights"]["source_url"])}" rel="noopener noreferrer">Rights evidence</a> · {_e(market["rights"]["status"])}</p>',
                   f'<p>{_e(market["rights"]["reason"])}</p>',
                   f'<img src="{market["id"]}.svg" alt="{_e(market["title"])} — market date {_e(market["market_date"] or "UNAVAILABLE")}">',
                   '<details><summary>Every supplied source node (no invented annual tenors)</summary><table><thead><tr><th>Tenor</th><th>Years</th><th>Yield (%)</th></tr></thead><tbody>']
        for node in market["nodes"]:
            value = "UNAVAILABLE" if node["yield_pct"] is None else format(node["yield_pct"], ".10g")
            pieces.append(f'<tr><td>{_e(node["tenor"])}</td><td>{_e(node["years"])}</td><td>{_e(value)}</td></tr>')
        if not market["nodes"]:
            pieces.append('<tr><td colspan="3">UNAVAILABLE — no verified source nodes</td></tr>')
        pieces.append('</tbody></table></details>')
        for note in market.get("notes", []):
            pieces.append(f'<p>{_e(note)}</p>')
        pieces.append('</section>')
    return "\n".join(pieces) + "\n</body></html>\n"


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_snapshot(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)


def write_archive(snapshot: dict, output_root: Path, public: bool = False) -> Path:
    validate_snapshot(snapshot, public=public)
    root = Path(output_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    destination = root / snapshot["snapshot_id"]
    lock = root / ("." + snapshot["snapshot_id"] + ".lock")
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(descriptor)
    stage = None
    try:
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(f"immutable archive already exists: {destination.name}")
        stage = Path(tempfile.mkdtemp(prefix=".curve-stage-", dir=root))
        (stage / "snapshot.json").write_text(json.dumps(snapshot, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
        (stage / "index.html").write_text(render_html(snapshot, public), encoding="utf-8")
        for market in snapshot["markets"]:
            (stage / f'{market["id"]}.svg').write_text(render_svg(snapshot, market, public), encoding="utf-8")
        # Same-tool publishers serialize through an exclusive sibling lock.
        # No existing destination is knowingly replaced; snapshots are immutable.
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(f"immutable archive appeared during generation: {destination.name}")
        stage.rename(destination)
        stage = None
        return destination
    finally:
        if stage is not None and stage.resolve().parent == root and stage.name.startswith(".curve-stage-"):
            shutil.rmtree(stage)
        lock.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--public", action="store_true", help="require APPROVED_PUBLIC_DISPLAY for every market")
    args = parser.parse_args()
    try:
        result = write_archive(load_snapshot(args.input), args.output_root, public=args.public)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.exit(1, f"Curve archive refused: {exc}\n")
    print(f"Created immutable snapshot: {result}")


if __name__ == "__main__":
    main()
