# P-Curve 0.1.0 — Benchmark Card

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
