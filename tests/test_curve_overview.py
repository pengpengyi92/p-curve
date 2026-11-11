"""Synthetic current-portal tests; frozen archive data must remain unchanged."""
import copy
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    'curve_overview_tests_module', Path(__file__).resolve().parents[1] / 'scripts/curve_overview.py'
)
overview = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(overview)


def fixture():
    return {
        'schema_version':'1.0.0','snapshot_id':'20261111T143334Z',
        'title':'Fictional sourced curves','generated_at':'2026-11-11T14:33:34+00:00',
        'markets':[{
            'id':'fictional','title':'Fictional curve','currency':'USD','market_date':'2026-11-10',
            'asof':'fictional dated fixture','retrieved_at':'2026-11-11T14:30:00+00:00',
            'source_url':'https://example.org/source','curve_type':'FICTIONAL continuous zero',
            'units':'percent_per_annum','status':'AVAILABLE',
            'rights':{'status':'APPROVED_PUBLIC_DISPLAY','source_url':'https://example.org/rights',
                      'reason':'Fictional permission; not a real source-rights assertion'},
            'nodes':[{'tenor':'1Y','years':1,'yield_pct':2.0},
                     {'tenor':'2Y','years':2,'yield_pct':None},
                     {'tenor':'3Y','years':3,'yield_pct':3.0}],
            'notes':['Source: fictional publisher. No real market data.']
        }]
    }


class CurveOverviewTests(unittest.TestCase):
    def test_author_comments_dates_and_attribution_are_explicit(self):
        text=overview.render_overview(fixture(),public=True)
        for expected in ['Author:','pengyi','Curated &amp; visualized by pengyi',
                         'original publishers','What a beautiful curve.',
                         'Editorial appreciation','not investment analysis',
                         '2026-11-10','2026-11-11T14:33:34+00:00','2 source nodes',
                         'Source: example.org']:
            self.assertIn(expected,text)

    def test_relative_links_are_portable_and_no_external_runtime(self):
        text=overview.render_overview(fixture(),public=True)
        for target in ['20261111T143334Z/fictional.svg','20261111T143334Z/index.html',
                       '20261111T143334Z/snapshot.json']:
            self.assertIn(target,text)
        self.assertNotIn('<script',text)
        self.assertNotIn('iframe',text)
        self.assertNotIn('file://',text)
        self.assertIn('prefers-reduced-motion',text)

    def test_full_native_table_retains_missing_positions_and_source_context(self):
        text=overview.render_overview(fixture(),public=True)
        self.assertIn('Full native node table (2 actual / 3 supplied positions)',text)
        for node in fixture()['markets'][0]['nodes']:
            self.assertIn('<td>'+node['tenor']+'</td>',text)
        self.assertIn('UNAVAILABLE',text)
        self.assertIn('Yield (% p.a.)',text)
        self.assertIn('As-of: fictional dated fixture',text)
        self.assertIn('2026-11-11T14:30:00+00:00',text)
        self.assertIn('@media(min-width:1400px)',text)

    def test_hostile_author_and_source_text_are_escaped(self):
        data=fixture();data['title']='<script>alert(1)</script>'
        data['markets'][0]['notes']=['<img src=x onerror="bad">']
        text=overview.render_overview(data,author='<b>person</b>',public=True)
        self.assertNotIn('<script>',text)
        self.assertNotIn('<b>person</b>',text)
        self.assertIn('&lt;b&gt;person&lt;/b&gt;',text)
        self.assertIn('&lt;img',text)

    def test_rights_hold_refused_for_public_and_visible_locally(self):
        data=fixture();data['markets'][0]['rights']['status']='HOLD'
        with self.assertRaises(ValueError):
            overview.render_overview(data,public=True)
        local=overview.render_overview(data)
        self.assertIn('Not approved for public redistribution',local)
        self.assertIn('HOLD',local)

    def test_rendering_does_not_mutate_source(self):
        data=fixture();original=copy.deepcopy(data)
        overview.render_overview(data,public=True)
        self.assertEqual(data,original)

    def test_invalid_authors_rejected(self):
        for author in ['',None,'x'*101,'name\nsecondline']:
            with self.subTest(author=author),self.assertRaises(ValueError):
                overview.render_overview(fixture(),author=author)

    def test_writes_only_root_portal_and_preserves_every_frozen_byte(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            frozen=overview.archive.write_archive(fixture(),root,public=True)
            before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in frozen.iterdir()}
            output=overview.write_overview(frozen/'snapshot.json',root/'index.html',public=True)
            self.assertEqual(output,root/'index.html')
            self.assertIn(overview.MARKER,output.read_text(encoding='utf-8'))
            overview.write_overview(frozen/'snapshot.json',root/'index.html',author='another',public=True)
            self.assertIn('another',output.read_text(encoding='utf-8'))
            after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in frozen.iterdir()}
            self.assertEqual(before,after)

    def test_output_inside_snapshot_or_outside_archive_root_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);frozen=overview.archive.write_archive(fixture(),root,public=True)
            for target in [frozen/'index.html',frozen/'new.html',root/'other.html',root/'elsewhere/index.html']:
                with self.subTest(target=target),self.assertRaises(ValueError):
                    overview.write_overview(frozen/'snapshot.json',target,public=True)

    def test_existing_unrelated_root_html_is_not_replaced(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);frozen=overview.archive.write_archive(fixture(),root,public=True)
            output=root/'index.html';output.write_text('unrelated user page',encoding='utf-8')
            with self.assertRaises(FileExistsError):
                overview.write_overview(frozen/'snapshot.json',output,public=True)
            self.assertEqual(output.read_text(encoding='utf-8'),'unrelated user page')

    def test_public_hold_refused_before_portal_creation(self):
        data=fixture();data['markets'][0]['rights']['status']='HOLD'
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);frozen=overview.archive.write_archive(data,root)
            with self.assertRaises(ValueError):
                overview.write_overview(frozen/'snapshot.json',root/'index.html',public=True)
            self.assertFalse((root/'index.html').exists())


if __name__=='__main__':
    unittest.main()
