"""Synthetic offline archive tests. No live market data or rights claims."""

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "curve_archive.py"
SPEC = importlib.util.spec_from_file_location("curve_archive", MODULE_PATH)
archive = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(archive)


def fixture():
    return {
        "schema_version": "1.0.0", "snapshot_id": "20261111T150000Z",
        "title": "Fictional curve snapshot", "generated_at": "2026-11-11T15:00:00+00:00",
        "markets": [{
            "id": "fictional", "title": "Fictional sovereign curve", "currency": "USD",
            "market_date": "2026-11-10", "asof": "latest verified fictional fixture",
            "retrieved_at": "2026-11-11T14:55:00+00:00", "source_url": "https://example.org/curve",
            "curve_type": "FICTIONAL continuous zero curve", "units": "percent_per_annum",
            "status": "AVAILABLE", "rights": {"status": "APPROVED_PUBLIC_DISPLAY",
                "source_url": "https://example.org/terms", "reason": "Fictional test only; no actual permission assertion"},
            "nodes": [{"tenor": "1Y", "years": 1, "yield_pct": -.1},
                      {"tenor": "2Y", "years": 2, "yield_pct": None},
                      {"tenor": "5Y", "years": 5, "yield_pct": 1.2}],
        }],
    }


class CurveArchiveTests(unittest.TestCase):
    def test_snapshot_keeps_every_input_node_and_missingness(self):
        data = fixture()
        self.assertIs(archive.validate_snapshot(data, public=True), data)
        original = copy.deepcopy(data)
        with tempfile.TemporaryDirectory() as directory:
            path = archive.write_archive(data, Path(directory), public=True)
            self.assertEqual(json.loads((path / "snapshot.json").read_text(encoding="utf-8")), original)
            svg = (path / "fictional.svg").read_text(encoding="utf-8")
            ET.fromstring(svg)
            self.assertEqual(svg.count("<circle "), 2)
            self.assertIn("M", svg)
            self.assertNotIn("L", svg.split('<path d="')[1].split('"')[0])
            self.assertIn("UNAVAILABLE", (path / "index.html").read_text(encoding="utf-8"))
            self.assertEqual(data, original)

    def test_timestamp_title_type_date_source_are_visible(self):
        data = fixture()
        svg = archive.render_svg(data, data["markets"][0], public=True)
        html = archive.render_html(data, public=True)
        for value in [data["generated_at"], "2026-11-10", "Fictional sovereign curve", "https://example.org/curve"]:
            self.assertIn(value, svg)
            self.assertIn(value, html)
        self.assertIn("not additional quotes", svg)
        self.assertNotIn("<script", html)
        self.assertNotIn("https://cdn", html)

    def test_hostile_text_is_escaped_not_executed(self):
        data = fixture()
        data["title"] = '<script>alert("x")</script>'
        data["markets"][0]["title"] = '<img src=x onerror="bad()"> & quote'
        html = archive.render_html(data)
        svg = archive.render_svg(data, data["markets"][0])
        ET.fromstring(svg)
        self.assertNotIn('<script>', html)
        self.assertNotIn('<img src=x', html)
        self.assertIn('&lt;script&gt;', html)
        self.assertIn('&lt;img', svg)

    def test_rights_hold_blocks_public_before_creating_any_output(self):
        data = fixture()
        data["markets"][0]["rights"]["status"] = "HOLD"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "new"
            with self.assertRaisesRegex(ValueError, "HOLD"):
                archive.write_archive(data, root, public=True)
            self.assertFalse(root.exists())
            path = archive.write_archive(data, root)
            self.assertIn("NOT APPROVED FOR PUBLIC REDISTRIBUTION", (path / "index.html").read_text(encoding="utf-8"))

    def test_no_overwrite_existing_archive(self):
        data = fixture()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = archive.write_archive(data, root)
            original = (path / "snapshot.json").read_bytes()
            data["title"] = "Changed title"
            with self.assertRaises(FileExistsError):
                archive.write_archive(data, root)
            self.assertEqual((path / "snapshot.json").read_bytes(), original)
            self.assertEqual(sorted(p.name for p in root.iterdir()), [data["snapshot_id"]])

    def test_duplicate_unsorted_nonfinite_out_of_range_rejected(self):
        invalid_nodes = [
            [{"tenor": "1Y", "years": 1, "yield_pct": 2}, {"tenor": "1Y", "years": 2, "yield_pct": 3}],
            [{"tenor": "2Y", "years": 2, "yield_pct": 2}, {"tenor": "1Y", "years": 1, "yield_pct": 3}],
            [{"tenor": "1Y", "years": 1, "yield_pct": float("nan")}],
            [{"tenor": "1Y", "years": 1, "yield_pct": float("inf")}],
            [{"tenor": "1Y", "years": 1, "yield_pct": 500}],
            [{"tenor": "0Y", "years": 0, "yield_pct": 2}],
            [{"tenor": "1Y", "years": True, "yield_pct": 2}],
        ]
        for nodes in invalid_nodes:
            data = fixture()
            data["markets"][0]["nodes"] = nodes
            with self.subTest(nodes=nodes), self.assertRaises(ValueError):
                archive.validate_snapshot(data)

    def test_timestamp_and_future_market_date_rejected(self):
        changes = [({"generated_at": "2026-11-11T15:00:00"}, {}),
                   ({}, {"retrieved_at": "2026-11-11T16:00:00+00:00"}),
                   ({}, {"market_date": "2026-11-12"}),
                   ({}, {"market_date": "bad-date"})]
        for top, market in changes:
            data = fixture()
            data.update(top)
            data["markets"][0].update(market)
            with self.subTest(top=top, market=market), self.assertRaises(ValueError):
                archive.validate_snapshot(data)

    def test_paths_unsafe_urls_and_unreviewed_keys_rejected(self):
        for value in ["../escape", "nested/path", "CON", "a.b"]:
            data = fixture()
            data["snapshot_id"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                archive.validate_snapshot(data)
        for url in ["javascript:alert(1)", "file:///private", "https://name:secret@example.org/"]:
            data = fixture()
            data["markets"][0]["source_url"] = url
            with self.subTest(url=url), self.assertRaises(ValueError):
                archive.validate_snapshot(data)
        data = fixture()
        data["private_notes"] = "must not silently pass through export"
        with self.assertRaises(ValueError):
            archive.validate_snapshot(data)

    def test_duplicate_market_and_json_keys_rejected(self):
        data = fixture()
        data["markets"].append(copy.deepcopy(data["markets"][0]))
        with self.assertRaises(ValueError):
            archive.validate_snapshot(data)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_text('{"title":"a","title":"b"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                archive.load_snapshot(path)

    def test_empty_market_remains_unavailable_not_zero(self):
        data = fixture()
        data["markets"][0].update(status="UNAVAILABLE", market_date=None, nodes=[])
        archive.validate_snapshot(data)
        svg = archive.render_svg(data, data["markets"][0])
        self.assertIn("UNAVAILABLE — no verified yield nodes", svg)
        self.assertNotIn("<circle ", svg)


if __name__ == "__main__":
    unittest.main()
