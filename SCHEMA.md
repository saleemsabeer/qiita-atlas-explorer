# Microbe–disease association table — format spec

The atlas can display microbe–disease associations with directionality
(enriched vs depleted per disease), each one traceable to the papers that
support it. The site ships **without** this layer until a real extraction
is provided — nothing is invented. This file is the exact format that
extraction needs to arrive in.

## File: `associations.csv`

One row per (taxon, disease, direction) claim. UTF-8, comma-separated,
header row required.

| column      | required | contents                                                                 |
|-------------|----------|--------------------------------------------------------------------------|
| `taxon`     | yes      | Microbe name as it should display, e.g. `Faecalibacterium prausnitzii`. Any rank is fine; be consistent. |
| `mondo_id`  | yes      | MONDO CURIE of the disease, e.g. `MONDO:0005011`. Must be one of the 1,104 nodes already in the atlas subtree (the validator checks). |
| `direction` | yes      | Exactly `enriched` or `depleted` — the direction of the association in that disease relative to controls, as reported by the papers. |
| `pmids`     | yes      | Semicolon-separated PMIDs of the supporting papers, e.g. `36902282;35123456`. Each must be a paper already in the atlas (validator maps them to atlas entries and reports any that are not). |
| `note`      | no       | Short free-text qualifier shown in the UI tooltip, e.g. `16S only` or `mouse + human`. |

**Format illustrations only — these three rows are NOT data** (invented to
show the shape; delete them before filling in the real extraction):

```csv
taxon,mondo_id,direction,pmids,note
Faecalibacterium prausnitzii,MONDO:0005011,depleted,36902282;34567890,
Fusobacterium nucleatum,MONDO:0005575,enriched,33333333,16S + shotgun
Akkermansia muciniphila,MONDO:0005148,depleted,31111111;32222222;33222222,
```

## Ground rules

- A claim appears once per (taxon, mondo_id, direction); merge PMID lists
  rather than repeating rows. Opposite directions for the same pair are
  allowed (conflicting literature) and will be shown as such.
- Every row must be supported by at least one PMID that is in the atlas.
- Direction is as *reported by the papers* (case vs control), not
  re-derived.

## From CSV to the site

```
python -I tools/validate_associations.py associations.csv atlas data.json path -o associations.js
```

The validator checks every rule above, reports unresolvable MONDO ids and
PMIDs, dedupes, and emits `associations.js` (paper references resolved to
atlas entries). Drop that file next to `index.html` and the Associations
drawer appears; without it, the site is unchanged.
