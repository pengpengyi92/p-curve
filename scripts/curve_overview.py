"""Build an author-attributed current portal without changing frozen archives.

No network, data fetching or chart recalculation. The current portal may be
updated; timestamped archive JSON, HTML and SVG files remain immutable.
"""

from __future__ import annotations

import argparse
from html import escape
import importlib.util
import os
from pathlib import Path
import tempfile
from urllib.parse import quote, urlsplit


_SPEC = importlib.util.spec_from_file_location(
    "p_curve_overview_archive", Path(__file__).resolve().with_name("curve_archive.py")
)
archive = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(archive)

MARKER = '<meta name="p-curve-overview-generator" content="1">'
EDITORIAL = "What a beautiful curve."
EDITORIAL_LIMIT = "Shapes worth studying, not signals to trade."


def _e(value: object) -> str:
    return escape(str(value), quote=True)


def _author(value: object) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 100:
        raise ValueError("author must be nonempty text of at most100 characters")
    if any(ord(c) < 32 for c in value):
        raise ValueError("author must not contain control characters")
    return value.strip()


def render_overview(snapshot: dict, author: str = "pengyi", public: bool = False) -> str:
    """Return a standalone current-view HTML document using relative archive assets."""
    archive.validate_snapshot(snapshot, public=public)
    author = _author(author)
    snapshot_id = quote(snapshot["snapshot_id"], safe="")
    total = sum(n["yield_pct"] is not None for m in snapshot["markets"] for n in m["nodes"])
    mode = "Selected public overview" if public else "Private / local research overview"
    warning = (
        "Only source-rights-reviewed curves are included. Code licensing does not relicense source data."
        if public else
        "Not approved for public redistribution. Source-specific HOLD restrictions remain in force."
    )
    style = """
:root{color-scheme:light;--ink:#142c40;--muted:#506779;--blue:#176b9e;--line:#d7e5ee}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font:16px/1.6 system-ui,-apple-system,Segoe UI,sans-serif;color:var(--ink);background:#f3f8fc}
main{max-width:1600px;margin:0 auto;padding:36px 24px 52px}.hero{padding:32px;background:linear-gradient(125deg,#fff,#e8f4fc);border:1px solid var(--line);border-radius:20px}
.eyebrow{margin:0;color:var(--blue);font-size:13px;font-weight:700;letter-spacing:.09em;text-transform:uppercase}h1{font-size:clamp(27px,3.4vw,43px);line-height:1.18;max-width:1050px;margin:16px 0}h2{font-size:25px;margin:32px 0 16px}h3{font-size:19px;line-height:1.4;margin:0 0 10px}
.author{font-size:18px;margin:12px 0 0}.quiet{color:var(--muted);font-size:14px}.author-note{margin-top:2px}.editorial{font-size:22px;margin:20px 0 0}.editorial small{display:block;font-size:14px;color:var(--muted)}
.stats,.actions,.jump{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:20px}.stat,.jump a{background:#fff;border:1px solid var(--line);padding:7px 12px;border-radius:9px;font-size:13px}.actions a{border:1px solid var(--blue);padding:10px 15px;border-radius:9px;text-decoration:none;font-weight:650}.actions a:first-child{color:#fff;background:var(--blue)}
a{color:var(--blue);overflow-wrap:anywhere}a:focus-visible{outline:3px solid #c36b0a;outline-offset:4px}.notice{border-left:4px solid #c78b37;background:#fff7e9;padding:14px 18px;margin:20px 0;font-size:14px}.grid{display:grid;grid-template-columns:1fr;gap:22px}.card{min-width:0;background:#fff;border:1px solid var(--line);border-radius:15px;overflow:hidden;scroll-margin-top:20px}.card-head,.card-foot{padding:20px 22px}.card-head{padding-bottom:8px}.card p{margin:7px 0}.card img{display:block;width:100%;height:auto}.facts{font-size:13px;color:var(--muted);overflow-wrap:anywhere}.links{display:flex;flex-wrap:wrap;gap:14px;font-size:13px}.comment{font-size:16px;color:#28516d}.comment-label{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}details{font-size:13px;color:var(--muted);margin-top:12px}summary{cursor:pointer}li{margin:7px 0}code{overflow-wrap:anywhere}.table-scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:13px;margin-top:10px}th,td{border-bottom:1px solid var(--line);padding:7px 10px;text-align:left;white-space:nowrap}th{color:var(--ink);background:#f4f9fc}td:nth-child(n+2),th:nth-child(n+2){text-align:right}footer{padding:28px 2px 0;border-top:1px solid var(--line);margin-top:32px;font-size:13px;color:var(--muted)}
@media(min-width:1400px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:850px){main{padding:18px 12px}.hero{padding:23px 20px}.card-head,.card-foot{padding:17px}.editorial{font-size:20px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""
    bits = [
        '<!doctype html><html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">', MARKER,
        f'<meta name="author" content="{_e(author)}">',
        f'<title>P-Curve overview — {_e(snapshot["title"])}</title>',
        f'<style>{style}</style></head><body><main>',
        f'<header class="hero"><p class="eyebrow">P-Curve · {_e(mode)}</p>',
        f'<h1>{_e(snapshot["title"])}</h1>',
        f'<p class="author">Author: <strong>{_e(author)}</strong></p>',
        f'<p class="quiet author-note">Curated &amp; visualized by {_e(author)}. Underlying data remains credited to its original publishers.</p>',
        f'<p class="editorial">{_e(EDITORIAL)}<small>{_e(EDITORIAL_LIMIT)} Editorial appreciation, not investment analysis.</small></p>',
        '<div class="stats">',
        f'<span class="stat">{len(snapshot["markets"])} curves</span>',
        f'<span class="stat">{total} published source nodes</span>',
        f'<span class="stat">Collected: {_e(snapshot["generated_at"])}</span>',
        '</div><nav class="actions" aria-label="Overview actions">',
        '<a href="#curves">Explore curves below</a>',
        f'<a href="{snapshot_id}/index.html">Original archived overview</a>',
        f'<a href="{snapshot_id}/snapshot.json">Source nodes &amp; metadata</a></nav></header>',
        f'<p class="notice">{_e(warning)} Market dates and curve definitions differ; collection time is not a synchronized live close. No missing tenor is invented or filled with zero.</p>',
        '<nav class="jump" aria-label="Jump to a curve">',
    ]
    for market in snapshot["markets"]:
        bits.append(f'<a href="#curve-{market["id"]}">{_e(market["id"].replace("_", " ").upper())}</a>')
    bits += ['</nav><h2 id="curves">The curves</h2><div class="grid">']
    comments = (
        "A shape worth slowing down to look at.",
        "Every tenor adds another detail to the picture.",
        "Beautiful lines; explicit dates and definitions.",
    )
    for index, market in enumerate(snapshot["markets"]):
        count = sum(n["yield_pct"] is not None for n in market["nodes"])
        domain = urlsplit(market["source_url"]).netloc
        market_id = market["id"]
        bits += [
            f'<section class="card" id="curve-{market_id}" aria-labelledby="heading-{market_id}">',
            f'<div class="card-head"><h3 id="heading-{market_id}">{_e(market["title"])}</h3>',
            f'<p class="facts">Market date: <strong>{_e(market["market_date"] or "UNAVAILABLE")}</strong> · {_e(market["currency"])} · {count} source nodes</p>',
            f'<p class="facts">{_e(market["curve_type"])} · Yield units: percent per annum</p>',
            f'<p class="facts">As-of: {_e(market["asof"])}</p></div>',
            f'<img src="{snapshot_id}/{market_id}.svg" alt="{_e(market["title"])} — market date {_e(market["market_date"] or "UNAVAILABLE")}" loading="lazy" width="1100" height="680">',
            '<div class="card-foot"><p class="comment-label">Editorial appreciation</p>',
            f'<p class="comment">{_e(comments[index % len(comments)])}</p>',
            '<div class="links">',
            f'<a href="{_e(market["source_url"])}" target="_blank" rel="noopener noreferrer">Source: {_e(domain)}</a>',
            f'<a href="{_e(market["rights"]["source_url"])}" target="_blank" rel="noopener noreferrer">Data-rights evidence</a>',
            f'<a href="{snapshot_id}/{market_id}.svg">Open chart</a></div>',
            f'<p class="facts">Retrieved: {_e(market["retrieved_at"])} · {_e(market["rights"]["status"])}</p>',
            f'<details><summary>Full native node table ({count} actual / {len(market["nodes"])} supplied positions)</summary><div class="table-scroll"><table>',
            '<thead><tr><th scope="col">Tenor</th><th scope="col">Years</th><th scope="col">Yield (% p.a.)</th></tr></thead><tbody>',
        ]
        for node in market["nodes"]:
            value = "UNAVAILABLE" if node["yield_pct"] is None else str(node["yield_pct"])
            bits.append(f'<tr><td>{_e(node["tenor"])}</td><td>{_e(node["years"])}</td><td>{_e(value)}</td></tr>')
        if not market["nodes"]:
            bits.append('<tr><td colspan="3">UNAVAILABLE — no verified source nodes</td></tr>')
        bits += [
            '</tbody></table></div></details>',
            '<details><summary>Source notes and limitations</summary>',
            f'<p>{_e(market["rights"]["reason"])}</p><ul>',
        ]
        bits.extend(f'<li>{_e(note)}</li>' for note in market.get("notes", []))
        bits.append('</ul></details></div></section>')
    bits += ['</div><footer>',
             f'<p>Curated &amp; visualized by {_e(author)}. Snapshot <code>{_e(snapshot["snapshot_id"])}</code>, collected {_e(snapshot["generated_at"])}.</p>',
             '<p>This current-view page may be updated. The linked timestamped archive and original source records are unchanged. Par, YTM and continuous-zero rates are not interchangeable; visual connecting lines are not additional quotes.</p>',
             '<p>Aesthetic comments express appreciation only. No forecast, causal claim, live execution, investment advice or institutional endorsement is implied.</p>',
             '</footer></main></body></html>']
    return "\n".join(bits) + "\n"


def write_overview(snapshot_path: Path, output: Path, author: str = "pengyi", public: bool = False) -> Path:
    """Update only archive_root/index.html; all timestamped files remain read-only."""
    snapshot_path = Path(snapshot_path).resolve(strict=True)
    snapshot = archive.load_snapshot(snapshot_path)
    archive.validate_snapshot(snapshot, public=public)
    if snapshot_path.name != "snapshot.json" or snapshot_path.parent.name != snapshot["snapshot_id"]:
        raise ValueError("input must be a timestamped archive's snapshot.json")
    root = snapshot_path.parent.parent
    output = Path(output).absolute()
    if output.name != "index.html" or output.parent.resolve() != root or output.is_symlink():
        raise ValueError("output must be the non-symlink archive-root index.html, never an immutable snapshot file")
    required = [snapshot_path.parent / "index.html", *[
        snapshot_path.parent / f'{m["id"]}.svg' for m in snapshot["markets"]
    ]]
    if any(not p.is_file() or p.is_symlink() for p in required):
        raise ValueError("complete, non-symlink frozen HTML/SVG assets are required")
    if output.exists() and (not output.is_file() or MARKER not in output.read_text(encoding="utf-8")):
        raise FileExistsError("refusing to replace a file not marked as this generator's current portal")
    content = render_overview(snapshot, author=author, public=public)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                         prefix=".overview-", suffix=".tmp", dir=root,
                                         delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        os.replace(temporary, output)
        temporary = None
    finally:
        if temporary is not None and temporary.parent.resolve() == root:
            temporary.unlink(missing_ok=True)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--author", default="pengyi")
    parser.add_argument("--public", action="store_true")
    args = parser.parse_args()
    try:
        path = write_overview(args.snapshot, args.output, author=args.author, public=args.public)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Overview refused: {exc}\n")
    print(f"Updated current overview: {path}")


if __name__ == "__main__":
    main()
