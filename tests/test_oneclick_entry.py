"""Offline entry-point checks; hosted rendering is verified separately."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Elements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag,dict(attrs)))

    def handle_data(self, value):
        self.text.append(value)


class OneClickEntryTests(unittest.TestCase):
    def test_root_redirect_and_pages_marker(self):
        self.assertTrue((ROOT/'.nojekyll').is_file())
        doc = Elements()
        doc.feed((ROOT/'index.html').read_text(encoding='utf-8'))
        redirects = [a for tag,a in doc.tags if tag=='meta' and a.get('http-equiv')=='refresh']
        self.assertEqual([x['content'] for x in redirects],['0;url=curve/index.html'])
        self.assertTrue((ROOT/'curve/index.html').is_file())

    def test_local_launcher_only_opens_sibling_html(self):
        launcher = (ROOT/'curve/OPEN_OVERVIEW.cmd').read_text(encoding='utf-8').splitlines()
        self.assertEqual(launcher,['@echo off','start "" "%~dp0index.html"'])

    def test_readme_places_actual_rendered_and_source_entries_together(self):
        for filename in ('README.md','curve/README.md'):
            text = (ROOT/filename).read_text(encoding='utf-8')
            self.assertIn('https://pengpengyi92.github.io/p-curve/curve/',text)
            self.assertIn('HTML source',text)
            self.assertIn('OPEN_OVERVIEW.cmd',text)

    def test_current_viewer_keeps_author_and_local_selected_images(self):
        doc = Elements()
        doc.feed((ROOT/'curve/index.html').read_text(encoding='utf-8'))
        text = ' '.join(doc.text)
        self.assertRegex(text,r'Author:\s*pengyi')
        self.assertIn('What a beautiful curve.',text)
        images = [attrs['src'] for tag,attrs in doc.tags if tag=='img']
        self.assertEqual(len(images),4)
        self.assertEqual({Path(src).stem for src in images},
                         {'ust','jgb','euro_area_aaa','euro_area_all'})
        for src in images:
            self.assertNotRegex(src,r'^(?:https?:|file:|/|[A-Za-z]:)')
            target = (ROOT/'curve'/src).resolve()
            self.assertTrue(target.is_relative_to(ROOT/'curve'))
            self.assertTrue(target.is_file())


if __name__ == '__main__':
    unittest.main()
