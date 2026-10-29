# What is reused and what was added

Reused verbatim (byte-verified at build time against the published atlas's DATA object,
sha256 prefix 2d2e6074dc400d0e): all 7,236 paper records (coordinates, titles, journals,
years, body sites, clusters, PMIDs, disease classes, MONDO terms and evidence tiers),
the journal, site, tier, class and cluster vocabularies, the 1,104 MONDO nodes with
their lineages, and the MONDO version string (2026-09-01).

Added, presentation only, all derived from the data above at page load:
- a point-density grid, used for the contour lines, the optional relief height
  (labeled on screen as presentation) and the territory-label anchors;
- the camera, tour stops and captions (captions state only counts computed from DATA);
- colors, typography and UI.

The dataset ships as atlas-data.js as plain JSON; the build script verifies it parses byte-identical to the source data before the page is written.

Nothing scientific was added, removed or changed. In disease, class and topic modes the
seven largest groups are colored and the rest are muted gray, matching the published
atlas's legend behaviour; papers whose group is "unclustered" or "none/healthy-cohort"
are shown muted, not hidden.

- `og-image.png` — a screenshot of the rendered page, committed so link previews (Open Graph) show the map. Presentation only, generated from the page itself.

- Globe projection — the same flat layout mapped onto a sphere (longitude proportional to x, latitude proportional to y) for presentation. The sphere carries no geographic meaning; the papers have no location data.

- `associations.js` + `pilot/associations.csv` — microbe–disease associations with directionality, produced ONLY from extraction over the corpus's own abstracts via `tools/validate_associations.py` (see `SCHEMA.md` and `EXTRACTION.md`); every association is traceable to its supporting papers in the atlas. The current layer is a PILOT: a 150-abstract stratified sample (by body site, seed 20261028), titles + abstracts only, double-pass extraction with an agreement filter.
  - Pass A 119 tuples; pass B 131 (independent same-model session: fresh context, reversed paper order, differently framed prompt; neither pass saw the other's output). Agreement kept 101 of 149 union tuples — **disagreement rate 32.2%**, consistent with the 25–50% single-pass extraction error that motivates the protocol. 0 tuples dropped by the double-medium confidence floor. 2 review/meta-analysis records excluded from primary claims.
  - MONDO resolution: all 23 distinct disease wordings hand-mapped to atlas-subtree nodes and programmatically verified against the subtree (100% reviewed — exceeds the protocol's 20% spot-check floor). 10 agreed tuples set aside as out of scope: preterm birth (6 — no node in this atlas's MONDO subtree), protein–calorie malnutrition within IBD (4 — a within-disease contrast, not case-vs-control).
  - Final: 91 rows — 54 enriched, 37 depleted, 21 diseases, 70 taxa, 24 supporting papers. The drawer header carries the label "pilot · abstract-only · double-pass agreed"; the full-corpus run should use two different models and full text where available.
