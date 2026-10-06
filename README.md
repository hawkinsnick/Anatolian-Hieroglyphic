# Anatolian Hieroglyphic Corpus

A provenance-first, machine-readable research corpus for Anatolian (Luwian) Hieroglyphic inscriptions.

## Scholarly scope

This project separates **physical objects**, **inscription/document identities**, **edition witnesses**, **sign/transliteration assertions**, and **linguistic interpretation**. It does not treat a digital corpus as an independent epigraphic witness and does not infer relationships to Aegean scripts from graphic resemblance.

### Initial source spine

The first acquisition target is the eDiAna Luwian-hieroglyphic corpus, whose project documentation states that Hawkins 1995 and Hawkins 2000 form the basic Empire and Post-Empire corpora. Those works remain bibliographic authorities; redistribution rights must be assessed source by source.

## Pre-Expert Maximum

Before expert adjudication, the project will exhaust lawful catalogue discovery, object/edition concordance, provenance, chronology, bibliography, sign-label lineage, source dependence, deterministic validation and explicit uncertainty. Disputed readings and palaeographic/linguistic judgments remain human-review gates.

See `research/pre-expert-maximum.json`, `docs/ROADMAP.md`, and `ai-skill/SKILL.md`.

## 2.0.0 milestone

All **287 eDiAna digital entries** now have explicit [identity and bibliography dossiers](docs/DIGITAL-ENTRY-DOSSIERS.md). These carry 274 bibliographic assertions on 262 entries, typed internal references/notices, 32 object classes and 118 secondary period candidates. One period conflict is preserved. Physical-object counts and direct edition verification remain open.

See [current assessment](docs/PRE-EXPERT-STATUS.md). Validate offline with `python scripts/reconcile.py` and `python -m pytest -q`.


## Offline corpus browser
Run `python scripts/build_corpus_browser.py` to generate `workbench/corpus-browser.html`. It searches only files explicitly admitted by `research/browser-sources.json`. Browser admission requires rights/provenance review; never recursively ingest restricted or raw upstream material. Display does not establish decipherment, source independence, or expert validation.
