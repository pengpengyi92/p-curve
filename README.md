# P-Curve

**Selected open-source curve research from PFICC / P-Curve.**

**[一键打开 Curve 总览](https://pengpengyi92.github.io/p-curve/curve/)** ·
[HTML source](curve/index.html) · [Local one-click](curve/OPEN_OVERVIEW.cmd)

Author: **pengyi** · Curated & visualized by pengyi. Official data sources are
credited separately. Aesthetic comments in the viewer are subjective, not
investment signals.

P-Curve is a small, reproducible FICC research library maintained by Pengyi Peng.
It is the **selected public subset** of the proprietary PFICC P-Curve program,
not a mirror, full release, or disclosure of that program. PFICC and its P-Curve
work will **not** be fully open-sourced. This public repository has its own scope,
tests, versioning, and contribution process.

> 这是 PFICC / P-Curve 的精选开源部分，不是 PFICC 或其 P-Curve 的完整公开版。
> 已有可信开源先例的相关主题，才进入公开候选；找不到相关先例的部分暂缓公开。
> 有先例也不等于自动公开：仍须审查代码权属、许可、数据和研究边界。

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

We welcome your curve implementations, independent test oracles, bug reports,
FICC repository recommendations, and carefully bounded research questions.
Start with an [issue](https://github.com/pengpengyi92/p-curve/issues/new/choose),
join [Discussions](https://github.com/pengpengyi92/p-curve/discussions), or read
[CONTRIBUTING.md](CONTRIBUTING.md). Novel topics without a reviewed public
precedent remain on hold under the publication policy. Never submit private
positions, employer/client material, credentials, or unlicensed datasets.

## Evidence and roadmap

- [Benchmark Card](BENCHMARK_CARD.md): what was and was not measured.
- [TODO](TODO.md): verifiable priorities, not implied implemented features.
- [Changelog](CHANGELOG.md) and [log](log/): versioned delivery records.
- [AGENTS.md](AGENTS.md): instructions for maintainers and coding agents.

MIT applies to our code and documentation in **this repository only**. Archived
source data retains the separate conditions in [DATA_LICENSES.md](curve/DATA_LICENSES.md),
not an automatic MIT relicensing. No private PFICC code, data, models or research
outside the selected public files is licensed here. See [LICENSE](LICENSE).
