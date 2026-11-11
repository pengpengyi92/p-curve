# Selected-publication policy

## Purpose

P-Curve makes selected parts of the proprietary PFICC P-Curve program useful to
the public. It is not a staged commitment to disclose the remaining program.
The public repository has an independent root commit and no private Git history.
Its license applies only to approved public files.

The owner explicitly chose this rule: **where a relevant open-source precedent
exists, consider a selected release; where none is established, hold publication.**
This is a disclosure rule, not proof that an algorithm is new or globally absent.
Search is necessarily incomplete. No claim is made to have reviewed all FICC
repositories or to be ahead of every public implementation.

## Review states

`PROPOSED → PRECEDENT_REVIEWED → RIGHTS_REVIEWED → TESTED → HUMAN_APPROVED → PUBLIC`

At any failed or incomplete gate: `HOLD`. Fixing tests does not bypass rights
review. A new composite strategy does not inherit publication approval merely
because its individual ingredients are familiar.

| Gate | Required evidence |
| --- | --- |
| Topic precedent | Actual open-source implementation, pinned source URL, license and bounded feature mapping; not merely a paper or an unlicensed repository |
| Rights | Ownership of our implementation; third-party obligations; independent source/data display and redistribution review where applicable |
| Disclosure | Explicit allowlist; no private tree/history, strategy, parameters, employer/client material, raw data or private metadata |
| Reproducibility | Standalone environment, synthetic default, tests, conventions, provenance and honest limits |
| Approval | Human/maintainer approves exact files and release scope; new topics need a new review |

## Initial release allowlist by subject

- Owner-controlled pure math utilities for given-parameter NS/NSS, continuous-zero
  discount/forward calculations, linear-zero interpolation, fixed-cashflow PV,
  and finite-difference parallel/key-rate DV01.
- Synthetic examples, independent mathematical test oracles, packaging and CI.
- Public policy, documentation, issue forms, source recommendations, and evidence.

No source/data directory from PFICC is bulk-exported. Macro response models,
event-case fixtures, trading strategies, fitted coefficients, calibration,
bootstrapping, data connectors and multi-curve pricing are outside initial scope.
Documentation can name their absence but must not disclose their private contents.

## Code and data are different permissions

### Version0.2 approved extension

The owner requested timestamped CGB/UST/JGB/UK/HK/euro-area curve storage. The
selected PUBLIC extension is the offline archive renderer and only those
individual datasets with reviewed public display/reproduction rights. Others
remain private or unavailable. OpenBB provides a reviewed same-topic public
precedent; it is not a code donor, dependency, or data entitlement.

Every snapshot needs title, timezone-aware generation/retrieval times, distinct
market date, source URL, curve representation, units and rights decision. Preserve
all native nodes without inventing missing annual observations. Outputs are
append-only; corrections create a new snapshot. Code MIT and upstream data rights
are separate; see the archive's DATA_LICENSES document.

An upstream MIT/BSD license covers that upstream's licensed code, not PFICC code
or market data. Our MIT license does not grant rights to any private PFICC work.
An openly viewable market page is not automatically an open dataset. Therefore
v0.1.0 contains no live/historical market-data snapshots, raw downloads or accounts.

External implementations are **references only** in v0.1.0: they are not runtime
dependencies, code donors, or measured comparison baselines. Any future copying
requires a separate compatibility/attribution review before merging.

## Honest frontier positioning

We aim to contribute to current FICC research through reproducibility, careful
contracts, independent checks and useful collaboration. Initial formulas are
well-known methods, not newly discovered models. SOTA, predictive skill, superior
pricing, economic benefit and production readiness require separate fixed-test
comparisons and independent evidence; they are not established by this release.
