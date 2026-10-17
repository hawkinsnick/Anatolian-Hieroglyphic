# Luwian research pilot: trace edition evidence before comparing signs

The proposed specialist use is to compare the attestations and interpretations of a Luwian sign or word. **The admitted layer here contains identity/bibliographic metadata, not an executable sign-reading corpus.** This pilot makes the evidence route and its missing prerequisites concrete. No academic has requested, participated in or endorsed it.

## Follow the documentary example

1. Open [the executed seven-case packet](../analysis/task-pilot-example.json).
2. Read `summary`: seven native metadata dossiers, all seven with reported edition locators; zero direct-edition checks performed by this pilot; sign-reading pilot executed is false. These seven overlap other native views and must not be added to the 287 digital-entry dossiers as new inscriptions.
3. Find `KOCAOĞUZ`. Its preserved `period` is `TRANSITION? / disputed`, not an adjudicated date. The packet reports the CHLI III route `pp.70–72, plate 46`. This is a reported locator, not a statement that the underlying pages were consulted in this pilot.
4. Inspect `source_locator`: exact repository path, file hash and JSON pointer `/records/0`. This locates a project metadata assertion, not an ancient sign or independently checked edition passage.
5. Read `next_research_step` and `review_question` for each case. Object identity, chronology, reading and source dependence require separate judgments.
6. `accepted_reading` is null in every case. No preferred sign value, translation or word analysis follows from metadata.

## Reproduce and inspect the native evidence

Download and extract the GitHub ZIP, open a terminal in its root and use Python 3.12:

```sh
python scripts/evidence_query.py --check
python scripts/task_pilot.py --check
python scripts/test_task_pilot.py
python scripts/evidence_query.py --record 'KOCAOĞUZ' --collection edition-metadata-pilot
```

The last command returns the unchanged native record with evidence/rights context. Use its exact Unicode identifier; do not join it to another identifier system by string similarity. The task packet binds both the metadata source and rights register by SHA-256. Byte identity does not establish historical truth.

## What unlocks the sign-reading study

For one bounded sign or word, obtain admissible reading-level evidence with author/edition, exact page/line/sign locus, original notation, alternative analyses, consultation state and intended-use rights. Keep the historical edition assertion separate from present physical-object verification. Do not reconstruct CHLI text, drawings or sign tables from derivative sites to avoid a rights barrier.

Only after those inputs are admitted should the study enumerate attestations, align competing readings at the same locus and compare linguistic analyses. Do not infer that all scholars or all existing tools lack these capabilities: the gap described here is in this project's admitted layer.

## AI and expert-review use

Supply the individual skill and seven-case packet and ask:

> Explain what the KOCAOĞUZ metadata asserts, where that assertion is recorded, and which evidence is still needed for a sign-reading comparison. Preserve the disputed period, distinguish reported locators from consulted editions, and do not invent a reading or independent witness.

Expected: documentary routing only, disputed chronology preserved, no sign-reading result. This is an acceptance criterion, not an empirical LLM evaluation.

Review status is PREPARED_NOT_REVIEWED. Ask a qualified reviewer to verify a specific reported edition locator using the actual source, recording the consulted version/locus, access/rights, expertise/conflicts, reasoning, dissent and maintainer decision. A submitted form or software pass does not certify expertise or adopt a reading.

Native [rights controls](../research/rights-source-matrix.json), [source lineage](../research/source-lineage.json) and [research-delivery controls](RESEARCH-DELIVERY.md) remain governing. This pilot adds no protected transcription, photograph, sign table, linguistic annotation or new reuse permission.


Subsequent bounded source work: [Source study and specialist handoff](SOURCE-STUDY-2026-10-17.md). Its scope and evidence are separate from this historical pilot.
