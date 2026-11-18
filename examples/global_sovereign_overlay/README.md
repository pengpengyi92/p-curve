# Global sovereign yield overlay

| Edition | Chart and config | Timing |
| --- | --- | --- |
| November 2026 six-market view (README default) | [Chart](../../curve/20261118T172919Z/global_sovereign_yields.svg) · [Config](../../curve/20261118T172919Z/config.json) | Compiled `2026-11-19T01:29:19+08:00`; five curves plus dated CGB auction points. |
| 2026-11-18 target (archive) | [Chart](../../curve/20261118T162711Z/global_sovereign_yields.svg) · [Config](../../curve/20261118T162711Z/config.json) | Compiled `2026-11-19T00:27:11+08:00`; only Singapore is a verified Nov 18 public observation. Earlier curves are labeled references. |
| 2026-11-19 snapshot (archive) | [Chart](../../curve/20261118T161713Z/global_sovereign_yields.svg) · [Config](../../curve/20261118T161713Z/config.json) | Original cutoff `2026-11-19T00:17:13+08:00`, original bytes retained; no Nov 19 market observation. |

The markets did not share a close. See the [source and rights review](../../curve/DATA_LICENSES.md).

## Reproduce

Python 3.10+, standard library only. Run from the repository root:

```sh
python -m examples.global_sovereign_overlay.generate
```

[DataCollector](data_collector.py) reads the JSON and validates its dates,
identifiers, units, nodes and public-display status; it performs **no network
calls**. It accepts an optional `target_market_date` distinct from compilation
time, and rejects observations later than the target. [Drawer](drawer.py)
labels earlier observations as references and draws one SVG. When the config
provides `point_observations`, each plotted tenor in that market requires a
date and source URL and is drawn without a connecting line. The drawer
reuses existing bytes on an exact rerun and will not overwrite a differing
chart. A new observation belongs in a new dated config and file.

To rerender the archived edition byte-for-byte into an unused local path:

```sh
python -m examples.global_sovereign_overlay.generate --config curve/20261118T161713Z/config.json --output build/archive-20261119.svg
```

For a lawful personal research file under the ignored `build/` directory:

```sh
python -m examples.global_sovereign_overlay.generate --local --config build/config.local.json --output build/global-sovereign.local.svg
```

Public mode rejects HOLD values even if supplied. Local-only data and chart
outputs must not enter the release. This gate checks existing rights labels;
it does not grant any rights or authorize reclassifying a source.

## Market observations

| Market | Verified observation date | Representation | Public points |
| --- | --- | --- | ---: |
| US Treasury | 2026-11-17 | USD nominal CMT par yields | 14 |
| Japan | 2026-11-17 | JPY MOF constant-maturity JGB yields | 15 |
| Australia | 2026-11-11 | AUD RBA F2 interpolated nominal yields, published 11-13 | 4 |
| Singapore | 2026-11-18 | SGD SGS nominal benchmark issue bid-side bond yields | 7 |
| China | 2026-11-06 to 2026-11-18 | CNY MOF primary auction rates, distinct observations | 6 |
| UK | 2026-11-16 | GBP BoE Database nominal par | 3 |

Singapore uses published benchmark maturity buckets, not the exact remaining
lives of those issues. Singapore Treasury-bill and Australian indexed-bond series are
outside this comparison. The Australian file ends at 10Y; nothing extends
that line beyond 10Y. The markers are observed/published nodes; the lines
only join them. No missing value is replaced or treated as zero.

**Example reading:** on 2026-11-17, US 2s10s was +30.0 bp, while JGB 2s10s was
+104.7 bp. Japan's 10Y yield was lower even though that portion of its curve
was steeper. The sources and conventions differ, so neither a level gap nor a
shape difference is an executable cross-market spread, a cause, or a hedge.

## CGB primary-market points

Source: Ministry of Finance of China. These six numerical observations
are independent of the ChinaBond curve. They span different auction dates
and instruments; do not fit them as a closing yield curve.

| Point | Auction date | Annual % | Published measure / source |
| --- | --- | ---: | --- |
| 91 days | 2026-11-18 | 1.11 | Bill issue yield ([notice 199](https://zwgls.mof.gov.cn/ywgg/202611/t20261118_4004935.htm)) |
| 182 days | 2026-11-18 | 1.12 | Bill issue yield ([notice 198](https://zwgls.mof.gov.cn/ywgg/202611/t20261118_4004932.htm)) |
| 3Y | 2026-11-13 | 1.22 | New-issue auction-set coupon ([notice 194](https://zwgls.mof.gov.cn/ywgg/202611/t20261113_4004659.htm)) |
| 7Y | 2026-11-18 | 1.40 | Special sovereign issue auction-set coupon ([notice 197](https://zwgls.mof.gov.cn/ywgg/202611/t20261118_4004931.htm)) |
| 10Y | 2026-11-13 | 1.56 | New-issue auction-set coupon ([notice 195](https://zwgls.mof.gov.cn/ywgg/202611/t20261113_4004660.htm)) |
| 49Y remaining | 2026-11-06 | 2.15 | Reopening yield of original 50Y issue ([notice 190](https://zwgls.mof.gov.cn/ywgg/202611/t20261106_4004206.htm)) |

Under the [MOF auction rules](https://yn.mof.gov.cn/tongzhitonggao/202206/t20220623_3820920.htm),
the displayed coupons from these rate-based auctions are the rounded
weighted winning rates. They do not report every allotment yield or an
observed secondary-market yield. The bill x-coordinates are days/365.

## Attribution

UK: Bank of England Statistics Database, IUDSNPY / IUDMNPY / IUDLNPY (5Y /
10Y / 20Y); contains public sector information licensed under the
[Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
No values from the BoE latest-curve workbook were used.

Contains information from **Daily SGS Prices**, accessed on 2026-11-19 from
the **Monetary Authority of Singapore**, made available under the
[MAS Terms of Use of Datasets](https://www.mas.gov.sg/terms-of-use).
No endorsement. Source yields are unchanged.
