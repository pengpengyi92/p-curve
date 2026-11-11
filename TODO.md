# Verifiable priorities

## P0 — initial public gate

- [x] Freeze selected-file manifest; review ownership, public precedents and all
  exported content; confirm no private Git history or market data.
- [x] Run the full offline suite and synthetic example in a clean environment.
- [x] Publish the approved subset to `pengpengyi92/p-curve`; verify public
  visibility, committed files and remote CI results.

## P1 — quality before breadth

- [x] Add offline immutable `curve/` archive, source-specific rights review and
  first selected dated snapshot with all native source points.
- [ ] Confirm v0.2.0 full tests, public allowlist and six-platform CI/readback.

- [x] Run Python3.10/3.12/3.14 tests on Linux and Windows; record results.
- [ ] Add independently sourced numerical reference fixtures only after their
  exact source/license and convention contracts are reviewed.
- [ ] Review first community curves and FICC recommendations through the issue
  templates; each proposed scope expansion must pass the publication gate.
- [ ] Consider a fully synthetic interactive HTML example after reproducibility
  and accessibility checks. It is not delivered in v0.1.0.

## HOLD — not initial publication scope

- Calibration, par bootstrap, calendar/day-count engines, empirical macro models,
  live market-data connectors, unreviewed real-data dashboards, multi-curve/CSA pricing, private
  strategies and production deployment. Each needs separate precedent, rights,
  disclosure, test and human approval; no automatic export from PFICC.
