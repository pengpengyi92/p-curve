# P-Curve — Benchmark Cards

## Six-market November edition — 2026-11-19

- **Baseline:** four curves; CGB and UK source-only.
- **Change:** exact UK Database nominal par series and six China MOF auction
  observations with per-node dates. Preserve the original rights holds.
- **Measure:** 49 public plotted values; validate auction marker separation,
  source data, older SVG byte equality and the README asset reference.
- **Result:** 83 local tests passed, and six markets visible on the new SVG.
- **Trade-off:** CGB points are not a daily secondary-market curve; rate
  conventions and observation dates are not homogeneous.
- **Next Action:** identify a redistributable CGB daily secondary series.

## Global sovereign overlay — 2026-11-19

- **Baseline:** dated sovereign pages with separate single-market charts.
- **Change:** a config-backed collector and one SVG with shared maturity and
  yield scales, source observation labels, and fail-closed public rendering.
- **Measure:** fixed 2026-11-19 config; four approved curves, 40 nodes. Recheck
  source dates, 10Y values, 2s10s, exact output bytes and HOLD rejection.
- **Result:** 77 local tests passed; UST 2s10s +30.0 bp and JGB +104.7 bp
  on 11-17. No live feed, forecasting or economic validity claim.
- **Trade-off:** different observation dates and quote conventions; RBA F2
  ends at 10Y and the source file was older. CGB/UK are source-only on README.
