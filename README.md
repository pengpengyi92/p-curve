# P-Curve

**Research on FICC. Share your curve.** P-Curve is a public place to study fixed income, currencies and commodities, conduct reproducible research, and exchange curve implementations and ideas. Humans and AI agents are welcome: start with [AGENTS.md](AGENTS.md).

**[一键打开 Curve 总览](https://pengpengyi92.github.io/p-curve/curve/)** ·
[HTML source](curve/index.html) · [Local one-click](curve/OPEN_OVERVIEW.cmd)

Author: **pengyi** · Curated & visualized by pengyi. Official data sources are
credited separately. Aesthetic comments in the viewer are subjective, not
investment signals.

P-Curve began with a selected release from **PFICC**, an internal, private proprietary-trading research repository. It now also conducts original curve research directly in public. We may publish or cite selected work from PFICC and the **Department of Macroeconomics and FICC**, one of the departments of **P University**, a private proprietary research initiative. Only explicitly approved material may be shared. Neither private repository is a dependency or a mirror of P-Curve.

> P-Curve 是公开的 FICC 研究、学习与交流项目。欢迎分享自己的曲线。PFICC 和 P University 均为私有；只会择取经批准可公开的成果，不公开内部原始材料。

## P-Curve opens for public FICC research and curve sharing

[Visualization references and FICC plotting checklist](repo/data-visualization/README.md):
12 public repositories, pinned code/license evidence, actual-tenor axes, units,
conventions and source rights. Reference-only; no new curve model/data release.

**2026-11-14T03:37:12+08:00** (Asia/Shanghai) · [Full statement and version history](update/).

Share synthetic or rights-cleared curves from any market: FX forwards and swaps, rates/OIS/swap curves, sovereign and corporate/credit bond yields, or commodity futures term structures. Countries, regions, issuers, and other organizations are all welcome. Clearly distinguish the market observation date from the submission timestamp.

| Direction | What to share |
| --- | --- |
| [Website](website/) · [Discuss](https://github.com/pengpengyi92/p-curve/discussions/3) | Public data-source pages, methodology guides, and educational sites |
| [Project](project/) · [Discuss](https://github.com/pengpengyi92/p-curve/discussions/4) | Original implementations, synthetic experiments, and reproductions |
| [Repo](repo/) · [Discuss](https://github.com/pengpengyi92/p-curve/discussions/5) | Upstream FICC code with an exact entry point and license |
| [Paper](paper/) · [Discuss](https://github.com/pengpengyi92/p-curve/discussions/6) | Research papers, reading notes, and reproduction proposals |
| [Report](report/) · [Discuss](https://github.com/pengpengyi92/p-curve/discussions/7) | Your own curve reports, convention comparisons, or source notes |

## Why a selected public release?

We want useful, frontier-oriented FICC research to be reproducible and discussable
without disclosing proprietary research. Here, **frontier-oriented is an ambition,
not a claim of state-of-the-art performance**. The initial methods are established
public mathematics. Value must be demonstrated through clear conventions,
independent checks, reproducibility, practical contributions, and measured results.
No private result is used as uninspectable evidence of public superiority.

Our publication rule is deliberate:

1. Find and record an existing, credibly open-source same-topic implementation.
2. Review our own ownership, source licenses, data rights, and disclosure boundary.
3. Export only explicitly approved files into this independent repository.
4. Test the public package independently. Publish measured claims with limits.

**No relevant public precedent found → HOLD, not publication.** A public precedent
is necessary, not sufficient; it does not grant rights to someone else's code or
data, or authorize disclosure of PFICC. We do not claim to have surveyed every
FICC repository. See [precedents](docs/OPEN_SOURCE_PRECEDENTS.md) and the
[publication policy](docs/PUBLICATION_POLICY.md).

## Version 0.2.0: dated curve archives

[Curve archive](curve/README.md) stores selected rights-reviewed sovereign curves
under immutable timestamped folders. Each has an independent SVG, full node table
and source metadata. Market date is separate from retrieval/generation time;
latest-available data is not advertised as today's live price. Source-published
par, issue-YTM and fitted-zero representations remain explicitly distinguished.

Only approved public-display sources are included. Requested markets with
unconfirmed redistribution rights remain excluded; see
[source/data rights](curve/DATA_LICENSES.md). The offline renderer does not fetch
data and cannot grant source rights. Future snapshots must pass the same gate.

## Mathematical core (introduced in 0.1.0)

- Given-parameter Nelson–Siegel and Nelson–Siegel–Svensson yield functions.
- Continuous-zero discount factors and period-average continuous forwards.
- Piecewise-linear zero interpolation, without extrapolation.
- Deterministic fixed-cashflow present values.
- Central finite-difference parallel and key-rate DV01.
- Synthetic examples and offline regression tests. No API key or market data needed.

This is **experimental research software**, not a validated production pricing
library, calibration engine, bootstrapping system, multi-curve/CSA framework,
market-data service, investment recommendation, or trading strategy. Macro betas,
private models, strategy logic, real positions, and original PFICC datasets are
outside this release. External repositories are references, not dependencies or
performance benchmarks.

## Run it

Python 3.10 or newer; the runtime and tests use only the Python standard library.
From a clone of this repository:

```sh
python -m pip install --no-deps -e .
python -m unittest discover -s tests -v
python examples/synthetic_curve.py
```

Or run without installing anything:

```sh
# Linux/macOS
PYTHONPATH=src python examples/synthetic_curve.py

# PowerShell
$env:PYTHONPATH = 'src'
python examples/synthetic_curve.py
```

```python
from p_curve import price_cashflows, parallel_dv01

# Explicitly synthetic: (years, continuous zero rate as a decimal).
curve = [(0.5, 0.03), (1.0, 0.03), (2.0, 0.04)]
cashflows = [(1.0, 5.0), (2.0, 105.0)]
pv = price_cashflows(cashflows, curve)
dv01 = parallel_dv01(cashflows, curve)
```

## Conventions are part of the API

- Times are caller-supplied year fractions; no date, settlement, day-count, or
  business-calendar engine is supplied.
- Rates are annualized decimals, **not percent**; `0.03` means 3%. Zero rates and
  the reported period-average forwards use continuous compounding.
- Cashflow amounts are signed and in one consistent currency/unit. No accrued
  interest, credit risk, tax, FX conversion, or optionality is inferred.
- Curves have strictly increasing nodes; cashflows must lie within their range.
  Negative rates are allowed. Non-finite inputs and unsupported numeric ranges
  are rejected rather than silently repaired.
- DV01 is `(PV_down - PV_up) / (2 * bump_bp)`, in currency units per 1 bp.
  Key-rate risks depend on the specified interpolation; their sum agrees with
  parallel DV01 only to finite-difference accuracy, not as an exact identity.

## Contribute your curve

Bring your own curve, algorithm, research question, or negative result. Start at [Share your curve — Issue #8](https://github.com/pengpengyi92/p-curve/issues/8) and choose a [Discussion](https://github.com/pengpengyi92/p-curve/discussions). Use issues for concrete proposals and focused PRs for reviewed changes. Include a title, timezone-aware timestamp, conventions, source and rights. Read [CONTRIBUTING.md](CONTRIBUTING.md) first. A proposal is not authorization to upload market data or release a new method.

## Evidence and roadmap

- [Benchmark Card](BENCHMARK_CARD.md): what was and was not measured.
- [TODO](TODO.md): verifiable priorities, not implied implemented features.
- [Changelog](CHANGELOG.md) and [log](log/): versioned delivery records.
- [AGENTS.md](AGENTS.md): instructions for maintainers and coding agents.

MIT applies to our code and documentation in **this repository only**. Archived
source data retains the separate conditions in [DATA_LICENSES.md](curve/DATA_LICENSES.md),
not an automatic MIT relicensing. No private PFICC code, data, models or research
outside the selected public files is licensed here. See [LICENSE](LICENSE).
