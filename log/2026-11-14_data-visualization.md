# FICC visualization reference route

Timestamp:2026-11-14T16:15:46+08:00 (Asia/Shanghai). Base12c7f3b.

Human-authorized public reference addition:12 pinned visualization/reporting
repositories, verified source file/license/NOTICE identities and independent
FICC study questions under repo/data-visualization/. Public metadata originated
in dsh-quant's dated review; no private PFICC files, hashes, paths or data used.
No new curve/calibration/bootstrap/live-ingestion implementation or data release.

Focus:actual-tenor axes; units/quote direction; curve-type conventions; market,
observation and retrieval time; raw native nodes and public-display rights.
Par, issue-YTM and continuous-zero curves must not be treated as interchangeable.
Performance-tearsheet/backtest engines are adjacent references, not curve pricers.
Automatic unknown Matplotlib licenses stay separate from manual observations;
AGPL and TradingView attribution are not ignored. All12 REFERENCE_ONLY/NOT_RUN.

The linked synthetic dsh-quant SVG is separately self-authored and not a new
P-Curve runtime. It helped identify existing backtest cash issue166; no claim
of verified strategy results is made. Exact source metadata is public, and the
reading route is authored specifically for FICC rather than duplicated claims.

Publication allowlist additions limited to:three repo/data-visualization files,
this log and tests/test_visualization_catalog.py. Existing README/repo index/
TODO/benchmark/manifest edited; approved topics and immutable snapshots retained.
Acceptance:full offline tests, synthetic example and publication checker, plus4
reference tests; actual command/results and push readback follow below.

Baseline ->existing curve renderer/archive; Change ->12 public reading references;
Measure ->pinned paths/license/contracts and exact file gate; Result ->references
only; Trade-off ->no data/commercial/runtime certification; Next ->separate
approved-snapshot renderer evaluation. Performance/financial gains UNMEASURED.
Thanks for sharing reproducible curve/data/visualization work; review, source
rights and contributor credit remain required.

## Local verification — 2026-11-14T16:18:59+08:00

First unittest invocation failed to import p_curve because the fresh worktree
was not installed. Using temporary PYTHONPATH=src, Python3.12 full suite68/68
PASS; existing synthetic_curve.py and publication_check.py PASS. This does not
claim the local package was installed; hosted CI separately installs it first.
`git diff --check` PASS. Actual curve/source/precedent files are unchanged;
allowlist additions are precisely the approved public reference/test/log files.
No live source, private material or rendering-library runtime executed.
Remote CI, commit and push readback follow after actual delivery.

## Remote receipt — 2026-11-14T16:24:42+08:00

Source2f605fb03edf5f33139c81cd77b3e0eef17ddfa7 pushed;
[PR9](https://github.com/pengpengyi92/p-curve/pull/9) normally merged as
f690436c5029e8ae225dea655384460e4e8c394b after all six OS/Python platforms in
[CI43575453374](https://github.com/pengpengyi92/p-curve/actions/runs/43575453374)
passed installed-package68 tests, synthetic example and publication checks.
No admin bypass, self-approval or independent human review claim. Synced to
actual merged main; final receipt is documentation-only and remains under the
same explicit publication allowlist. No private-source/data or curve code
change; catalog remains reference-only, renderer gains UNMEASURED.
