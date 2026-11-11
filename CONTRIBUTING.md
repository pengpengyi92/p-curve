# Contributing to P-Curve

Welcome your curve implementations, numerical tests, reproducible bug reports,
research questions, and recommendations of useful FICC repositories. A careful
small contribution is more useful than an unreviewable expansion of scope.

P-Curve is a **selected open-source surface** of PFICC's P-Curve research, not the
complete proprietary system. A contribution does not grant access to PFICC, and
this repository is not a route for requesting private code, datasets or methods.

## Choose a contribution path

| You want to contribute | Start here | Useful evidence |
| --- | --- | --- |
| A curve, numerical method or risk calculation | Curve / method proposal issue, then a focused PR | Conventions, existing openly licensed same-topic precedent, hand-calculated baseline and edge tests |
| A useful FICC repository | FICC repository recommendation issue | Canonical URL, license evidence, exact relevant feature and a limitation |
| A defect | Reproducible bug report issue | Minimal synthetic fixture, expected and actual results, version and command |
| A research question or comparison | Research discussion issue | Falsifiable question, public references, baseline and a proposed measurement |
| Better documentation or a regression test | A small PR | Explain which ambiguity or failure the change resolves |

Issue templates are available under **New issue**. Use Discussions if enabled for
longer exploration; keep an implementation issue or PR linked to the resulting
decision. Recommendations are reviewed, not automatically endorsed, installed,
executed or merged into the project.

## Publication gate: precedent is necessary, not sufficient

For a new mathematical or FICC topic, identify a credible **already openly
licensed same-topic implementation** and link the exact relevant source and
license. If no relevant open-source precedent is established, the proposed topic
stays **HOLD / not selected for publication**. An interesting paper, a public
website or a repository without a license is not enough to pass that gate.

Even with a precedent, a maintainer must explicitly review rights, confidentiality,
scope and evidence before accepting the topic. Public availability elsewhere is
**not permission to disclose PFICC code or data**, does not establish our ownership,
and does not authorize copying third-party code. A precedent may be documented
without becoming a dependency or contributing any code.

For your own original code, confirm that you are entitled to publish it and identify
any employer, collaborator or contractual restrictions. For adapted third-party
code, identify the upstream version, license compatibility, required notices and
attribution; do not relabel copied code as original or remove license notices.
Data permissions must be reviewed separately from software licenses.

## Numerical contribution contract

A new curve or calculation must state:

- The object being modeled: benchmark yield, par, zero, discount factor, forward,
  spread, volatility, or something else. Do not silently treat them as equivalent.
- Units and quote direction: decimal or percent rates, bp or pips, currency and
  notional, maturity or settlement dates, and risk sign convention.
- Compounding, interpolation/extrapolation, day count and calendars. Say
  **not modeled** when the implementation intentionally uses year fractions only.
- A small independent oracle or hand calculation, not merely the same helper
  function called twice, and tolerances with a reason.
- Tests for zero/short maturity, negative rates where supported, invalid/non-finite
  inputs, and off-node behavior relevant to the change. Do not assume one test set
  is sufficient for every method.
- Scope and limitations. Distinguish arithmetic identities and synthetic scenarios
  from fitted models, calibrated curves, forecasts, executable prices and P&L.

Use synthetic data by default. Do not attach raw vendor data, customer positions,
bank materials, credentials, private URLs or unpublished PFICC artifacts. A public
market-data page does not by itself permit redistribution of its contents.

## Development and evidence

Use the installation instructions in the README, then run the offline suite from
the repository root:

```console
python -m unittest discover -s tests -v
```

Run any additional command relevant to your change and record the exact result.
If a test, benchmark, live feed, integration or platform was not exercised, mark it
**NOT_RUN** or **UNMEASURED** rather than implying that it passed. Keep external
network/data checks separate from deterministic offline tests.

A substantive method or workflow change should update the Benchmark Card using
**Baseline → Change → Measure → Result → Trade-off → Next Action**. Claims such as
faster, more accurate, frontier or state of the art require an identified comparator,
fixed test set, protocol, results and limitations. A new chart is not that evidence.

## Review, AI assistance and communication

AI assistance is welcome when a human contributor understands the change,
reviews it, runs the relevant tests and discloses material assistance in the PR.
Do not submit unverified generated code, citations or measurements. Do not allow
an agent to publish private material or send external comments on your behalf
without explicit authorization.

Maintainers retain a **human merge and publication gate**. A passing CI run does
not authorize a new public topic, prove financial validity or trigger automatic
release. Please use the PR checklist and keep one independently reviewable change
per PR. Be respectful of reviewers' time; no response is not approval.
