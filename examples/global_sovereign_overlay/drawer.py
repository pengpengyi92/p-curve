"""Draw normalized source nodes. Does not read configs or retrieve data."""

from html import escape
from math import ceil, floor
from pathlib import Path

# Distinct hues and dash patterns remain identifiable where curves cross.
STYLES = (
    ("#23538c", ""),
    ("#a23f32", "9 4"),
    ("#71419a", "3 3"),
    ("#176f73", "12 4 3 4"),
    ("#a06013", "5 4"),
    ("#23744e", "14 4"),
)


class Drawer:
    def render(self, snapshot: dict, *, public: bool = True) -> str:
        markets = snapshot["markets"]
        if public and any(m["rights"]["status"] == "HOLD" and m["nodes"] for m in markets):
            raise ValueError("public rendering cannot include HOLD nodes")
        nodes = [n for m in markets for n in m["nodes"] if n["yield_pct"] is not None]
        max_years = max(10, ceil(max(n["years"] for n in nodes) / 10) * 10)
        low = min(0, floor(min(n["yield_pct"] for n in nodes)))
        high = max(low + 1, ceil(max(n["yield_pct"] for n in nodes) + 0.15))
        y_step = max(1, ceil((high - low) / 7))
        left, top, right, bottom = 82, 151, 827, 533
        height = max(708, 230 + 67 * len(markets))

        def x(years: float) -> float:
            return left + (right - left) * years / max_years

        def y(value: float) -> float:
            return bottom - (bottom - top) * (value - low) / (high - low)

        def text(xp, yp, value, size=13, *, color="#24394a", extra=""):
            return f'<text x="{xp}" y="{yp}" font-size="{size}" fill="{color}"{extra}>{escape(str(value))}</text>'

        heading = "Global sovereign yield curves"
        timestamp = snapshot["generated_at"]
        target = snapshot.get("target_market_date")
        subtitle = (f"Target market date: {target}   |   Compiled: {timestamp}"
                    if target else f"Snapshot cutoff: {timestamp}   |   Market observation dates vary")
        description = " | ".join(
            f"{m['title']}: {m['market_date'] or 'not displayed'}; {m['curve_type']}" for m in markets
        )
        mode = "PUBLIC SNAPSHOT" if public else "LOCAL RESEARCH ONLY"
        bits = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="1216" height="{height}" '
            f'viewBox="0 0 1216 {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{heading}</title>',
            f'<desc id="desc">{escape(timestamp)}. {escape(description)}. '
            'Maturity in years. Annual nominal yield in percent.</desc>',
            f'<rect width="1216" height="{height}" fill="#f4f7f8"/>',
            f'<rect x="26" y="24" width="1164" height="{height - 48}" rx="8" '
            'fill="white" stroke="#dee6ea"/>',
            '<g font-family="system-ui, sans-serif">',
            text(56, 56, f"P-CURVE  /  {mode}", 13, color="#236a74", extra=' font-weight="700"'),
            text(56, 96, heading, 34, extra=' font-weight="720"'),
            text(56, 120, subtitle, 14),
            text(left, top - 10, "Annual nominal yield (%)", 13, extra=' font-weight="650"'),
        ]
        for tick in range(low, high + 1, y_step):
            yp = y(tick)
            bits += [
                f'<path d="M{left},{yp:.2f}H{right}" stroke="#e1e8ed"/>',
                text(left - 9, f"{yp + 4:.2f}", tick, 13, extra=' text-anchor="end"'),
            ]
        step = max(5, ceil(max_years / 50) * 5)
        for tick in sorted({0, 2, max_years, *range(step, max_years, step)}):
            xp = x(tick)
            bits += [
                f'<path d="M{xp:.2f},{top}V{bottom}" stroke="#e9eef0"/>',
                text(f"{xp:.2f}", bottom + 20, tick, 13, extra=' text-anchor="middle"'),
            ]
        bits.extend([
            f'<path d="M{left},{top}V{bottom}H{right}" stroke="#a5b6c2" fill="none"/>',
            text((left + right) / 2, 580, "Maturity (years)", 14, extra=' text-anchor="middle"'),
            '<path d="M856,151V573" stroke="#e1e8ed"/>',
            text(881, 158, "MARKET / OBSERVATION DATE", 12, extra=' font-weight="700"'),
            text(1163, 158, "10Y", 12, extra=' font-weight="700" text-anchor="end"'),
        ])
        for i, market in enumerate(markets):
            available = market["status"] == "AVAILABLE"
            color, pattern = STYLES[i % len(STYLES)]
            if not available:
                color, pattern = "#627480", "2 4"
            dash = f' stroke-dasharray="{pattern}"' if pattern else ""
            vals = {n["years"]: n["yield_pct"] for n in market["nodes"] if n["yield_pct"] is not None}
            value = f'{vals[10]:.3f}%' if 10 in vals else "-"
            yy = 186 + 62 * i
            no_data = "Not displayed: rights HOLD" if market["rights"]["status"] == "HOLD" else "No verified nodes"
            date_label = market["market_date"] if available else no_data
            if available and target:
                role = "Target date" if market["market_date"] == target else "Earlier reference"
                date_label = f"{date_label}  /  {role}"
            bits += [
                f'<path d="M882,{yy - 4}h22" stroke="{color}" stroke-width="3"{dash}/>',
                text(914, yy, market["title"], 15, color=color, extra=' font-weight="720"'),
                text(1163, yy, value, 14, extra=' text-anchor="end" font-weight="700"'),
                text(914, yy + 17, date_label, 12),
                text(914, yy + 33, market["curve_type"], 12),
            ]
            if not available:
                continue
            parts = []
            markers = []
            next_cmd = "M"
            for node in market["nodes"]:
                rate = node["yield_pct"]
                if rate is None:
                    next_cmd = "M"
                    continue
                px, py = x(node["years"]), y(rate)
                parts.append(f"{next_cmd}{px:.2f},{py:.2f}")
                next_cmd = "L"
                label = escape(f"{market['title']}, {node['tenor']}: {rate:g}%")
                markers.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="2.4"><title>{label}</title></circle>')
            bits += [
                f'<g id="{market["id"]}" fill="{color}">',
                f'<path d="{" ".join(parts)}" stroke="{color}" stroke-width="2.8" fill="none"{dash}/>',
                *markers,
                "</g>",
            ]
        bits += [
            '<path d="M56,598H1160" stroke="#dee6ea"/>',
            text(56, 621, "Local-currency rates in source conventions: par, interpolated bond yields, benchmark yields and spot yields are not interchangeable.", 12),
            text(56, 642, "Markers are source nodes. Lines are visual guides; no filled gaps, extrapolation or tradeable cross-currency spread.", 12),
            text(56, 663, "Sources: US Treasury, Japan MOF, RBA, MAS" +
                 ("; local series: CCDC and Bank of England." if not public else ".") +
                 " See data and rights notes. Curated by pengyi.", 12),
            "</g></svg>",
        ]
        return "\n".join(bits) + "\n"

    def write(self, snapshot: dict, output: Path, *, public: bool = True) -> None:
        svg = self.render(snapshot, public=public)
        try:
            with output.open("x", encoding="utf-8", newline="\n") as file:
                file.write(svg)
        except FileExistsError:
            if output.read_bytes() != svg.encode("utf-8"):
                raise ValueError(f"refusing to overwrite an existing chart: {output}") from None
