# Data rights and source review — 2026-11-11

MIT covers P-Curve code and our documentation, not an automatic relicensing of
upstream market data. The following is a bounded source-specific publication
review, not legal advice or a grant from the data owners. Future uses and source
changes need a new review. No upstream logos or institutional endorsement.

| Source / data | Decision | Conditions and evidence |
| --- | --- | --- |
| US Treasury daily nominal par curve | Approved selected public display | Official Treasury-published [Data.gov record](https://catalog.data.gov/dataset/interest-rate-statistics-daily-treasury-yield-curve-rates) identifies [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Source: US Treasury. Values unchanged; P-Curve generates the chart and tenor-year representation. |
| Japan MOF constant-maturity JGB data | Approved selected public display | [MOF notice](https://www.mof.go.jp/english/about_mof/notice/index.html) applies [PDL1.0](https://www.digital.go.jp/en/resources/open_data/public_data_license_v1.0) unless separately indicated. Source: Ministry of Finance Japan. P-Curve extracts the latest dated row and redraws the curve; no MOF endorsement. Preserve attribution, PDL link and adaptation notice. |
| ECB euro-area AAA / all-ratings spot curves | Approved accurate research display | [ECB copyright conditions](https://www.ecb.europa.eu/services/using-our-site/disclaimer/html/index.en.html) require accurate reproduction and ECB attribution, and explicit notice of modifications. Source: European Central Bank. Node values unchanged; charts/tenor mapping by P-Curve. This free repository is not a paid data subscription. [Curve-specific information](https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_area_yield_curves/html/index.en.html) is public information, not a pricing or investment recommendation. |
| ChinaBond CGB YTM key nodes | HOLD — not included in public archive | Accessible [official table](https://yield.chinabond.com.cn/cbweb-pbc-web/pbc/more?locale=en_US) does not by itself establish republication rights. [ChinaBond product-use notice](https://yield.chinabond.com.cn/cbweb-mn/yield_main?locale=en_US) requires additional review/permission for specified uses. No blanket derived-chart/data permission established. |
| HK Government Bond IBP/GSBP closing benchmarks | HOLD — not included in public archive | [HKGB copyright](https://www.hkgb.gov.hk/en/others/copyright.html) permits certain noncommercial original-format uses; that is not assumed to license our derived chart/JSON for a reusable public repository. Government ownership and external calculating-agent credits are retained in the private source review. |
| Bank of England nominal gilt curve ZIP | HOLD — not included in public archive | [BoE legal terms](https://www.bankofengland.co.uk/legal) distinguish internal/noncommercial website uses from public reuse. The separate Bank of England Database OGL terms are not automatically applied to the [yield-curve ZIP](https://www.bankofengland.co.uk/statistics/yield-curves). Workbook credits include external data providers. |

Only a small latest-date selected dataset is stored here, not the downloaded
historical CSVs, XLS/XLSX workbooks, ZIPs, an API mirror or raw cache. Source hashes,
retrieval times and representations appear in snapshot notes. The metadata
labels do not certify financial accuracy or grant rights beyond the sources.

## Grouped edition — 2026-11-14

- **Australia F2 nominal yields:** the four daily series in the edition identify
  the RBA alone in the CSV's source row. Public display is limited to those
  selected data and the derived chart, under [RBA terms, sections 3 and 5](https://www.rba.gov.au/copyright/).
  Source: Reserve Bank of Australia 2026. P-Curve drew the chart without
  changing yields. No RBA endorsement or use as a financial benchmark.
- U.S., Japan and ECB use the same source-specific conditions as above.
- ChinaBond and BoE remain **HOLD**. Hong Kong's source-only page does not
  republish the institutional fixings or y-t-m from the separate HKMA Exchange
  Fund proxy; that proxy has a third-party data credit and remains **HOLD**.

## Global overlay — 2026-11-19

- Same reviewed scopes for UST, Japan MOF and RBA F2, with independently
  dated rows. Source: Reserve Bank of Australia 2026. Unchanged yields, chart
  redrawn. Japan MOF data under [PDL 1.0](https://www.digital.go.jp/en/resources/open_data/public_data_license_v1.0).
- **MAS Daily SGS Prices:** bounded public display of the seven selected
  benchmark bond yield columns under the [MAS Terms of Use of Datasets](https://www.mas.gov.sg/terms-of-use).
  Source is MAS's published Closing Levels table; primary-dealer bid rates are
  the stated inputs. No separate dealer feed, price columns, raw download or
  MAS branding is redistributed. Preserve source/access-date attribution.
- **CGB and UK gilts:** retain HOLD, with public source links but neither
  values nor derived plot lines. A user's separately authorized personal copy
  stays outside the public tree, including all outputs from it.

## November 2026 six-market comparison

- **UK:** the three nominal-par series `IUDSNPY`, `IUDMNPY`, `IUDLNPY` are
  from the Bank of England Statistics Database, whose [own legal terms](https://www.bankofengland.co.uk/legal#bank-of-england-database)
  identify OGL for Database data unless otherwise stated. No series-specific
  rights exclusion was indicated for these three modeled series. Contains
  public sector information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
  The unrelated latest-curve spot workbook remains HOLD.
- **China:** the six plotted numerical facts are independently sourced from
  the [Ministry of Finance debt-management site](https://zwgls.mof.gov.cn/),
  whose footer requests attribution for republication. Only the rates/terms
  and dates needed to identify the points were extracted from ministry-authored
  announcements with per-point citations. The ChinaBond market curve remains
  HOLD and no ChinaBond numbers are included in the public SVG or config.
- See the [edition and source table](../examples/global_sovereign_overlay/README.md).
