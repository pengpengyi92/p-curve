# Global sovereign yield curves: developed and emerging markets

**Generated:** `2026-11-14T15:52:32+00:00` (23:52:32 Asia/Shanghai). **Author:** pengyi.

[Developed index](../curve/developed/20261114T155232Z/index.html) ·
[Emerging index](../curve/emerging/20261114T155232Z/index.html) ·
[Share a curve or finding](https://github.com/pengpengyi92/p-curve/discussions/7).

| Geography | Latest usable date in the input | Representation | Public |
| --- | --- | --- | --- |
| U.S. | 2026-11-13 | U.S. Treasury nominal par | 14 nodes |
| Japan | 2026-11-12 | MOF constant-maturity yields, semiannual | 15 nodes |
| Euro area | 2026-11-12 | ECB fitted continuous-zero spot, AAA and all ratings | 358 + 358 nodes |
| Australia | 2026-11-11 | RBA F2 nominal 2Y, 3Y, 5Y and 10Y | 4 nodes |
| U.K. | 2026-11-12 | BoE nominal gilt spot | Source only |
| Hong Kong SAR | 2026-11-13 (proxy) | HKMA Exchange Fund Bills & Notes, not a government-bond fixing | Source only |
| Mainland China | 2026-11-13 | ChinaBond fitted CGB yield to maturity | Source only |

Classification follows the [IMF WEO statistical appendix](https://www.imf.org/-/media/files/publications/weo/2026/april/english/statsappendix.pdf):
Hong Kong SAR is counted separately as advanced; mainland China is in emerging
and developing economies. ECB data represent euro-area issuer groups, not one
country or all of Europe. Observation dates are local market labels, not the
generation timestamp or a synchronized close.

The charts show meaningful differences in shape without mixing rates into one
pricing curve. The Treasury curve is higher at 20 years than at 30 years; the
Australian observations dip from 2 years to 3 years before rising to 10 years.
The two euro-area series use different issuer populations even though both use
the same fitted spot convention. None of these differences constitutes a
tradable spread. Source values are unchanged; connecting lines are visual guides.

The public export contains only the reviewed SVG/HTML and metadata (no raw
responses, sources on HOLD, or local PNGs). See the
[source terms](../curve/DATA_LICENSES.md). This edition does not change the
package version or older snapshots.
