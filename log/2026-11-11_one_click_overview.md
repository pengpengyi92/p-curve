# One-click curve overview — 2026-11-11

## Requested change

Add an actually rendered one-click overview beside the HTML-source link, credit
`Author: pengyi`, and include appreciative comments such as “What a beautiful
curve.” Synchronize the presentation pattern without exporting private curves.

## Implementation

- New current portal `curve/index.html`; frozen dated snapshots are read-only.
- Credit pengyi for curation/visualization, not authorship of official source data.
- Subjective editorial appreciation is separate from source facts and explicitly
  not investment analysis. No forecasts, causal claims or new market observations.
- Full native tables, source/rights notes, market/retrieval/collection clocks and
  original archived charts are retained. No external runtime/CDN or analytics.
- README places the rendered GitHub Pages entry next to HTML source. Root entry
  redirects to the current portal; `.nojekyll` keeps this buildless/static.
- `curve/OPEN_OVERVIEW.cmd` contains only two commands opening its sibling HTML;
  clone/download first, then double-click on Windows. No network/upload behavior.
- Public portal contains only the4already-approved curves/745nodes. Private
  archives are not deployed. No Pages settings are changed for private PFICC.

## Verification

-64/64 offline tests PASS (49existing +11portal +4entry tests).
- Original public snapshot Git subtree remains
  `c771c3781fceacd4eac6d455b89eed615393ec65`; no dated JSON/HTML/SVG changed.
- Portable relative image/metadata links, escaping, author/source distinction,
  full node tables, HOLD rejection and immutable-byte preservation checked.
- Browser automation blocks `file://` navigation. Local-only UI clicks were not
  automated; private content was not served through a workaround.
- Remote CI, Pages deployment, HTTP and public browser verification: PENDING.

## Scope

Static selected public research presentation only. No new model, feed, data-rights
grant, private-site deployment, financial validation or trading service.
