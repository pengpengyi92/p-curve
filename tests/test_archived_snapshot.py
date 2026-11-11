"""Regression checks for the first rights-reviewed real-data public archive."""
import importlib.util
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'curve/20261111T143334Z'
SPEC = importlib.util.spec_from_file_location('archive_snapshot_checks', ROOT / 'scripts/curve_archive.py')
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)


class ArchivedSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = renderer.load_snapshot(ARCHIVE / 'snapshot.json')

    def test_initial_snapshot_contains_only_reviewed_public_sources(self):
        renderer.validate_snapshot(self.snapshot, public=True)
        self.assertEqual(self.snapshot['generated_at'], '2026-11-11T14:33:34+00:00')
        markets = {m['id']:m for m in self.snapshot['markets']}
        self.assertEqual(set(markets), {'ust','jgb','euro_area_aaa','euro_area_all'})
        self.assertEqual({k:len(m['nodes']) for k,m in markets.items()},
                         {'ust':14,'jgb':15,'euro_area_aaa':358,'euro_area_all':358})
        self.assertTrue(all(m['market_date']=='2026-11-10' for m in markets.values()))

    def test_native_grid_and_known_source_anchor_values_preserved(self):
        markets = {m['id']:m for m in self.snapshot['markets']}
        ust = {n['tenor']:n['yield_pct'] for n in markets['ust']['nodes']}
        self.assertEqual(ust['1.5M'],4.16)
        self.assertEqual(ust['10Y'],4.98)
        self.assertNotIn('4Y',ust)
        jgb = {n['tenor']:n['yield_pct'] for n in markets['jgb']['nodes']}
        self.assertEqual(jgb['1Y'],1.597)
        self.assertEqual(jgb['40Y'],3.996)
        self.assertNotIn('11Y',jgb)
        for key in ('euro_area_aaa','euro_area_all'):
            nodes = markets[key]['nodes']
            self.assertEqual(nodes[0]['tenor'],'3M')
            self.assertEqual(nodes[-1]['tenor'],'30Y')
            self.assertTrue(all(abs(n['years']-(i+3)/12)<1e-12 for i,n in enumerate(nodes)))

    def test_svg_chart_points_and_metadata_match_snapshot(self):
        ns = {'s':'http://www.w3.org/2000/svg'}
        for market in self.snapshot['markets']:
            with self.subTest(market=market['id']):
                text = (ARCHIVE / (market['id']+'.svg')).read_text(encoding='utf-8')
                svg = ET.fromstring(text)
                self.assertEqual(svg.find('s:title',ns).text,market['title'])
                self.assertEqual(len(svg.findall('.//s:circle',ns)),len(market['nodes']))
                self.assertIn(self.snapshot['generated_at'],text)
                self.assertIn(market['market_date'],text)
                self.assertIn('PUBLIC DISPLAY',text)
                self.assertNotIn('<script',text)


if __name__ == '__main__':
    unittest.main()
