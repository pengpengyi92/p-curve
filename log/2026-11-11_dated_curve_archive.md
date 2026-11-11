# Dated curve archive — 2026-11-11

## Delivered scope

Owner requested timestamped sovereign curve storage. Version0.2.0 adds the
offline standard-library renderer, append-only archive protocol and a selected
public snapshot `20261111T143334Z`, generated14:33:34UTC /22:33:34Asia/Shanghai.
It preserves745 actual published points across UST, JGB and ECB euro-area AAA /
all-ratings. Every included source's latest market date was2026-11-10, not11-11.

Requested CGB, HKGB and UK derived data/figures remain excluded from this public
repository because the required public reuse rights were not established. The
rights-review document distinguishes those HOLD sources from approved ones.
No private archive/history or raw CSV, XLS/XLSX, ZIP download is exported.

## Source, code and data gates

- Original offline rendering code; OpenBB's pinned ECB/Fed yield-curve handlers
  establish a same-topic public precedent. No external implementation was copied.
- Treasury CC0 metadata; Japan MOF PDL1.0 with attribution/adaptation note; ECB
  accurate reproduction with attribution and research-display limitations.
- MIT code license is explicitly separated from source-specific data conditions.
- All native source points retained: UST14 includes1.5M/2M/4M; JGB15 includes40Y;
  both ECB groups retain358 monthly points3M–30Y. No missing annual point invented.
- This is a collected daily source snapshot, not synchronized live market data,
  a zero-curve conversion, pricing validation, PIT backtest or trade signal.

## Verification

- Full local suite **49/49 PASS**:30math +4repository +12renderer +3actual-archive
  regression tests. No skipped tests. Fresh0.2.0 wheel install PASS.
- Independent source-to-output checks PASS: all selected source values unchanged,
 745 public nodes, and actual rights-HOLD private input rejected in public mode.
- Eight source-derived SVGs were rasterized for visual review using the bundled
  image tool; titles, dates, axes and plotted source nodes were legible.
- Real public input and outputs generated successfully; exact41-file publication
  allowlist/heuristic scan PASS.
- Git normalizes text to LF; source values/timestamps are unchanged. Generated
  snapshots are not overwritten when appended.
- First CI found that Python3.10 rejects source timestamps with seven fractional
  second digits, while3.12/3.14 accepted them. The parser now normalizes only its
  internal comparison value to microseconds (the newer Python behavior), keeping
  original archived strings unchanged. Two regressions cover a strict old-parser
  stub and write/read preservation. Actual3.10 reruns passed on Linux and Windows.

## Delivery receipts

- [PR1](https://github.com/pengpengyi92/p-curve/pull/1) merged as
  `e2bcfd18bd2a50334b30583187e10d68be50c583` after all12checks succeeded
  (push+PR events, each Linux/Windows × Python3.10/3.12/3.14).
- Verified code head `4f18feb7083297675bccaf413a9c7b6f8c0f36e9`:
  [run43041490074](https://github.com/pengpengyi92/p-curve/actions/runs/43041490074)
  and [run43041477243](https://github.com/pengpengyi92/p-curve/actions/runs/43041477243)
  both SUCCESS. The initial failure is retained, not hidden or bypassed.
- Remote immutable archive subtree matches local Git tree
  `c771c3781fceacd4eac6d455b89eed615393ec65` exactly. Snapshot JSON/SVG values and
  original timestamp strings were not changed by the compatibility fix.
- This receipt-only follow-up uses the same workflow; the Actions page is the
  live source for its status. No PyPI upload or hosted/live-data deployment.

## Next action

Add each future collection under a fresh timestamp. Corrections link to the prior
snapshot rather than overwrite it. Continue source-rights review for excluded
markets; do not infer permission from a public webpage or open-source code.