- **Next Action:** implement one official daily adapter with fixtures and
  rights evidence ([Issue #10](https://github.com/pengpengyi92/p-curve/issues/10)).

## Grouped sovereign archive — 2026-11-14

- **Baseline:** four rights-reviewed public series in a flat dated archive.
- **Change:** index new immutable editions by market group and geography; add RBA
  F2 and keep source-only pages distinct from plotted data.
- **Measure:** source-date/node checks, internal HTML links, SVG-node counts,
  HOLD exclusions and exact publication allowlist.
- **Result:** five public series, 749 source nodes; no synthetic fills. Pricing
  accuracy, investment value and adoption remain **UNMEASURED**.
- **Trade-off:** different observation dates and quote conventions; do not treat
  plots as compatible zero curves. Public art is text-based SVG.
- **Next Action:** resolve the exact HKGB observation and outstanding source rights
  before exporting any additional series.

## Visualization reference route — 2026-11-14

- **Baseline**:independent curve renderer and public archive; no visualization repo reading route.
- **Change**:12 fixed public source references with FICC tenor/unit/type/rights checks, manual license notes and4 metadata/link tests. No private PFICC files, new financial models or immutable snapshots changed.
- **Measure**:full offline suite, synthetic example and explicit publication manifest; actual results in log/2026-11-14_data-visualization.md. External renderers NOT_RUN.
- **Result**:source/reading references only; renderer speed, financial validity and research gains UNMEASURED.
- **Trade-off**:open code is not a data license or export approval; AGPL/NOTICE/manual unknown-SPDX boundaries retained. No new runtime dependencies.
- **Next Action**:complete source/privacy/CI review and push; separately test an approved renderer without expanding curve/calibration/live-data scope.

## Community update — 2026-11-14

- **Baseline:** public math library and immutable curve archive; no five-track contribution index.
- **Change:** introduce a public research statement, agent onboarding and five linked submission tracks without widening the implementation or data allowlists.
- **Measure:** offline suite, synthetic example, exact publication inventory and public Issue/Discussion readback.
- **Result:** 64 local tests, synthetic example and publication check passed; five public discussion threads and [Issue #8](https://github.com/pengpengyi92/p-curve/issues/8) created. Existing source, snapshots and package version unchanged.
- **Trade-off:** discussion is open, but publication still requires rights and maintainer review; three threads remain in General. Adoption and research performance are **UNMEASURED**.
- **Next Action:** review the first contributed curve and finish organizing discussion categories.

Follow-up: all five dedicated categories are live. The original three threads moved in place; no duplicate posts were created.

## Baseline

No standalone public P-Curve package. Selected owner-controlled mathematical
utilities existed inside proprietary PFICC, but public users could not reproduce
them independently. This is an extraction/quality baseline, not an upstream
performance comparison.

## Change

Publish only established-topic pure math, explicit continuous-zero/year-fraction
contracts, synthetic fixtures, independent oracles and offline tests. Remove
private research, macro/event fixtures, data, filesystem/network assumptions and
private repository metadata. Document reviewed public precedents as references.

## Measure

Full unittest suite, synthetic example, standalone packaging, supported Python/OS
CI, exact staged-file disclosure review, and remote readback. Measurements and
release receipts are recorded in `log/2026-11-11_initial_public_release.md`.

## Result

Independent fresh-environment install, **34/34 tests** (30 math +4 repository
contracts), the synthetic example, dependency check and exact28-file publication
check PASS on Python3.12.14. An unapproved-file negative probe was correctly
rejected. Initial code commit passed all six Linux/Windows remote jobs on
Python3.10/3.12/3.14; see the linked run in the delivery log. No claim is inferred from the
private project's tests. Performance vs QuantLib/FinancePy/NSS, calibration
accuracy, empirical forecasts, PIT/OOS alpha, economic benefit, user adoption and
production readiness: **UNMEASURED / NOT_RUN**.

## Trade-off

Standard-library-only and synthetic-default makes the boundary easy to inspect,
but omits calibration, calendars/day-count, live data, multi-curve, credit and
execution. KRD is interpolation-dependent; finite differences are approximations.
These are established formulas, not a novel curve model or SOTA claim.

## Next Action

Complete the exact public gate and CI; then prioritize independent numerical
oracles and community-reviewed bugs before adding features. New topics remain on
HOLD until their separate publication review passes.

## 0.2.0 — Timestamped sovereign archives

- **Baseline:** no dedicated immutable curve archive or source-specific public
  data gate; mathematical core only.
- **Change:** offline SVG/HTML/JSON renderer, explicit source/market/retrieval
  clocks, append-only writes, per-source data terms and745 selected native nodes.
- **Measure:** synthetic renderer tests, actual-data date/grid/SVG regressions,
  source-to-output equality, rights HOLD rejection, full package checks and CI.
- **Result:**49/49 local tests PASS; independent0.2.0 install PASS;745 public nodes
  exactly match reviewed source extractions. All8 private-side SVG layouts
  visually inspected; no raw downloads or excluded-market figures exported.
  Public PR passed12checks across both event types; actual Linux/Windows3.10,
 3.12and3.14 all PASS. Remote immutable archive subtree readback MATCH.
- **Trade-off:** asynchronous source dates, par/YTM/spot differences, missing
  native tenors and selected publication rights constrain comparisons. These
  archives do not establish pricing accuracy, PIT, live feeds or financial value.
- **Next Action:** append future snapshots with
  reviewed sources and new timestamps. Financial accuracy vs independent vendor,
  alpha, profitability and production readiness remain UNMEASURED / NOT_RUN.

## 0.2.1 — One-click author-attributed overview

- **Baseline:** GitHub HTML links show source; the frozen local overview has no
  author/editorial presentation and lacks a stable local entry.
- **Change:** stable current portal, online/source/local entry links, portable
  launcher, pengyi curation credit and clearly subjective aesthetic comments.
- **Measure:** author/link/source/data/rights/immutability contracts, full offline
  tests, public CI, Pages deployment and actual browser rendering.
- **Result:**64/64 offline tests PASS; frozen snapshot subtree unchanged.
  Local file-browser automation blocked by tool policy, not bypassed. All12PR
  checks and6main checks PASS; Pages built, HTTP200/HTML, author and4figure
  checks PASS. Actual README click and browser visual review PASS.
- **Trade-off:** private8curve portal stays local; public4curve portal may be
  hosted. Aesthetic comments add no empirical or pricing evidence. Current page
  can evolve while historical snapshots remain immutable.
- **Next Action:** preserve selected public deployment and both Git syncs. New
  collection events still need new dated source/rights reviews and timestamps.

## Regional sovereign portfolio — 2026-11-19

- **Baseline:** one six-market README chart; 83 offline tests.
- **Change:** six regional/classification panels from three frozen inputs,
  using the existing `DataCollector` and `Drawer`.
- **Measure:** geography coverage, dates and rights, selected source values,
  preserved native node counts, auction markers, six byte-exact replays and
  all three prior overlay replays; desktop SVG render check.
- **Result:** 88 local tests pass; 14 distinct series and 789 native observations
  represented. All six panels rendered in an isolated Chromium profile.
- **Trade-off:** published local-currency conventions and market dates differ;
  auction diamonds and retail quotes cannot substitute for secondary closes.
- **Next Action:** obtain permission for comparable secondary-market sources
  before adding a common-date comparison. Trading usefulness: **UNMEASURED**.

## Expanded 2026 coverage — 2026-11-19

- **Baseline:** 789 distinct source nodes; three markets had no exact 10Y
  point in the fixed sidebar; charts had a linear maturity axis.
- **Change:** select from 2026, add native tenors, show actual sidebar tenors
  and spread the short end visually while retaining the full maturity range.
- **Measure:** source anchors, unique node counts, seven README embeds, all
  sidebar rates present, old and new byte-exact replay and Chrome rendering.
- **Result:** 923 distinct nodes across the same 14 series; all 90 local tests
  pass. Older SVG files are unchanged.
- **Trade-off:** yield and date conventions remain heterogeneous; the scale
  does not preserve slope per pixel. Calendar/trading comparability is **UNMEASURED**.
- **Next Action:** pursue rights-reviewed same-day secondary-market coverage.
