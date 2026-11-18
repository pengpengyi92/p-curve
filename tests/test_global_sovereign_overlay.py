"""Test data boundaries and regeneration of the README chart."""

import copy
from decimal import Decimal
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from examples.global_sovereign_overlay.data_collector import DataCollector
from examples.global_sovereign_overlay.drawer import Drawer
from examples.global_sovereign_overlay.generate import EDITION, ROOT

SVG = {"svg": "http://www.w3.org/2000/svg"}
ARCHIVED_EDITION = ROOT / "curve/20261118T161713Z"


class GlobalSovereignOverlayTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = DataCollector(ARCHIVED_EDITION / "config.json").collect()

    def _markets(self):
        return {m["id"]: m for m in self.snapshot["markets"]}

    def _local_fixture(self):
        snapshot = copy.deepcopy(self.snapshot)
        market = next(m for m in snapshot["markets"] if m["id"] == "cgb")
        # Deliberately fake regression values, never part of any published curve.
        market.update(status="AVAILABLE", market_date="2026-11-18",
                      nodes=[{"tenor": "10Y", "years": 10, "yield_pct": 99.875}])
        return snapshot

    def test_public_snapshot_dates_counts_and_holds(self):
        markets = self._markets()
        self.assertEqual(self.snapshot["generated_at"], "2026-11-19T00:17:13+08:00")
        self.assertEqual(
            {k: (m["market_date"], len(m["nodes"])) for k, m in markets.items()},
            {"ust": ("2026-11-17", 14), "jgb": ("2026-11-17", 15),
             "au": ("2026-11-11", 4), "sg": ("2026-11-18", 7),
             "cgb": (None, 0), "uk": (None, 0)},
        )
        self.assertEqual({k for k, m in markets.items() if m["rights"]["status"] == "HOLD"}, {"cgb", "uk"})

    def test_official_known_tenors_and_slope(self):
        yields = {key: {n["years"]: Decimal(str(n["yield_pct"])) for n in market["nodes"]}
                  for key, market in self._markets().items()}
        for market, rate in {"ust": "5.10", "jgb": "2.925", "au": "5.044", "sg": "2.29"}.items():
            self.assertEqual(yields[market][10], Decimal(rate))
        self.assertEqual((yields["ust"][10] - yields["ust"][2]) * 100, Decimal("30"))
        self.assertEqual((yields["jgb"][10] - yields["jgb"][2]) * 100, Decimal("104.7"))

    def test_config_holds_require_explicit_local_mode(self):
        fixture = self._local_fixture()
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "config.json"
            config.write_text(json.dumps(fixture), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "public export blocked: cgb"):
                DataCollector(config).collect()
            self.assertEqual(DataCollector(config).collect(public=False), fixture)
        with self.assertRaisesRegex(ValueError, "cannot include HOLD nodes"):
            Drawer().render(fixture)
        self.assertIn("99.875%", Drawer().render(fixture, public=False))

    def test_config_rejects_future_market_dates(self):
        with tempfile.TemporaryDirectory() as directory:
            self.snapshot["markets"][0]["market_date"] = "2026-11-20"
            config = Path(directory) / "config.json"
            config.write_text(json.dumps(self.snapshot), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "market_date cannot be after"):
                DataCollector(config).collect()

    def test_regenerates_exact_chart_with_only_approved_markers(self):
        svg = Drawer().render(self.snapshot)
        self.assertEqual(svg.encode("utf-8"), (ARCHIVED_EDITION / "global_sovereign_yields.svg").read_bytes())
        root = ET.fromstring(svg)
        self.assertEqual(len(root.findall(".//svg:circle", SVG)), 40)
        self.assertEqual({g.get("id") for g in root.findall(".//svg:g[@id]", SVG)}, {"ust", "jgb", "au", "sg"})
        self.assertEqual(svg.count("Not displayed: rights HOLD"), 2)

    def test_target_edition_labels_actual_dates_and_regenerates(self):
        snapshot = DataCollector(EDITION / "config.json").collect()
        self.assertEqual(snapshot["target_market_date"], "2026-11-18")
        self.assertEqual(snapshot["generated_at"], "2026-11-19T00:27:11+08:00")
        self.assertEqual([m["id"] for m in snapshot["markets"]
                          if m["market_date"] == snapshot["target_market_date"]], ["sg"])
        svg = Drawer().render(snapshot)
        self.assertEqual(svg.encode("utf-8"), (EDITION / "global_sovereign_yields.svg").read_bytes())
        self.assertIn("2026-11-18  /  Target date", svg)
        self.assertEqual(svg.count("/  Earlier reference"), 3)

    def test_target_date_rejects_invalid_or_later_observations(self):
        for target, error in [
            ("2026-11-31", "YYYY-MM-DD"),
            ("2026-11-20", "follow the compilation date"),
            ("2026-11-17", "observation cannot be after"),
        ]:
            with self.subTest(target=target), tempfile.TemporaryDirectory() as directory:
                payload = dict(self.snapshot, target_market_date=target)
                config = Path(directory) / "config.json"
                config.write_text(json.dumps(payload), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, error):
                    DataCollector(config).collect()

    def test_homepage_does_not_embed_archived_november_19_chart(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("](curve/20261118T162711Z/global_sovereign_yields.svg)", readme)
        self.assertNotIn("curve/20261118T161713Z/global_sovereign_yields.svg", readme)

    def test_existing_different_chart_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "chart.svg"
            drawer = Drawer()
            drawer.write(self.snapshot, path)
            drawer.write(self.snapshot, path)  # Exact rerender is harmless.
            original = path.read_bytes()
            changed = copy.deepcopy(self.snapshot)
            changed["markets"][0]["nodes"][-1]["yield_pct"] = 6.0
            with self.assertRaisesRegex(ValueError, "refusing to overwrite"):
                drawer.write(changed, path)
            self.assertEqual(path.read_bytes(), original)
