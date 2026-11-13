# P-Curve — Benchmark Cards

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
