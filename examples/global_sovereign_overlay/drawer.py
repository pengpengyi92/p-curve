"""Draw normalized source nodes. Does not read configs or retrieve data."""

from html import escape
from math import ceil, floor, sqrt
from pathlib import Path

# Distinct hues and dash patterns remain identifiable where curves cross.
STYLES = (
    ("#23538c", ""),
    ("#a23f32", "9 4"),
    ("#71419a", "3 3"),
    ("#176f73", "12 4 3 4"),
    ("#a06013", "5 4"),
    ("#23744e", "14 4"),
    ("#9c3e73", "7 3 2 3"),
    ("#526321", "2 5"),
)


class Drawer:
    def render(self, snapshot: dict, *, public: bool = True, portfolio: bool = False) -> str:
        markets = snapshot["markets"]
        coverage = portfolio and snapshot.get("layout") == "coverage"
        point_observations = snapshot.get("point_observations", {})
        if public and any(m["rights"]["status"] == "HOLD" and m["nodes"] for m in markets):
            raise ValueError("public rendering cannot include HOLD nodes")
        nodes = [n for m in markets for n in m["nodes"] if n["yield_pct"] is not None]
        max_years = max(10, ceil(max(n["years"] for n in nodes) / 10) * 10)
        low = floor(min(n["yield_pct"] for n in nodes))
        if not coverage:
            low = min(0, low)
        high = max(low + 1, ceil(max(n["yield_pct"] for n in nodes) + 0.15))
        y_step = max(1, ceil((high - low) / 7))
        left, top, right, bottom = 82, 151, 827, 533
        footer = max(598, 186 + 62 * (len(markets) - 1) + 54)
        height = max(footer + 110, 230 + 67 * len(markets))

        def x(years: float) -> float:
            if coverage:
                return left + (right - left) * sqrt(years / max_years)
            return left + (right - left) * years / max_years

        def y(value: float) -> float:
            return bottom - (bottom - top) * (value - low) / (high - low)

        def text(xp, yp, value, size=13, *, color="#24394a", extra=""):
            return f'<text x="{xp}" y="{yp}" font-size="{size}" fill="{color}"{extra}>{escape(str(value))}</text>'

        heading = snapshot["title"]
        timestamp = snapshot["generated_at"]
        target = snapshot.get("target_market_date")
        subtitle = (f"Target market date: {target}   |   Compiled: {timestamp}"
                    if target else f"Snapshot cutoff: {timestamp}   |   Market observation dates vary")
        if portfolio:
            subtitle = f"Regional portfolio  /  Compiled: {timestamp}  /  Asynchronous observations"
        description = " | ".join(
            f"{m['title']}: {m['market_date'] or 'not displayed'}; {m['curve_type']}" for m in markets
        )
        mode = "PUBLIC SNAPSHOT" if public else "LOCAL RESEARCH ONLY"
        bits = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="1216" height="{height}" '
            f'viewBox="0 0 1216 {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(heading)}</title>',
            f'<desc id="desc">{escape(timestamp)}. {escape(description)}. '
            'Maturity in years. Annual nominal yield in percent.</desc>',
            f'<rect width="1216" height="{height}" fill="#f4f7f8"/>',
            f'<rect x="26" y="24" width="1164" height="{height - 48}" rx="8" '
            'fill="white" stroke="#dee6ea"/>',
            '<g font-family="system-ui, sans-serif">',
            text(56, 56, f"P-CURVE  /  {mode}", 13, color="#236a74", extra=' font-weight="700"'),
            text(56, 96, heading, 34, extra=' font-weight="720"'),
            text(56, 120, subtitle, 14),
            text(left, top - 10, "Annual nominal rate / yield (%)" if point_observations
                 else "Annual nominal yield (%)", 13, extra=' font-weight="650"'),
        ]
        for tick in range(low, high + 1, y_step):
            yp = y(tick)
            bits += [
                f'<path d="M{left},{yp:.2f}H{right}" stroke="#e1e8ed"/>',
                text(left - 9, f"{yp + 4:.2f}", tick, 13, extra=' text-anchor="end"'),
            ]
        if coverage:
            ticks = {max_years, *(v for v in (0, 0.25, 1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 50) if v < max_years)}
        else:
            step = max(5, ceil(max_years / 50) * 5)
            ticks = {0, 2, max_years, *range(step, max_years, step)}
        for tick in sorted(ticks):
            xp = x(tick)
            bits += [
                f'<path d="M{xp:.2f},{top}V{bottom}" stroke="#e9eef0"/>',
                text(f"{xp:.2f}", bottom + 20, tick, 13, extra=' text-anchor="middle"'),
            ]
        bits.extend([
            f'<path d="M{left},{top}V{bottom}H{right}" stroke="#a5b6c2" fill="none"/>',
            text((left + right) / 2, 580, "Maturity (years; square-root spacing)" if coverage
                 else "Maturity (years)", 14, extra=' text-anchor="middle"'),
            f'<path d="M856,151V{max(573, footer - 15)}" stroke="#e1e8ed"/>'
            if portfolio else '<path d="M856,151V573" stroke="#e1e8ed"/>',
            text(881, 158, "MARKET / DATE" if coverage else "MARKET / OBSERVATION DATE", 12,
                 extra=' font-weight="700"'),
            text(1163, 158, "OBSERVED POINT" if coverage else "10Y", 12,
                 extra=' font-weight="700" text-anchor="end"'),
        ])
        for i, market in enumerate(markets):
            available = market["status"] == "AVAILABLE"
            observations = point_observations.get(market["id"])
            color, pattern = STYLES[i % len(STYLES)]
            if not available:
                color, pattern = "#627480", "2 4"
            dash = f' stroke-dasharray="{pattern}"' if pattern else ""
            vals = {n["years"]: n["yield_pct"] for n in market["nodes"] if n["yield_pct"] is not None}
            value = f'{vals[10]:.3f}%' if 10 in vals else "-"
            reference = ""
            if coverage and vals:
                years = min(vals, key=lambda t: (abs(t - 10), t))
                value = f"{vals[years]:.3f}%"
                reference = f"{years:.2f}".rstrip("0").rstrip(".") + "Y"
            yy = 186 + 62 * i
            no_data = "Not displayed: rights HOLD" if market["rights"]["status"] == "HOLD" else "No verified nodes"
            date_label = market["market_date"] if available else no_data
            if available and target:
                role = "Target date" if market["market_date"] == target else "Earlier reference"
                date_label = f"{date_label}  /  {role}"
            legend = f'<path d="M882,{yy - 4}h22" stroke="{color}" stroke-width="3"{dash}/>'
            if observations:
                dates = [o["market_date"] for o in observations.values()]
                date_label = f"{min(dates)} to {max(dates)}"
                if portfolio and min(dates) == max(dates):
                    date_label = min(dates)
                legend = _diamond(893, yy - 4, color)
            curve_label = market["curve_type"]
            if portfolio:
                curve_label = f"{market['currency']} / {curve_label.partition(';')[0]}"
            bits += [
                legend,
                text(914, yy, market["title"], 15, color=color, extra=' font-weight="720"'),
                text(1163, yy + 17 if portfolio else yy, value, 14, extra=' text-anchor="end" font-weight="700"'),
                text(914, yy + 17, date_label, 12),
                text(914, yy + 33, curve_label, 12),
            ]
            if reference:
                bits.append(text(1163, yy + 33, reference, 12, extra=' text-anchor="end"'))
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
                label = f"{market['title']}, {node['tenor']}: {rate:g}%"
                if observations:
                    label += f" | auction on {observations[node['tenor']]['market_date']}"
                    markers.append(_diamond(px, py, color, label))
                else:
                    radius = 1.1 if portfolio and len(market["nodes"]) > 100 else 2.4
                    markers.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{radius}"><title>{escape(label)}</title></circle>')
            bits += [
                f'<g id="{market["id"]}" fill="{color}">',
                *([] if observations else [f'<path d="{" ".join(parts)}" stroke="{color}" stroke-width="2.8" fill="none"{dash}/>']),
                *markers,
                "</g>",
            ]
        comparison_note = ("CGB diamonds are official primary-market auction rates on different dates, not a secondary-market curve."
                           if point_observations else
                           "Local-currency rates in source conventions: par, interpolated bond yields, benchmark yields and spot yields are not interchangeable.")
        sources = ("Sources: US Treasury, China MOF, Japan MOF, Bank of England Database, RBA and MAS."
                   if point_observations else "Sources: US Treasury, Japan MOF, RBA, MAS" +
                   ("; local series: CCDC and Bank of England." if not public else "."))
        if portfolio:
            comparison_note = ("Diamonds: primary auction observations, not a secondary-market curve. Conventions and dates differ."
                               if point_observations else
                               "Par, fitted zero, benchmark-issue and other published yields retain their source conventions.")
            sources = "Sources: see the portfolio source and rights register."
        guides = "Markers are source nodes. Lines are visual guides; no filled gaps, extrapolation or tradeable cross-currency spread."
        if coverage:
            guides = "The sidebar shows the available tenor closest to 10Y. Lines guide the eye; no missing yields are estimated."
        bits += [
            f'<path d="M56,{footer}H1160" stroke="#dee6ea"/>',
            text(56, footer + 23, comparison_note, 12),
            text(56, footer + 44, guides, 12),
            text(56, footer + 65, sources + (" Curated by pengyi." if portfolio else " See data and rights notes. Curated by pengyi."), 12),
            "</g></svg>",
        ]
        return "\n".join(bits) + "\n"

    def write(self, snapshot: dict, output: Path, *, public: bool = True, portfolio: bool = False) -> None:
        svg = self.render(snapshot, public=public, portfolio=portfolio)
        try:
            with output.open("x", encoding="utf-8", newline="\n") as file:
                file.write(svg)
        except FileExistsError:
            if output.read_bytes() != svg.encode("utf-8"):
                raise ValueError(f"refusing to overwrite an existing chart: {output}") from None


def _diamond(x: float, y: float, color: str, label: str = "") -> str:
    tip = f"<title>{escape(label)}</title>" if label else ""
    points = f"{x:.2f},{y-5:.2f} {x+5:.2f},{y:.2f} {x:.2f},{y+5:.2f} {x-5:.2f},{y:.2f}"
    return f'<polygon points="{points}" fill="#fff" stroke="{color}" stroke-width="2">{tip}</polygon>'
