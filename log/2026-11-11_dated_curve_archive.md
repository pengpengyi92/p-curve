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

## Real-data cross-timezone replay — 2026-11-14T18:31:54+08:00

**Question.** Can two daily sovereign par-curve streams be replayed in UTC across the European and U.S. autumn clock changes while preserving source yields, local market dates, and the caller's timezone-aware inputs?

**Fixed sample.** 2026-10-23 through 2026-11-04, inclusive; 9 observations per source, at the published 2Y, 5Y and 10Y tenors, in percent. [U.S. Treasury daily nominal par curve](https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics/) ([October XML](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml?data=daily_treasury_yield_curve&field_tdr_date_value_month=202610), [November XML](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml?data=daily_treasury_yield_curve&field_tdr_date_value_month=202611); [CC0 source metadata](https://catalog.data.gov/dataset/interest-rate-statistics-daily-treasury-yield-curve-rates)) and [European Central Bank euro-area all-ratings par curve](https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_area_yield_curves/html/index.en.html) ([YC API CSV](https://data-api.ecb.europa.eu/service/data/YC/B.U2.EUR.4F.G_N_A.SV_C_YM.PY_2Y+PY_5Y+PY_10Y?startPeriod=2026-10-23&endPeriod=2026-11-04&format=csvdata), series `PY_2Y`, `PY_5Y`, `PY_10Y`; [ECB source/use conditions](https://www.ecb.europa.eu/services/using-our-site/disclaimer/html/index.en.html)). No interpolation, fill, revisions inferred, or combination of the two curves into one. Rates are real; timestamp transformations are ours. Raw downloads and replay code are not published here.

**Clock model.** Anchor ECB events at its scheduled noon release in `Europe/Berlin`; anchor UST events at the documented approximate 15:30 indicative quote observation in `America/New_York`, not a verified release time. Preserve the source market date independently of UTC and `Asia/Shanghai` dates. These are modeled daily events, not historical tick or data-availability timestamps.

| Local market date | ECB modeled UTC | UST modeled UTC |
| --- | --- | --- |
| 2026-10-23 | 10:00 | 19:30 |
| 2026-10-26 (after European DST change) | 11:00 | 19:30 |
| 2026-11-02 (after U.S. DST change) | 11:00 | 20:30 |

**Baseline → change → result.** Holding the first day's UTC offsets fixed misplaced 11 of 18 events by one hour (ECB 8, UST 3). Using IANA zones (tzdata 2026.6), Point72 CSP 0.19.0 replayed 18 distinct events in one merged UTC stream and preserved all 54 source values. All 9 UST events landed on the following date in Shanghai; a join on market date alone would attach a later modeled UST observation to all 9 same-day ECB events. This does not establish actual publication lag or prove a point-in-time trading backtest.

**CSP #794 cross-check.** With the same released native wheel and identical input, the baseline Python curve adapter rewrote all 18 timestamps in the caller's lists; the adapter at [Point72 CSP #794](https://github.com/Point72/csp/pull/794) rewrote zero. Both emitted the same event times and yields; 5 focused CSP tests passed on the PR source. No native rebuild or CI matrix was run locally. There was no public reviewer feedback; DCO passed separately, while the [build](https://github.com/Point72/csp/actions/runs/43573181608) and [Conda](https://github.com/Point72/csp/actions/runs/43573181708) workflows still required upstream action.

**Trade-off / next action.** This is an offline chronology check on one fixed window, not a new P-Curve dataset, runtime dependency, live ingestion feature, pricing result or alpha claim. Actual historical publication timestamps, revisions, and performance are `UNMEASURED`. For future point-in-time use, collect and audit publication/receipt timestamps separately before any cross-market join.
