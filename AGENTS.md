# P-Curve maintainer and agent instructions

## Identity and hard boundary

- This repository is the selected open-source subset of proprietary PFICC /
  P-Curve, not its mirror or complete release. PFICC P-Curve will not be fully
  public. Never clone, sync, copy, or publish its whole tree or Git history here.
- Public code must remain independently understandable, installable, testable,
  and useful. Never require access to private PFICC to reproduce a public claim.
- Frontier-oriented research is a goal, not proof of novelty or SOTA. Established
  methods must be called established; no unmeasured performance or alpha claims.

## Required publication gate

For EACH proposed feature/topic, including external contributions:

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
