# Timestamped sovereign curve archive

Each directory is one immutable collection event, not a synchronized live close.
Every chart records its title, generation timestamp, market date, retrieval time,
curve representation, units, source and rights decision. Source-published par,
benchmark yields and fitted continuous-zero rates are not interchangeable.

## Latest collection

**Title:** Selected public sovereign curves, collected2026-11-11.
**Generated:** 2026-11-11T14:33:34+00:00 (22:33:34 Asia/Shanghai).

[Offline HTML overview](20261111T143334Z/index.html) ·
[Full source nodes and metadata](20261111T143334Z/snapshot.json)

| Curve | Market date | Published nodes | Chart |
| --- | --- | ---: | --- |
| US Treasury nominal par | 2026-11-10 | 14,1M–30Y | [UST](20261111T143334Z/ust.svg) |
| Japan MOF constant maturity, semiannual compounding | 2026-11-10 | 15,1Y–40Y | [JGB](20261111T143334Z/jgb.svg) |
| Euro-area AAA fitted continuous-zero spot | 2026-11-10 | 358,3M–30Y monthly | [AAA](20261111T143334Z/euro_area_aaa.svg) |
| Euro-area all-ratings fitted continuous-zero spot | 2026-11-10 | 358,3M–30Y monthly | [All ratings](20261111T143334Z/euro_area_all.svg) |

Europe means the ECB euro-area groups, not every European country. All745 source
nodes are retained. Missing annual maturities are not invented or set to zero;
the connecting lines are visual guides, not new market observations. Original
source curves may themselves be model-fitted, as the labels explain.

CGB, HKGB and UK were also requested. Their derived figures/data are **not
published here**, because public reproduction/redistribution permission was not
established for the retrieved sources. See [DATA_LICENSES.md](DATA_LICENSES.md).

GitHub previews SVGs. Download the folder to open its HTML overview locally;
GitHub's HTML source page does not execute it. No hosted website or live feed is
being deployed by this archive.

## Add the next curve

1. Review the actual source, public-display rights, units, representation,
   observation date and all native maturity points. Record retrieval time and
   source hashes in the notes where available. Do not reuse a prior price under
   today's market date.
2. Prepare a new schema1.0.0 JSON input. `scripts/curve_archive.py` documents and
   validates the fields; the current snapshot is a concrete example. Use a new
   UTC timestamp identifier such as `YYYYMMDDTHHMMSSZ`.
3. Run offline:

   ```sh
   python scripts/curve_archive.py REVIEWED_INPUT.json --output-root curve --public
   ```

4. The renderer rejects existing snapshot directories and any rights HOLD. It
   does not fetch sources or establish rights by itself. Review output, add every
   new public file to `publication_manifest.json`, run tests/publication checks,
   and obtain approval before pushing.
5. Add a dated entry here and in the delivery log. Corrections create a NEW
   snapshot with a correction note and link; do not overwrite the earlier one.

This protocol stores new curves when produced. It does not schedule continuous
fetching, promise a daily update, reconstruct historical availability, or create
a trading/data service.
