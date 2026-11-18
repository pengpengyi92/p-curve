# Global sovereign yield overlay

**Snapshot cutoff:** `2026-11-19T00:17:13+08:00`, or `2026-11-18T16:17:13Z`.
The cutoff dates the example. The markets did not share a close, and these are
not November 19 end-of-day observations or intraday prices.

- [Frozen public config](../../curve/20261118T161713Z/config.json)
- [Single shared-axis chart](../../curve/20261118T161713Z/global_sovereign_yields.svg)
- [Source and rights review](../../curve/DATA_LICENSES.md)

## Reproduce

Python 3.10+, standard library only. Run from the repository root:

```sh
python -m examples.global_sovereign_overlay.generate
```

[DataCollector](data_collector.py) reads the JSON and validates its dates,
identifiers, units, nodes and public-display status; it performs **no network
calls**. [Drawer](drawer.py) consumes that snapshot and draws one SVG. It
reuses existing bytes on an exact rerun and will not overwrite a differing
chart. A new observation belongs in a new dated config and file.

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
| China | 2026-11-18 checked locally | CNY ChinaBond government nominal YTM | HOLD |
| UK | 2026-11-17 checked locally | GBP BoE nominal gilt spot yields | HOLD |

Singapore uses published benchmark maturity buckets, not the exact remaining
lives of those issues. Treasury-bill and Australian indexed-bond series are
outside this comparison. The Australian file ends at 10Y; nothing extends
that line beyond 10Y. The markers are observed/published nodes; the lines
only join them. No missing value is replaced or treated as zero.

**Example reading:** on 2026-11-17, US 2s10s was +30.0 bp, while JGB 2s10s was
+104.7 bp. Japan's 10Y yield was lower even though that portion of its curve
was steeper. The sources and conventions differ, so neither a level gap nor a
shape difference is an executable cross-market spread, a cause, or a hedge.

Contains information from **Daily SGS Prices**, accessed on 2026-11-19 from
the **Monetary Authority of Singapore**, made available under the
[MAS Terms of Use of Datasets](https://www.mas.gov.sg/terms-of-use).
No endorsement. Source yields are unchanged.
