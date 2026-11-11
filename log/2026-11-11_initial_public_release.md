# Initial selected public release — 2026-11-11

## Authorization and scope

The owner explicitly requested a new public `p-curve` repository containing only
selected parts of proprietary PFICC / P-Curve, precedent-first publication rules
in README and AGENTS, and contribution paths for readers' curves and FICC repos.
The full private program is not being published. This new repository contains no
private Git history or market-data snapshot. Code selection and review were
AI-assisted; independent human financial review is **NOT_RUN**.

## Source and adaptation

Owner-controlled pure mathematical routines were selectively adapted from PFICC
P-Curve. Private source commit/blob receipts and content hashes are retained in
an ignored local audit, not the public tree. Tests were rewritten with fictional
fixtures and independent mathematical oracles. Macro/event data, private models,
strategies, data files, accounts and private links were excluded.

Four pinned primary-source repositories establish same-topic public precedents:
NSS, QuantLib, FinancePy and Strata. No third-party implementation was copied or
installed. The register is not a performance benchmark or proof of frontier/SOTA.

## Verification

- Public mathematical tests: **30/30 PASS** on Python 3.12.14.
- Repository contracts: **4/4 PASS**; full suite **34/34 PASS** (0 skipped).
- A fresh local virtual environment installed the built 0.1.0 wheel; import was
  explicitly checked to come from its `site-packages`, not the source tree.
  `pip check` passed; runtime dependency count is zero. Building requires setuptools.
- Synthetic example: PASS; independent exponential PV oracle agreed; example PV
  101.77944403833929 and parallel DV01 0.019870666170938023 currency/bp.
- Exact 28-file publication inventory and bounded disclosure scan: PASS. An
  intentionally unapproved synthetic probe was rejected, then removed.
- Five YAML contribution/config files parsed and their basic field structure
  checked locally using an existing PyYAML tool; it is not a project dependency.
  Hosted issue-form rendering remains NOT_RUN.
- Independent review corrected a README/API mismatch and found an overflowed
  finite-difference denominator. Both fixed; the latter has a regression test.
- The first build attempt hit sandbox temporary-directory permissions; a second
  offline attempt exposed a missing build backend in the unrelated research
  environment. No packages were installed into that environment. Fresh-environment
  build isolation installed the declared backend and succeeded.
- Public remote created: [pengpengyi92/p-curve](https://github.com/pengpengyi92/p-curve).
  Issues and Discussions enabled. PFICC independently rechecked as private;
  its contents and visibility were not modified.
- Initial public root commit `f2f63b657addeed7cdd202fc1147420fed419174` has **zero
  parents**. Remote tree readback returned exactly the28 allowlisted files.
- [Initial-code CI43037316248](https://github.com/pengpengyi92/p-curve/actions/runs/43037316248):
  **6/6 jobs PASS** — Linux and Windows × Python3.10/3.12/3.14. Each job independently
  installed the package, ran34 tests, ran the synthetic example and passed the
  publication check. Follow-up receipt/documentation edits are checked by the
  same workflow; the Actions page remains the live status source.
- Package version is0.1.0. This delivery publishes source to GitHub only; no PyPI
  upload, data service, hosted dashboard, trade or external upstream PR occurred.

The scanner is a bounded heuristic and allowlist check, not proof of absence of
all sensitive content. Every selected public file also receives content review.
Cross-library accuracy/performance, empirical prediction, PIT/OOS alpha,
production readiness, economic benefit and adoption remain **UNMEASURED**.

## Next action

Review community curves and recommendations individually; prioritize independent
numerical oracles before breadth. Do not widen the public scope automatically.
