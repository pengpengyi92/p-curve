# Open-source precedents and publication boundary

Reviewed: 2026-11-11. Machine-readable record:
[`data/open_source_precedents.json`](../data/open_source_precedents.json).

P-Curve is a **selected open-source part** of the proprietary PFICC / P-Curve
research program, not a mirror or a promise to publish that program in full.
This register records credible public precedents for the **topics** in the first
public scope. It is a bounded primary-source review, not a survey of every FICC
repository, a ranking, or proof of novelty/frontier status.

## Publication rule

An already-public, openly licensed implementation of a substantially similar
topic is a **necessary but not sufficient** publication gate. If we cannot find
and verify one, that topic stays **HOLD** and is not exported from private work.
Public precedent does not oblige us to publish everything in the same category.

Each export also needs owner approval, an explicit file allowlist, code and data
rights review, privacy review, accurate scope/convention notes, and reproducible
tests. Another repository's license does **not** grant rights to private PFICC
code or data. Do not copy third-party code, fixtures, or data merely because a
topic appears here. Any future reuse needs a separate compatibility/attribution
review. The first release does not vendor these projects or require them at
runtime.

## Reviewed primary sources

All links below are pinned to the reviewed commit; a current default branch may
have changed after this review. License descriptions are evidence inventory,
not a legal assurance or an endorsement by the upstream projects.

