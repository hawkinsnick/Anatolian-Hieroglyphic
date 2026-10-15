# Evidence and alternative-reading queries

This corpus exposes its existing native evidence through a checksum-pinned profile. The query layer preserves complete selected records and their source locators, uncertainties, editorial assertions and rights fields. It adds no new source acquisition, canonical reading, restoration, adjudication, source independence or expert acceptance.

## Use

Run from the repository root:

```sh
python scripts/evidence_query.py --coverage
python scripts/evidence_query.py --list 'digital-entry-dossiers'
python scripts/evidence_query.py --record 'EDIANA-HL-000' --collection 'digital-entry-dossiers'
python scripts/evidence_query.py --check
python scripts/test_native_evidence_query.py
```

Use exact native IDs. If an ID occurs in more than one view, specify `--collection`. Absence from these selected views does not establish absence from the full corpus, scholarship or historical record.

## Declared native views

| View | Records | Native unit | Scope |
|---|---:|---|---|
| digital-entry-dossiers | 287 | digital text-entry dossier | Bibliographic locators and discovery candidates are not critical readings. |
| edition-metadata-pilot | 7 | edition metadata pilot entry | No inferred join to other ID systems. |
| disagreement-register | 4 | research disagreement/control item | Period conflict and unknown assignments retain source scope. |

Counts overlap and must not be added as unique inscriptions, objects or independent witnesses. The coverage report deliberately leaves alternative-pair and independent-witness counts unknown; a comparison register can include reported, dependent or unaligned assertions.

## Trace a claim

Each dossier returns `native_record` unchanged, the repository path, exact JSON pointer and file SHA-256. It also returns any records linked by specifically declared equal native keys. Such links are editorial associations, not certified physical equivalence or source independence. Read source authorship, locators, inspection state, uncertainty and rights in the native record and its context.

The profile lists additional source, rights and disagreement registers. These are corpus-level context pointers: inclusion does not mean every register asserts facts about the queried record. Retrieve an exact existing claim with:

```sh
python scripts/evidence_query.py --artifact 'research/digital-entry-dossiers.json' --pointer '/entries'
```

Pointers use RFC 6901 escaping (`~1` for slash, `~0` for tilde). JSONL artifacts are viewed as arrays of nonempty source lines; CSV fields remain source strings. Context envelopes omit array-valued siblings; use `--artifact` to retrieve those siblings and their full qualifications. Nothing is fetched from the network or from private gold/calibration files.

## Corpus-specific limits

- Bibliographic citations marked direct_edition_checked=false remain uninspected leads. Secondary label matching does not certify chronology or physical object identity.

## Further scholarly work

For each proposed alternative, identify the author or edition, precise page/plate/position, literal reading, consultation state, source lineage and reuse terms. Distinguish observed damage, supplied text, segmentation, transliteration conventions, source-reported analysis and project hypotheses. Align the same locus before comparing readings. Keep unresolved attribution and alignment explicit. Existing register entries must not be promoted to completed collation merely because they are searchable.

The profile and report are `research/evidence-query-profile.json` and `analysis/evidence-query-coverage.json`. Source pins fail closed: changes to a registered source require inspecting the change, updating its profile pin, regenerating coverage and rerunning tests. Hashes establish byte identity, not historical truth. Source-specific rights prevail over project licenses; this interface grants no new extraction or redistribution permission.
