# P-Curve regional sovereign portfolio

Edition `20261118T175156Z` · Compiled `2026-11-19T01:51:56+08:00` · Curated and visualized by pengyi.
Actual observations in the plots span 2026-10-21 to 2026-11-18.
This is a historical display example, not a live feed or a single market close.

[Portfolio groups and upstream editions](portfolio.json) · [Additional normalized nodes](config.json) ·
[Reproduce](../../../examples/global_sovereign_overlay/README.md#reproduce-the-regional-portfolio)

| Series | Observation date | Measure, source and public-display basis |
| --- | --- | --- |
| United States (USD) | 2026-11-17 | [US Treasury](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve) constant-maturity par yields; [CC0 catalogue record](https://catalog.data.gov/dataset/interest-rate-statistics-daily-treasury-yield-curve-rates). |
| Canada (CAD) | 2026-11-16 | [Bank of Canada](https://www.bankofcanada.ca/rates/interest-rates/canadian-bonds/) mid-market closing YTM for nominal benchmark issues, 2/3/5/7/10Y; omitted the long-term category, which has no fixed tenor. [Terms](https://www.bankofcanada.ca/terms/). |
| United Kingdom (GBP) | 2026-11-16 | Bank of England Database IUDSNPY / IUDMNPY / IUDLNPY at 5/10/20Y. Contains public sector information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). |
| Australia (AUD) | 2026-11-11 (published 11-13) | RBA F2 nominal interpolated yields. [Original config and terms](../../20261118T172919Z/config.json). |
| Japan (JPY) | 2026-11-17 | Japan MOF constant-maturity JGB yields. [Original config and terms](../../20261118T172919Z/config.json). |
| Hong Kong SAR (HKD) | 2026-10-21 and 2026-11-11 | HKSAR Government/HKMA institutional Government Bond tenders: [3Y](https://www.info.gov.hk/gia/general/202610/21/P2026102100512p.htm) and [10Y](https://www.info.gov.hk/gia/general/202610/21/P2026102100513p.htm) on Oct 21; [7Y](https://www.info.gov.hk/gia/general/202611/11/P2026111100497p.htm) on Nov 11. Yield implied by average accepted price at published issue tenor; [official press feed](https://data.gov.hk/en-data/dataset/hk-isd-gnmis-gnmis) and [attribution terms](https://data.gov.hk/en/terms-and-conditions). No Reuters bulletin data. |
| Singapore (SGD) | 2026-11-18 | SGS nominal benchmark issue bid-side yields. Contains information from **Daily SGS Prices**, accessed 2026-11-19, © Monetary Authority of Singapore as made available under the [MAS Terms of Use of Datasets](https://www.mas.gov.sg/terms-of-use). |
| South Korea (KRW) | 2026-11-09, 11-13 and 11-16 | Ministry of Economy and Finance KTB reopening [3Y](https://mofe.go.kr/st/fnancstats/detailTbFnancstatsView.do?bbsId=MOSFBBS_000000000049&menuNo=6050300&searchSn=MOSF_000000000079902), [50Y](https://mofe.go.kr/st/fnancstats/detailTbFnancstatsView.do?bbsId=MOSFBBS_000000000049&menuNo=6050300&searchSn=MOSF_000000000079954) and [10Y](https://mofe.go.kr/st/fnancstats/detailTbFnancstatsView.do?bbsId=MOSFBBS_000000000049&menuNo=6050300&searchSn=MOSF_000000000079970) awards at published issue tenors. Weighted-average award yields for 3/10Y, stated award yield for 50Y. Three attributed numerical facts only ([Korean Copyright Act, Article 7](https://www.copyright.or.kr/eng/laws-and-treaties/copyright-law/chapter02/section01.do)); no notice text or third-party data. |
| China (CNY) | 2026-11-06 to 11-18 | China MOF nominal primary bill yields, auction-set coupons and reopening yield. [Per-tenor notices and convention](../../../examples/global_sovereign_overlay/README.md#cgb-primary-market-points). No ChinaBond curve. |
| Mexico (MXN) | 2026-11-17 | [Banco de México](https://www.banxico.org.mx/tipcamb/llenarTasasInteresAction.do?idioma=sp) CETES and nominal fixed-rate Bono auction yields; CETES days/365, 3Y published bucket. [Usage policy](https://www.banxico.org.mx/footer-en/disclaimer-usage-policies-ban.html). |
| Brazil (BRL) | 2026-11-17 | [Tesouro Nacional, Treasury Direct](https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3), Tesouro Prefixado non-coupon, `Taxa Compra Manha`, mornings; maturity mapped from reference date as days/365.25. Retail posted quotes, not wholesale bonds. Extraction remains under [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/), outside the code license. |
| Euro area (EUR), AAA and all-rated issuers | 2026-11-12 | [ECB](https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_area_yield_curves/html/index.en.html) fitted nominal spot rates with continuous compounding. Full 3M–30Y monthly nodes. [ECB terms](https://www.ecb.europa.eu/services/using-our-site/disclaimer/html/index.en.html); source rates unchanged, tenor mapping and chart added. |
| New Zealand (NZD) | 2026-11-05 | [New Zealand Debt Management, Treasury](https://debtmanagement.treasury.govt.nz/tender/nominal-bond-tender-1016), weighted-average accepted nominal yields from tender 1016. Maturities measured from the 2026-11-10 settlement as days/365.25. [Crown CC BY 4.0](https://debtmanagement.treasury.govt.nz/copyright-and-licensing); tenors mapped and chart redrawn. |

The [IMF WEO statistical appendix](https://www.imf.org/-/media/files/publications/weo/2026/april/english/statsappendix.pdf)
places Hong Kong SAR, Singapore, Japan and South Korea among the advanced
economies, and China, Mexico and Brazil among the emerging and developing
economies. Geography cuts across those groups. The UK and ECB series
illustrate Europe, not a claim to cover every European country.

The maturity axis preserves all included source points. Some x-values are
published benchmark buckets rather than a security's exact remaining life.
The sidebar shows 10Y only where an exact 10Y point is present, never an
interpolated number. Compare shapes and levels with the rate types and dates
next to each plot; cross-currency levels are not total returns or trading
signals. No endorsement or change to the source values is implied.
