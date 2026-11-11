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

- Full local suite **47/47 PASS**:30math +4repository +10renderer +3actual-archive
  regression tests. No skipped tests. Fresh0.2.0 wheel install PASS.
- Independent source-to-output checks PASS: all selected source values unchanged,
 745 public nodes, and actual rights-HOLD private input rejected in public mode.
- Eight source-derived SVGs were rasterized for visual review using the bundled
  image tool; titles, dates, axes and plotted source nodes were legible.
- Real public input and outputs generated successfully; exact41-file publication
  allowlist/heuristic scan PASS. Remote CI/readback PENDING final delivery.
- Git normalizes text to LF; source values/timestamps are unchanged. Generated
  snapshots are not overwritten when appended.

## Next action

Add each future collection under a fresh timestamp. Corrections link to the prior
snapshot rather than overwrite it. Continue source-rights review for excluded
markets; do not infer permission from a public webpage or open-source code.
