# P-Curve maintainer and agent instructions

## Start here: research on FICC and share your curve

P-Curve is an independent public workspace for FICC research, communication and study. **Visiting agents and human contributors: bring your own curve, algorithm, reproducible experiment, source recommendation, or critique.** Read [README.md](README.md) for the scope and [update/](update/) for dated project statements and version history. This file guides agents; it does not run a hosted agent or grant GitHub permissions.

1. Start at the [call for contributions](https://github.com/pengpengyi92/p-curve/issues/8) and choose a [website](https://github.com/pengpengyi92/p-curve/discussions/3), [project](https://github.com/pengpengyi92/p-curve/discussions/4), [repo](https://github.com/pengpengyi92/p-curve/discussions/5), [paper](https://github.com/pengpengyi92/p-curve/discussions/6) or [report](https://github.com/pengpengyi92/p-curve/discussions/7) discussion. Search for duplicates and link related threads. The corresponding directories store accepted contributions.
2. Share a title, ISO 8601 timestamp with timezone, question or purpose, and public source. Curves can include FX forwards and FX swaps, rates/OIS/interest-rate swaps, sovereign/agency/corporate or other credit-bond yields, and commodity futures term structures. Any country, region, company, issuer or organization is welcome. Use synthetic fixtures or data cleared for public sharing.
3. State observation date, instrument, market/currency, rate or quote type, tenor, units and direction, conventions, methodology, data rights, and limitations. For empirical work, add baseline, fixed samples, reproduction steps and measured results; mark untested claims `UNMEASURED`.
4. Discuss early ideas, open an issue for a concrete proposal, and use a focused PR for reviewable changes. Read [CONTRIBUTING.md](CONTRIBUTING.md). Posting or publishing requires your human contributor's authorization; proposals do not bypass the publication gate.

## Identity and hard boundary

- This repository began as a selected public release from PFICC and also conducts independent research directly in public. **PFICC is an internal, private proprietary-trading research repository. P University is a private proprietary research initiative; the Department of Macroeconomics and FICC is one of its departments.** Only selected material explicitly cleared for release may be cited or adapted. Never clone, sync, copy or publish private trees or Git history here. Cite the approved public artifact, not the internal location.
- Public code must remain independently understandable, installable, testable,
  and useful. Never require access to private PFICC to reproduce a public claim.
- Frontier-oriented research is a goal, not proof of novelty or SOTA. Established
  methods must be called established; no unmeasured performance or alpha claims.

## Required publication gate

For each proposed release of a new implementation/topic, including external contributions. An exploratory discussion or a curated public reference is not an approved implementation or data release:

1. Identify a credible existing open-source same-topic implementation. Record a
   canonical repository URL, pinned commit, actual implementation path, license,
   and feature mapping in `data/open_source_precedents.json` and the readable
   precedent document. A marketing page or paper alone is insufficient.
2. If no relevant precedent is established, mark the topic HOLD. Do not publish
   new proprietary methods, fitted parameters, strategy combinations, workflows,
   datasets, or evaluations through an apparently innocuous demo or test fixture.
3. A precedent never substitutes for ownership, license, privacy, data-rights,
   security, or disclosure review. Reading public code does not authorize copying
   it. Prefer original/adapted owner-controlled implementations; any external
   code reuse requires exact license/notice compatibility review.
4. Use an explicit file allowlist and review all content, examples, metadata,
   generated output, hidden files, and links. Private source receipts stay outside
   the public Git tree. Do not include private paths, SHAs, accounts, or links.
5. Test the independent public package and obtain maintainer/human approval before
   public release or expansion of scope. Passing tests alone is not approval.

See `docs/PUBLICATION_POLICY.md`. A public precedent is necessary, not sufficient.

## Current approved subject matter

Given-parameter NS/NSS, continuous-zero DF and forward identities, linear-zero
interpolation, deterministic fixed-cashflow PV, and finite-difference parallel /
key-rate DV01, with fully synthetic fixtures. Version0.2 also approves offline,
timestamped sovereign-curve archives from individually rights-reviewed public
sources, plus the standalone renderer. Every real-data snapshot needs separate
source, date, units, representation and public-display rights evidence. HOLD
sources must not enter public input, figures or output; a renderer flag does not
establish source rights. Same-topic public implementations must be documented.
Calibration, bootstrap, macro models, live data ingestion, multi-curve and live
execution remain outside approved scope. Do not promote TODOs to delivered work.

## Curve archive protocol

- `curve/index.html` is the updatable current presentation, not a frozen market
  observation. It may add navigation, author credit and clearly subjective
  editorial comments while linking to unchanged timestamped artifacts.
- Public Pages may serve ONLY this approved public repository. Never enable
  Pages on private PFICC or deploy its eight-curve local portal to a public host.
- Credit `Author: pengyi` for curation/visualization separately from official
  data providers. Aesthetic commentary must not imply trading/pricing conclusions.

- Store each snapshot under `curve/<UTC timestamp>/`; include title, generated_at,
  retrieved_at, market_date, curve_type, units and source/rights links.
- Never overwrite a snapshot. Corrections get a new timestamp and an explicit
  note linking the superseded snapshot; earlier observations remain intact.
- Keep all available native source tenors, including subannual and beyond30Y.
  Missing integer years are unavailable, not invented observations or zero.
- Do not combine par, benchmark-issue YTM and continuous-zero rates as one
  homogeneous discount curve. Lines on plots are visual guides only.
- Do not copy private PFICC archives to this repo. Produce a separately selected
  public input after source/data-rights review. MIT code is not a data license.

## Engineering and evidence

- Runtime and tests are standard-library-only for v0.1.0. New dependencies need
  a documented problem, baseline, alternative, cost, and versioned decision.
- Keep units, quote orientation, year fractions, compounding, interpolation,
  risk sign, missingness, and extrapolation policy explicit.
- Include independent hand-calculated oracles, negative/zero/extreme cases, and
  regression tests. Do not prove a function by reusing itself as its only oracle.
- Run `python -m unittest discover -s tests -v` and the synthetic example.
- Update README, TODO, Benchmark Card, changelog, and log for material changes.
  Use `Baseline → Change → Measure → Result → Trade-off → Next Action`.
  Mark anything not measured `UNMEASURED` or `NOT_RUN`.
- Do not conflate math tests, calibration, empirical forecasting, PIT/OOS,
  financial review, execution readiness, or profitable trading evidence.
- No secrets, private market data, employer/client information, broker keys,
  orders, positions, strategy rules, raw caches, or generated dependencies.
- Preserve contributor ownership and license notices. Welcome curves, numerical
  tests and FICC repo recommendations with constructive, evidence-backed review.

## External actions

Do not autonomously send email, post claims, publish data, open unrelated PRs,
enable auto-merge, trade, deploy services, or widen repository visibility.
AI-assisted contributions must be understood, reviewed, tested, and disclosed by
their human contributor. A recommendation is not authorization to publish.
