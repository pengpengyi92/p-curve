# Global sovereign yield overlay delivery

- **Cutoff:** `2026-11-19T00:17:13+08:00`; UTC archive ID
  `20261118T161713Z`. Input base `9b979ca0c1e40b57094f7ad9e34fa764697d6ab3`.
  Cutoff is not market date. No 11-19 end-of-day rates are in this edition.
- **Scope:** original config ingestion and visualization example. Four public
  curves with 40 source nodes and two source-only entries. ChinaBond and the
  BoE workbook remain HOLD. Separate local-only inputs and outputs excluded.
- **Precedents:** the already reviewed [OpenBB dated sovereign
  schema](../docs/OPEN_SOURCE_PRECEDENTS.md) and curated [static plotting
  implementations](../repo/data-visualization/README.md). No external code
  copied, package/API changes, or new runtime dependencies.
- **Local validation:** Windows 11 / Python 3.12.14. `PYTHONPATH=src` and
  `python -X utf8 -m unittest discover -s tests -q`: baseline 71, candidate
  77 pass, exit 0. `python -X utf8 scripts/publication_check.py` passes.
  `python -X utf8 -m examples.global_sovereign_overlay.generate` regenerates
  exact SVG bytes; the existing synthetic example also runs. Visually checked
  the SVGs in isolated headless Chrome. Local evidence is not hosted CI.
- [Frozen config](../curve/20261118T161713Z/config.json) ·
  [Chart](../curve/20261118T161713Z/global_sovereign_yields.svg) ·
  [Usage / limits](../examples/global_sovereign_overlay/README.md).
- [Issue #10](https://github.com/pengpengyi92/p-curve/issues/10) requests one
  official daily data adapter first; intraday access is unverified.
