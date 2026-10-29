"""Validate a microbe-disease association table against the atlas data and
emit associations.js for the site. See SCHEMA.md for the input format.

Usage:
  python -I tools/validate_associations.py associations.csv data.json [-o associations.js]

Exit 0 with no emitted file (and a note) when the CSV does not exist - the
site ships without the associations layer by design until the extraction
arrives. Any validation error exits 1 and emits nothing.
"""
import csv, json, os, sys

def main(argv):
    args = [a for a in argv if not a.startswith('-o')]
    out = None
    if '-o' in argv:
        out = argv[argv.index('-o') + 1]
        args = [a for a in argv if a != '-o' and a != out]
    if len(args) != 2:
        print(__doc__); return 1
    csv_path, data_path = args
    if not os.path.exists(csv_path):
        print('no associations file at %r - the site ships without the drawer (by design).' % csv_path)
        return 0
    data = json.loads(open(data_path, 'rb').read())
    mondo_by_id = {n['id']: i for i, n in enumerate(data['mondoNodes'])}
    pmid_field = data['fields'].index('pmid')
    paper_by_pmid = {}
    for i, p in enumerate(data['papers']):
        if p[pmid_field]:
            paper_by_pmid.setdefault(str(p[pmid_field]), i)

    rows, errors, warnings, seen = [], [], [], {}
    with open(csv_path, newline='', encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        need = {'taxon', 'mondo_id', 'direction', 'pmids'}
        if not need.issubset(set(rdr.fieldnames or [])):
            print('ERROR: header must include %s (got %s)' % (sorted(need), rdr.fieldnames)); return 1
        for ln, r in enumerate(rdr, start=2):
            taxon = (r['taxon'] or '').strip()
            mid = (r['mondo_id'] or '').strip()
            d = (r['direction'] or '').strip().lower()
            if not taxon: errors.append('line %d: empty taxon' % ln); continue
            if d not in ('enriched', 'depleted'):
                errors.append('line %d: direction %r is not enriched|depleted' % (ln, r['direction'])); continue
            if mid not in mondo_by_id:
                errors.append('line %d: %s is not a node of the atlas MONDO subtree' % (ln, mid)); continue
            idxs, missing = [], []
            for pm in (r['pmids'] or '').replace(' ', '').split(';'):
                if not pm: continue
                (idxs if pm in paper_by_pmid else missing).append(
                    paper_by_pmid.get(pm, pm))
            if missing:
                warnings.append('line %d: %d PMID(s) not in the atlas, dropped: %s' % (ln, len(missing), ','.join(missing)))
            if not idxs:
                errors.append('line %d: no supporting paper is in the atlas' % ln); continue
            key = (taxon.lower(), mid, d)
            if key in seen:
                seen[key]['papers'] = sorted(set(seen[key]['papers']) | set(idxs))
                warnings.append('line %d: duplicate of (%s, %s, %s) - PMIDs merged' % (ln, taxon, mid, d))
                continue
            rec = {'taxon': taxon, 'mondo': mondo_by_id[mid], 'dir': d,
                   'papers': sorted(set(idxs))}
            note = (r.get('note') or '').strip()
            if note: rec['note'] = note
            seen[key] = rec; rows.append(rec)

    for w in warnings: print('warning:', w)
    for e in errors: print('ERROR:', e)
    if errors:
        print('%d error(s): nothing emitted.' % len(errors)); return 1
    print('%d association(s) valid (%d enriched, %d depleted), %d disease(s), %d taxa.' % (
        len(rows), sum(r['dir'] == 'enriched' for r in rows),
        sum(r['dir'] == 'depleted' for r in rows),
        len({r['mondo'] for r in rows}), len({r['taxon'].lower() for r in rows})))
    if out:
        js = 'window.ASSOC =\n' + json.dumps(rows, ensure_ascii=False, indent=1) + '\n;\n'
        assert json.loads(js[len('window.ASSOC =\n'):-len('\n;\n')]) == rows
        open(out, 'w', encoding='utf-8').write(js)
        print('wrote', out)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
