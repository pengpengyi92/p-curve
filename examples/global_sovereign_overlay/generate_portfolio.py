"""Render the frozen regional portfolio offline with DataCollector and Drawer."""

import argparse
from datetime import date
from pathlib import Path
import re

from scripts.curve_archive import load_snapshot, validate_snapshot

from .data_collector import DataCollector
from .drawer import Drawer
from .generate import ROOT


EDITION = ROOT / "curve/portfolio/20261118T180812Z"


def compose(edition: Path = EDITION) -> dict:
    spec = load_snapshot(edition / "portfolio.json")
    required = {"sources", "window", "groups"}
    if not required.issubset(spec) or set(spec) - (required | {"layout"}):
        raise ValueError("invalid portfolio keys")
    if "layout" in spec and spec["layout"] != "coverage":
        raise ValueError("unrecognized portfolio layout")
    recent = DataCollector(edition / "config.json").collect()
    if recent["snapshot_id"] != edition.name:
        raise ValueError("portfolio snapshot_id must match the edition directory")
    start, end = map(date.fromisoformat, spec["window"])
    if start > end or end > date.fromisoformat(recent["generated_at"][:10]):
        raise ValueError("invalid portfolio observation window")

    inputs = [(recent, None)]
    for entry in spec["sources"]:
        if isinstance(entry, str):
            source, selection = entry, None
        elif isinstance(entry, dict) and set(entry) == {"path", "markets"}:
            source, selection = entry["path"], entry["markets"]
            if not isinstance(selection, list) or not selection or len(selection) != len(set(selection)):
                raise ValueError("portfolio source selection must contain distinct market IDs")
        else:
            raise ValueError("invalid portfolio source reference")
        path = (ROOT / source).resolve()
        if not path.is_relative_to(ROOT / "curve"):
            raise ValueError("portfolio sources must be frozen repository curve configs")
        inputs.append((DataCollector(path).collect(), selection))

    markets = {}
    observations = {}
    for snapshot, selection in inputs:
        available_ids = {m["id"] for m in snapshot["markets"]}
        if selection is not None and set(selection) - available_ids:
            raise ValueError("portfolio source includes an unknown selected market")
        selected = available_ids if selection is None else set(selection)
        for market in snapshot["markets"]:
            key = market["id"]
            if key not in selected:
                continue
            if key in markets:
                raise ValueError(f"duplicate source market: {key}")
            markets[key] = market
        observations.update({key: points for key, points in snapshot.get("point_observations", {}).items()
                             if key in selected})

    outputs = {}
    for slug, group in spec["groups"].items():
        if not re.fullmatch(r"[a-z][a-z_-]{0,30}", slug) or set(group) != {"title", "markets"}:
            raise ValueError(f"invalid portfolio group: {slug}")
        ids = group["markets"]
        if len(ids) < 2 or len(ids) != len(set(ids)) or set(ids) - markets.keys():
            raise ValueError(f"group must contain distinct known markets: {slug}")
        selected_points = {key: observations[key] for key in ids if key in observations}
        view = {**recent, "title": group["title"], "markets": [markets[key] for key in ids]}
        view.pop("point_observations", None)
        validate_snapshot(view, public=True)
        for market in view["markets"]:
            if market["status"] != "AVAILABLE" or sum(n["yield_pct"] is not None for n in market["nodes"]) < 2:
                raise ValueError(f"group includes an empty or single-point market: {market['id']}")
            days = [market["market_date"]]
            days.extend(point["market_date"] for point in selected_points.get(market["id"], {}).values())
            if any(not start <= date.fromisoformat(day) <= end for day in days):
                raise ValueError(f"observation outside the portfolio window: {market['id']}")
        outputs[slug] = {**view, "point_observations": selected_points}
        if "layout" in spec:
            outputs[slug]["layout"] = spec["layout"]
    if not outputs:
        raise ValueError("portfolio has no groups")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--edition", type=Path, default=EDITION, help="frozen portfolio directory")
    parser.add_argument("--output-dir", type=Path, help="defaults to the edition directory")
    args = parser.parse_args()
    views = compose(args.edition)
    output_dir = args.output_dir or args.edition
    output_dir.mkdir(parents=True, exist_ok=True)
    drawer = Drawer()
    for slug, view in views.items():
        output = output_dir / f"{slug}.svg"
        drawer.write(view, output, portfolio=True)
        print(f"{slug}: {len(view['markets'])} series -> {output.name}")


if __name__ == "__main__":
    main()
