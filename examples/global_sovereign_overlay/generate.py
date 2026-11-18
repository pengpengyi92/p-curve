"""Render the dated public example or an explicitly local comparison."""

import argparse
from pathlib import Path

from .data_collector import DataCollector
from .drawer import Drawer

ROOT = Path(__file__).resolve().parents[2]
EDITION = ROOT / "curve/20261118T161713Z"
BUILD = ROOT / "build"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--local", action="store_true", help="Permit HOLD data; output only to ignored build/")
    args = parser.parse_args()
    if args.local and (args.config is None or args.output is None):
        parser.error("--local requires an explicit --config and --output")
    output = args.output or (EDITION / "global_sovereign_yields.svg")
    if args.local and not output.resolve().is_relative_to(BUILD.resolve()):
        parser.error("local-only charts must stay under build/")
    snapshot = DataCollector(args.config or (EDITION / "config.json")).collect(public=not args.local)
    output.parent.mkdir(parents=True, exist_ok=True)
    Drawer().write(snapshot, output, public=not args.local)
    print(f"{sum(m['status'] == 'AVAILABLE' for m in snapshot['markets'])} curves -> {output}")


if __name__ == "__main__":
    main()
