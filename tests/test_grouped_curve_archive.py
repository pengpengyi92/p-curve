"""Verify the grouped edition links only reviewed public curves."""
import importlib.util
import json
import re
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CURVE = ROOT / "curve"
EDITION = "20261114T155232Z"
OBS = {
    "united-states": {"ust": ("2026-11-13", 14)},
    "japan": {"jgb": ("2026-11-12", 15)},
    "euro-area": {"euro_area_aaa": ("2026-11-12", 358), "euro_area_all": ("2026-11-12", 358)},
    "australia": {"australia": ("2026-11-11", 4)},
}
SPEC = importlib.util.spec_from_file_location("grouped_renderer", ROOT / "scripts/curve_archive.py")
RENDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDER)


class GroupedCurveArchiveTests(unittest.TestCase):
    def test_public_source_metadata_and_svg_nodes_match(self):
        for region, expected in OBS.items():
            with self.subTest(region=region):
                directory = CURVE / "developed" / region / EDITION
                shot = json.loads((directory / "snapshot.json").read_text(encoding="utf-8"))
                RENDER.validate_snapshot(shot, public=True)
                self.assertEqual(shot["snapshot_id"], EDITION)
                self.assertEqual(
                    {m["id"]: (m["market_date"], len(m["nodes"])) for m in shot["markets"]}, expected,
                )
                for market in shot["markets"]:
                    svg = ET.parse(directory / (market["id"] + ".svg"))
                    points = svg.findall(".//{http://www.w3.org/2000/svg}circle")
                    self.assertEqual(len(points), len(market["nodes"]))
                    self.assertIn(market["market_date"], ET.tostring(svg.getroot(), encoding="unicode"))

    def test_links_stay_inside_archive_and_resolve(self):
        pages = [CURVE / "index.html", *(p for p in CURVE.rglob("index.html") if p.parent.name == EDITION)]
        self.assertEqual(len(pages), 10)
        for page in pages:
            for ref in re.findall(r'(?:href|src)="([^"]+)"', page.read_text(encoding="utf-8")):
                if ref.startswith("https://"):
                    continue
                with self.subTest(page=page, link=ref):
                    target = (page.parent / ref).resolve()
                    self.assertTrue(target.is_relative_to(CURVE))
                    self.assertTrue(target.is_file())

    def test_hold_geographies_ship_only_a_source_note(self):
        for group, region in [("developed", "hong-kong"), ("developed", "united-kingdom"),
                              ("emerging", "china")]:
            with self.subTest(region=region):
                path = CURVE / group / region / EDITION
                self.assertEqual({file.name for file in path.iterdir()}, {"index.html"})
                self.assertNotIn("<img ", (path / "index.html").read_text(encoding="utf-8"))
