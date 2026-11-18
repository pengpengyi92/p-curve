# P-Curve: 2026 sovereign yield coverage

Compiled `2026-11-19T02:08:12+08:00` · Curated and visualized by pengyi.
This replaces the README figures from the [prior portfolio](../20261118T175156Z/);
the prior dated files remain unchanged. Candidate observations may be from any
published 2026 date. The selected observations range from 2026-04-14
to 2026-11-18; this is neither a full-year time series nor a common close.

[Additional curves and exact per-point receipts](config.json) ·
[Panel membership and reused inputs](portfolio.json) ·
[Python reproduction](../../../examples/global_sovereign_overlay/README.md#reproduce-the-regional-portfolio)

| Market | Coverage change and provenance |
| --- | --- |
| China | Add 1Y ([MOF 174](https://zwgls.mof.gov.cn/ywgg/202610/t20261014_4002819.htm), Oct 14, 1.16%), 2Y ([103](https://zwgls.mof.gov.cn/ywgg/202606/t20260624_3992217.htm), Jun 24, 1.21%), 5Y ([58](https://zwgls.mof.gov.cn/ywgg/202604/t20260414_3987577.htm), Apr 14, 1.50%) and 30Y ([184](https://zwgls.mof.gov.cn/ywgg/202610/t20261023_4003386.htm), Oct 23, 2.06%). Attributed rate-auction coupons; existing bill yields and reopening yield retain their conventions. No ChinaBond data. |
| Hong Kong SAR | Add the HKSAR Government/HKMA [5Y HKD reopening](https://www.info.gov.hk/gia/general/202608/12/P2026081200499p.htm), Aug 12, 3.270% annualized from the average accepted price. Four issuer facts with [source attribution](https://data.gov.hk/en/terms-and-conditions); no vendor yield bulletin. |
| South Korea | Add Ministry of Economy and Finance KTB auction award yields: 2Y Nov 2, 5Y Oct 26, 20Y Oct 27 and 30Y Nov 3. All official result URLs are in `point_observations.kr`. Seven numerical issuer facts only, not notice text or vendor data ([Article 7](https://www.copyright.or.kr/eng/laws-and-treaties/copyright-law/chapter02/section01.do)). |
| Canada | Replace the closing benchmark input with the [Bank of Canada's own fitted GoC zero curve](https://www.bankofcanada.ca/rates/interest-rates/bond-yield-curves/) for Oct 28, all 120 quarterly nodes, from 0.25 to 30 years. Values converted from decimals to annual percentages; new chart. [Bank of Canada terms](https://www.bankofcanada.ca/terms/). The prior benchmark table now carries joint CanDeal credit and was not reused. |
| Mexico | [Banco de México SIE CF114](https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadro&idCuadro=CF114), official **October monthly average** nominal CETES and fixed-rate Bonos, 28D through 30Y (9 source nodes). Oct 31 is the reporting-period end, not a trade date. No published 7Y or inflation-linked values used. Rates unchanged; [Banco de México terms](https://www.banxico.org.mx/footer-en/disclaimer-usage-policies-ban.html). |
| Brazil | Same Nov 17 [Tesouro Direto](https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3) morning quote field, adding fixed-rate coupon issues due Jan 1 of 2033, 2035 and 2037. The short nodes are non-coupon; the line is not a fixed-convention wholesale yield curve. Tenors are calendar days / 365.25. Extracted rates retain [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/), not the code license. |
| New Zealand | Add three accepted yields from NZ Treasury Debt Management [1012](https://debtmanagement.treasury.govt.nz/tender/nominal-bond-tender-1012) and [1014](https://debtmanagement.treasury.govt.nz/tender/nominal-bond-tender-1014) to the [1016](https://debtmanagement.treasury.govt.nz/tender/nominal-bond-tender-1016) set. Tenors are actual days from each settlement / 365.25. Rates unchanged; tenor mapped and chart redrawn, [Crown CC BY 4.0](https://debtmanagement.treasury.govt.nz/copyright-and-licensing). |

The US, UK, Australia, Japan, Singapore and both ECB curves reuse the original
frozen rows and [attributions](../20261118T175156Z/README.md). UK Database data are
under [OGL v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
Contains information from **Daily SGS Prices**, accessed 2026-11-19, Monetary
Authority of Singapore, made available under the [MAS Terms of Use of Datasets](https://www.mas.gov.sg/terms-of-use).
The ECB data remain the two fitted nominal continuous-zero euro-area curves.
The [IMF WEO classification](https://www.imf.org/-/media/files/publications/weo/2026/april/english/statsappendix.pdf)
still governs the advanced and emerging panels.

## How to read

The horizontal scale gives the short end more space, using the square root of
years. Its tick labels are actual maturities, but the drawn slope per pixel is
not a slope per year. The sidebar always shows an available observed rate and
its tenor, choosing 10Y if present or the nearest published tenor otherwise.
Check that tenor, the convention and the observation date before comparing.
No filling, extrapolation or tradeable cross-currency spread is implied.
