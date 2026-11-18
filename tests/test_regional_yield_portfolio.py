"""Verify regional coverage, actual observations and independent SVG replay."""

from datetime import date
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from examples.global_sovereign_overlay.drawer import Drawer
from examples.global_sovereign_overlay.generate import ROOT
from examples.global_sovereign_overlay.generate_portfolio import EDITION, compose


SVG = {"svg": "http://www.w3.org/2000/svg"}
GROUPS = {
    "advanced": {"ust", "ca", "uk", "au", "jgb", "hk", "sg", "kr"},
    "asia": {"hk", "sg", "cgb", "jgb", "kr"},
    "americas": {"ust", "ca", "mx", "br"},
    "europe": {"uk", "euro_area_aaa", "euro_area_all"},
    "oceania": {"au", "nz"},
    "emerging": {"cgb", "mx", "br"},
}


class RegionalYieldPortfolioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.views = compose()

    def test_groups_contain_only_real_dated_available_series(self):
        self.assertEqual(list(self.views), list(GROUPS))
        for group, view in self.views.items():
            self.assertEqual({m["id"] for m in view["markets"]}, GROUPS[group])
            for market in view["markets"]:
                self.assertEqual(market["status"], "AVAILABLE")
                self.assertEqual(market["rights"]["status"], "APPROVED_PUBLIC_DISPLAY")
                self.assertGreaterEqual(sum(n["yield_pct"] is not None for n in market["nodes"]), 2)
                self.assertLessEqual(date(2026, 10, 1), date.fromisoformat(market["market_date"]))
                self.assertLessEqual(date.fromisoformat(market["market_date"]), date(2026, 11, 18))
        days = {obs["market_date"] for view in self.views.values()
                for market in view["point_observations"].values() for obs in market.values()}
        self.assertEqual((min(days), max(days)), ("2026-10-21", "2026-11-18"))

    def test_selected_official_observations(self):
        markets = {m["id"]: m for view in self.views.values() for m in view["markets"]}
        anchors = {"ca": ("10Y", 3.81), "hk": ("10Y", 4.164), "kr": ("10Y", 3.985),
                   "nz": ("2032-05-15", 4.2163), "mx": ("91D", 6.49), "br": ("2032-01-01", 15.35)}
        for key, expected in anchors.items():
            with self.subTest(market=key):
                self.assertIn(expected, [(n["tenor"], n["yield_pct"]) for n in markets[key]["nodes"]])
        self.assertAlmostEqual(markets["nz"]["nodes"][0]["years"], 5.5112936345)
        self.assertEqual(len(markets["euro_area_aaa"]["nodes"]), 358)
        self.assertEqual(len(markets["euro_area_all"]["nodes"]), 358)
        self.assertEqual(len(markets), 14)

    def test_svg_bytes_exact_and_every_auction_is_a_diamond(self):
        for group, view in self.views.items():
            with self.subTest(group=group):
                svg = Drawer().render(view, portfolio=True)
                self.assertEqual(svg.encode("utf-8"), (EDITION / f"{group}.svg").read_bytes())
                tree = ET.fromstring(svg)
                markets = {m["id"]: m for m in view["markets"]}
                self.assertEqual({g.get("id") for g in tree.findall(".//svg:g[@id]", SVG)}, markets.keys())
                for key, market in markets.items():
                    plot = tree.find(f".//svg:g[@id='{key}']", SVG)
                    count = sum(n["yield_pct"] is not None for n in market["nodes"])
                    if key in view["point_observations"]:
                        self.assertEqual(len(plot.findall("svg:polygon", SVG)), count)
                        self.assertIsNone(plot.find("svg:path", SVG))
                    else:
                        self.assertEqual(len(plot.findall("svg:circle", SVG)), count)
                        self.assertIsNotNone(plot.find("svg:path", SVG))

    def test_readme_embeds_all_groups_after_original(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        position = readme.index("curve/20261118T172919Z/global_sovereign_yields.svg")
        for group in GROUPS:
            asset = f"](curve/portfolio/{EDITION.name}/{group}.svg)"
            self.assertEqual(readme.count(asset), 1)
            self.assertGreater(readme.index(asset), position)
            position = readme.index(asset)

    def test_mismatched_source_group_and_window_fail_closed(self):
        for change, error in [
            ({"sources": ["../elsewhere.json"]}, "frozen repository curve configs"),
            ({"window": ["2026-11-01", "2026-11-18"]}, "outside the portfolio window: hk"),
            ({"groups": {"fake": {"title": "Missing", "markets": ["ust", "unknown"]}}}, "distinct known markets"),
        ]:
            with self.subTest(change=change), tempfile.TemporaryDirectory() as temp:
                edition = Path(temp) / EDITION.name
                edition.mkdir()
                (edition / "config.json").write_bytes((EDITION / "config.json").read_bytes())
                spec = json.loads((EDITION / "portfolio.json").read_text(encoding="utf-8"))
                (edition / "portfolio.json").write_text(json.dumps({**spec, **change}), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, error):
                    compose(edition)
