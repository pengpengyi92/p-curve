# Expand the sovereign comparison beyond one month

- Compiled `2026-11-19T02:08:12+08:00`; base commit `20c6cb4`.
- Replace the global overview and six regional figures in the root README
  with the [expanded 2026 edition](../curve/portfolio/20261118T180812Z/README.md).
- Candidate window: Jan 1 to Nov 18 (last completed observation date in
  these sources); selected coverage Apr 14 to Nov 18. 923 distinct nodes,
  versus 789 previously. Every plotted series has an observed sidebar rate,
  at its displayed tenor nearest 10Y. No new future or inferred rates.
- Preserve all dated assets. Replace the Canadian benchmark input in the
  current view because its source table carries CanDeal credit. Use the
  Bank of Canada's own Oct 28 fitted zero output instead. Mexico's longer
  coverage comes from official October monthly auction averages, not fills.

## Evidence

Windows and Python 3.12.14, `PYTHONPATH=src`.
`python -X utf8 -m unittest discover -s tests -q`: baseline 88 passes.
First changed-tree run: three test-oracle failures (an image was wrapped in
a link, Canadian 10Y tenor string was mis-specified and the New Zealand
reference expectation was not actually the nearest 10Y). Corrected assertions;
90 passes on rerun. Tests verify preserved dated charts, expanded coverage,
the fallback tenor and all seven nonblank SVG reference columns.

`python -m examples.global_sovereign_overlay.generate_portfolio` regenerates
all seven charts without network. The previous portfolio also rerenders
byte-for-byte via `--edition curve/portfolio/20261118T175156Z`; the standalone
legacy overlay tests remain green. Chrome desktop visual review checked all
seven SVGs after regenerating the updated legend. Synthetic math example ran.
