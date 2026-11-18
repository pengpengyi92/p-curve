# November six-market README replacement

- Compiled `2026-11-19T01:29:19+08:00` from verified November observations.
  Base `76240ce698a40bd8aab6304bfe76d523e38b767c`.
- Reused the four existing public rows. Added BoE Database par rates for
  2026-11-16 (5Y / 10Y / 20Y); retrieved CSV SHA-256
  `ac7259f7843c7c5dc67373aaab5b4a73108d2b63e29633259b28f4e4428883f4`.
  Added six distinct China MOF primary-market points with exact announcement
  URLs and auction dates. Neither HOLD source was published.
- [Data and licenses](../examples/global_sovereign_overlay/README.md) ·
  [New input](../curve/20261118T172919Z/config.json) ·
  [New output](../curve/20261118T172919Z/global_sovereign_yields.svg).
- Same offline DataCollector and Drawer, no external code copied. Both old
  config/figure pairs remain byte-identical. New input draws five curves
  and six distinct auction diamonds, not an inferred China secondary curve.
- Windows 11 / Python 3.12.14: `PYTHONPATH=src`,
  `python -X utf8 -m unittest discover -s tests -q` 83 PASS (baseline 80).
  `python -X utf8 -m examples.global_sovereign_overlay.generate` regenerates
  exact SVG bytes. Checked chart visually in an isolated headless browser.
  Live collection and financial benchmarks were not run.
