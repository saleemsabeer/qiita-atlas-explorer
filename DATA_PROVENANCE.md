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

Nothing scientific was added, removed or changed. In disease, class and topic modes the
seven largest groups are colored and the rest are muted gray, matching the published
atlas's legend behaviour; papers whose group is "unclustered" or "none/healthy-cohort"
are shown muted, not hidden.
