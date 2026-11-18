# README now shows the November 18 target edition

- **Target market date:** 2026-11-18. **Compilation cutoff:**
  `2026-11-19T00:27:11+08:00`. This is not a common close or a PIT reconstruction.
- The [MAS Daily SGS Prices table](https://eservices.mas.gov.sg/statistics/fdanet/SgsBenchmarkIssuePrices.aspx)
  contains the actual 11-18 observation. The [Treasury table](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202611&type=daily_treasury_yield_curve)
  and [Japan MOF release list](https://www.mof.go.jp/english/public_relations/whats_new/202611.html)
  had verifiable 11-17 rows. RBA F2 was 11-11;
  [F2 has a weekly publication schedule](https://www.rba.gov.au/schedules-events/frequency-statistical-releases.html).
  No later dates were imputed. China and UK rights HOLD stays unchanged.
- [New README chart](../curve/20261118T162711Z/global_sovereign_yields.svg) and
  [frozen config](../curve/20261118T162711Z/config.json) use the same offline
  collector/drawer. All four public curves retain their original node values.
- [Original 11-19 chart](../curve/20261118T161713Z/global_sovereign_yields.svg)
  and [original config](../curve/20261118T161713Z/config.json) remain immutable.
  The archived SVG regenerated to identical SHA-256
  `a6add3e2e16fdb3f8425ac72ede997e1a154130f6e192deab9c806dfcb860894`.
- Windows 11 / Python 3.12.14: baseline 77 tests, updated suite 80 passed.
  Both SVGs regenerate via `python -m examples.global_sovereign_overlay.generate`
  with the respective config. New chart visually checked using isolated headless
  Chrome. No runtime dependency, network backend or package version changes.
