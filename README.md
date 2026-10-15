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


## Linear A method-parity gate
Anatolian Hieroglyphic has reached the machine-resolvable method-parity baseline for its current lawful identity/bibliography layer: 287 digital entries, explicit source dependence, disagreement/rights controls, browser/API/exports, validation and expert boundaries. Read `docs/RIGHTS-ONLY-READINESS.md` and `research/residual-blocker-ledger.json`. Do not convert digital entries into physical-object counts, treat eDiAna/Hawkins as independent witnesses, or reconstruct protected CHLI readings/sign apparatus from derivative sources. Further material critical-corpus growth is rights/access bound.

Fleet research-contract implementation and replay: [admission guide](docs/FLEET-ADMISSION.md).

## AI integrity checkpoint — 2026-10-11

[AI integrity controls](docs/AI-INTEGRITY.md) document source-bound bundle publication and checked cross-corpus dependency safeguards. Reading coverage and scholarly acceptance are unchanged.

## Coverage expansion — 2026-10-12

Use the full 287-row digital-entry dossier view for combined queries and API/export access. Treat prior observed-ID and portable-subset registers as overlapping context. Preserve unknown classes, period candidates, source notices and unverified edition locators; do not infer physical object identity or reading completeness.

See [docs/COVERAGE-EXPANSION-2026-10-12.md](docs/COVERAGE-EXPANSION-2026-10-12.md).

## Evidence and alternative-reading queries

[Query source evidence and unresolved alternatives](docs/EVIDENCE-AND-ALTERNATIVES.md) using exact native IDs, full source records, pinned artifact locators and explicit corpus-specific scope. [Coverage by native view](analysis/evidence-query-coverage.json) keeps catalogue entries, reading versions, assertions and research issues distinct. This interface adds no source collation, canonical reading or expert acceptance.
