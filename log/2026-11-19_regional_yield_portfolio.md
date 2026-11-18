# Regional sovereign curve portfolio

- Compilation: `2026-11-19T01:51:56+08:00`; base `a57d100d6f1e39dddf7b13169d21eb319c8b3dee`.
- Added [one dated portfolio](../curve/portfolio/20261118T175156Z/README.md) and six figures
  beneath the existing November chart. Existing frozen inputs and images are not
  replaced. No package version bump, API, dependency or live data integration.
- 14 distinct series across 12 economies and two ECB aggregations, totaling
  789 source nodes. Earliest point is 2026-10-21 and latest is 2026-11-18.
- Scope: source-selected numerical facts and rights-reviewed public snapshots
  only. Reused the existing dated-sovereign-archive precedent and no third-party
  implementation. Do not interpret non-synchronous auction rates, retail
  quotes, par and zero rates as comparable executable prices.

## Verification

Windows, Python 3.12.14, `PYTHONPATH=src`. Baseline `python -X utf8 -m unittest
discover -s tests -q`: 83 pass. Changed tree, same command: 88 pass. New tests
verify the six group memberships, source anchors, date boundaries, per-tenor
auction provenance in SVGs, byte-exact replay and README layout. Inherited
tests still regenerate the three older overlay images byte-for-byte.

`python -X utf8 -m examples.global_sovereign_overlay.generate_portfolio`
produces six SVGs offline; `python -X utf8 examples/synthetic_curve.py` ran
successfully. All six SVGs rendered with isolated Chrome; the Europe legend was
adjusted and rendered again so the all-ratings label clears its 10Y value.
Public file allowlist, source boundary and Git integrity are checked before
push; CI is separate from these local receipts.