| Project / reviewed commit | Observed public implementation | License evidence | Relevance and limit |
| --- | --- | --- | --- |
| [nelson_siegel_svensson](https://github.com/luphord/nelson_siegel_svensson/tree/0cc9aea682e3e007d6cf08e028e07e7ca5157ed6) · `0cc9aea` | [`ns.py`](https://github.com/luphord/nelson_siegel_svensson/blob/0cc9aea682e3e007d6cf08e028e07e7ca5157ed6/nelson_siegel_svensson/ns.py), [`nss.py`](https://github.com/luphord/nelson_siegel_svensson/blob/0cc9aea682e3e007d6cf08e028e07e7ca5157ed6/nelson_siegel_svensson/nss.py) | [MIT](https://github.com/luphord/nelson_siegel_svensson/blob/0cc9aea682e3e007d6cf08e028e07e7ca5157ed6/LICENSE) | Given-parameter Nelson–Siegel / Svensson curve evaluation is already public. P-Curve's small evaluator is not an adoption of its calibration routines or a claim that calibration always converges. |
| [QuantLib](https://github.com/lballabio/QuantLib/tree/cf74c9f657150750dfbf00ed6fd4c0768bc5ce36) · `cf74c9f` | [`YieldTermStructure`](https://github.com/lballabio/QuantLib/blob/cf74c9f657150750dfbf00ed6fd4c0768bc5ce36/ql/termstructures/yieldtermstructure.cpp), [`BondFunctions`](https://github.com/lballabio/QuantLib/blob/cf74c9f657150750dfbf00ed6fd4c0768bc5ce36/ql/pricingengines/bond/bondfunctions.cpp) | [QuantLib BSD-style three-condition license text](https://github.com/lballabio/QuantLib/blob/cf74c9f657150750dfbf00ed6fd4c0768bc5ce36/LICENSE.TXT); GitHub reports `NOASSERTION`, so no exact SPDX identifier is asserted here | Discount factors, period forwards, discounted cash flows and bond basis-point risk are public subjects. QuantLib supports materially more dates, instruments and conventions; its bond BPS/BPV definitions must not be silently equated with P-Curve's zero-node bump DV01. |
| [FinancePy](https://github.com/domokane/FinancePy/tree/0b0dc17ab3bcdaa0a21ae73b734f2641c9e5cf41) · `0b0dc17` | [`Bond.dv01`, `key_rate_durations_zero_tent`, `key_rate_durations`](https://github.com/domokane/FinancePy/blob/0b0dc17ab3bcdaa0a21ae73b734f2641c9e5cf41/financepy/products/bonds/bond.py) | [GPL v3 text](https://github.com/domokane/FinancePy/blob/0b0dc17ab3bcdaa0a21ae73b734f2641c9e5cf41/LICENSE), explicitly [`GPL-3.0-or-later` in project metadata](https://github.com/domokane/FinancePy/blob/0b0dc17ab3bcdaa0a21ae73b734f2641c9e5cf41/pyproject.toml#L14) | Parallel yield bumps and key-rate zero-curve risk have openly licensed precedents. Key-rate **duration**, currency DV01, zero-node risk and par-curve risk have different units/conventions. No FinancePy code is copied, vendored, or imported by this release. |
| [Strata](https://github.com/tradingtechnologies/Strata/tree/171b1c3c9347e36534f014779064b1ff1bc19216) · `171b1c3` | [`ZeroRateDiscountFactors`](https://github.com/tradingtechnologies/Strata/blob/171b1c3c9347e36534f014779064b1ff1bc19216/modules/pricer/src/main/java/com/opengamma/strata/pricer/ZeroRateDiscountFactors.java), [`LinearCurveInterpolator`](https://github.com/tradingtechnologies/Strata/blob/171b1c3c9347e36534f014779064b1ff1bc19216/modules/market/src/main/java/com/opengamma/strata/market/curve/interpolator/LinearCurveInterpolator.java), [`DiscountingPaymentPricer`](https://github.com/tradingtechnologies/Strata/blob/171b1c3c9347e36534f014779064b1ff1bc19216/modules/pricer/src/main/java/com/opengamma/strata/pricer/DiscountingPaymentPricer.java) | [Apache-2.0](https://github.com/tradingtechnologies/Strata/blob/171b1c3c9347e36534f014779064b1ff1bc19216/LICENSE.txt) | Continuous-zero discounting, interpolation, payment PV and parameter sensitivities are public. This is not evidence that P-Curve reproduces Strata's calendars, day counts, curve calibration or analytic sensitivities. |

## First-scope gate mapping

| Public topic | Verified topic precedents | Gate result / limits |
| --- | --- | --- |
| Given-parameter NS/NSS | nelson_siegel_svensson | `PRECEDENT_FOUND`; no calibration or parameter-estimation claim |
| Continuous-zero DF and period forward | Strata; QuantLib | `PRECEDENT_FOUND`; explicit year fractions and continuous compounding only in this public scope |
| Linear zero interpolation | Strata | `PRECEDENT_FOUND`; interpolation variable and extrapolation policy must be documented independently |
| Deterministic fixed-cash-flow PV | Strata; QuantLib | `PRECEDENT_FOUND`; not a complete bond schedule/settlement pricer |
| Parallel DV01 | FinancePy; QuantLib (related bond risk) | `PRECEDENT_FOUND`; bump variable, sign and units must remain explicit |
| Key-rate zero-node DV01 | FinancePy; Strata (parameter-risk precedent) | `PRECEDENT_FOUND`; not identical to every upstream KRD/PV01 definition |

`PRECEDENT_FOUND` clears only the same-topic-public-evidence gate. It is not
`APPROVED_FOR_EXPORT`, numerical validation, or permission to copy upstream code.

## What has and has not been tested

- Review performed: canonical repository identity/default branch, current commit,
  pinned license text/metadata, and the implementation paths listed above.
- No upstream packages installed or executed for this register; no code copied.
- Cross-library accuracy, performance, relative feature quality and production
  suitability: **UNMEASURED**. No baseline benchmark result is claimed.
- P-Curve's ambition is frontier-oriented, useful, reproducible FICC research.
  A specific novelty, superiority or state-of-the-art claim requires a falsifiable
  question, fixed benchmark, competing baselines, measured results and limitations.

## Future review / contribution queue

Readers are welcome to recommend their curves, openly licensed implementations,
FICC repositories, counterexamples and test fixtures. Use the repository's issue
templates and contribution guide. A useful recommendation includes canonical URL,
license, implementation path, conventions, reproducible example and limitations.

New topics (for example bootstrapping, collateral-aware multi-curve pricing, FX
curve coupling or volatility surfaces) start **UNREVIEWED / HOLD** here. This is
not a statement about what private PFICC contains. Find and review credible public
precedents, then review rights, scope and tests before any public implementation
is accepted. A lack of a match in this four-project register is not proof that no
public implementation exists.

Refresh triggers: a contribution proposes a new topic, a license or canonical
repository changes, or a measured comparison is planned. Preserve reviewed SHAs
and add a dated revision rather than quietly rewriting the historical evidence.

## 2026-11-11 extension: dated sovereign curve archive

[OpenBB](https://github.com/openbq-org/OpenBB/tree/11290d8b468570cea64b5feb0225ad9cbf5228e0)
provides [ECB dated curve handling](https://github.com/openbq-org/OpenBB/blob/11290d8b468570cea64b5feb0225ad9cbf5228e0/openbb_platform/providers/ecb/openbb_ecb/models/yield_curve.py)
and [Federal Reserve maturity/date observations](https://github.com/openbq-org/OpenBB/blob/11290d8b468570cea64b5feb0225ad9cbf5228e0/openbb_platform/providers/federal_reserve/openbb_federal_reserve/models/yield_curve.py).
The pinned root [LICENSE](https://github.com/openbq-org/OpenBB/blob/11290d8b468570cea64b5feb0225ad9cbf5228e0/LICENSE)
explicitly specifies Apache-2.0 (GitHub SPDX metadata itself is NOASSERTION).
This clears the same-topic precedent gate for sourced dated-curve records, not
rights to market data. P-Curve's offline renderer is original; no OpenBB code,
dependencies, fixtures or data are imported. Source-by-source display decisions
remain separate and are recorded in the archive DATA_LICENSES document.
