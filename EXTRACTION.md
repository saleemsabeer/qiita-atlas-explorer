# Microbe–disease association extraction protocol

Per-paper LLM extraction of directional microbe–disease claims for the
atlas's associations layer. Designed for rigor over recall: extraction
error in this lab's prior experience runs 25–50% single-pass, so every
tuple here must survive two independent passes, and the disagreement rate
is published as the layer's error statement.

## Input

One record per paper: PMID, title, abstract (and full text where
available — the pilot is abstract-only and must be labeled as such).
Exclude records whose `pub_types` mark them as Review, Systematic Review,
or Meta-Analysis from PRIMARY claims (their claims may be recorded with
`source=review` but are not counted in the atlas layer).

## Pass prompt (use verbatim; run per paper)

```
You are extracting directional microbe-disease claims from one paper.

TITLE: {title}
ABSTRACT: {abstract}

Extract ONLY explicit, case-versus-control directional claims about a
microbial taxon in a human disease, stated as this paper's own finding:
patterns like "X was enriched / increased / higher / more abundant in
patients with Y" or "X was depleted / decreased / lower / reduced in Y".

Rules:
- The claim must name a specific taxon (any rank) and a specific disease
  or condition, and state a direction relative to controls or a healthy
  comparison group.
- Report the disease exactly as the paper words it.
- NO inference: absence of a microbe is not "depleted" unless stated;
  correlations with severity/treatment response are NOT case-control
  direction; claims the paper attributes to other studies do not count.
- Diversity metrics, enterotypes, and ratios (e.g. F/B ratio) are not
  taxa; skip them.
- If the paper reports no such claim, return an empty list.

Return JSON only:
[{"taxon": "...", "disease_as_stated": "...",
  "direction": "enriched"|"depleted",
  "evidence": "<the verbatim sentence(s) supporting it>",
  "confidence": "high"|"medium"}]
"high" = the direction is stated in one unambiguous sentence;
"medium" = assembled from two adjacent sentences or hedged wording.
```

## Quality control (the part that makes it publishable)

1. **Two independent passes per paper.** Ideally different models, or at
   minimum different prompt orderings/temperatures; the two passes must
   not see each other's output. (The pilot in this repository used the
   same model in two separately framed passes — state this limitation
   wherever the pilot is described; the full run should use two models.)
2. **Agreement filter.** Keep a tuple only when both passes produce the
   same (taxon at the same rank, disease, direction), matched after
   lowercasing and stripping strain suffixes. Everything else is
   discarded and counted.
3. **Error statement.** Report: papers processed, tuples in pass A,
   pass B, agreed tuples, and the disagreement rate
   (1 − agreed / union). This number accompanies the layer wherever it
   is shown and goes in the manuscript's AI-use statement.
4. **Confidence floor.** Drop tuples where both passes said "medium"
   unless full text was used.

## MONDO resolution (separate step, separately checked)

1. Map each agreed `disease_as_stated` to a MONDO id **within the atlas's
   1,104-node subtree** (the validator rejects ids outside it). Exact
   label match first, then synonym match, then manual assignment.
2. Claims whose disease has no node in the subtree are set aside and
   counted — they are not errors, just outside this atlas's disease scope.
3. Spot-check: a human (or an independent pass) reviews a random 20% of
   the resolutions, reported as resolution accuracy.

## Output and ingestion

Aggregate agreed tuples to one row per (taxon, MONDO id, direction) with
merged PMIDs, in the `associations.csv` format of `SCHEMA.md`, then:

```
python -I tools/validate_associations.py associations.csv data.json -o associations.js --label "pilot · abstract-only · double-pass agreed"
```

The `--label` text is displayed in the drawer header; use it to state the
layer's provenance and stage honestly ("pilot, abstract-only…" until the
full-text, two-model run replaces it).
