# Attribution review

All four controls retain period unknowns/conflicts, fragment units and Hawkins-derived editorial lineage. Metadata reconciliation is not direct edition collation.

Existing source consultation receipts and limits are inherited exactly from the referenced native packets. This pass inspects those packets, not the underlying publications afresh. No exhaustive literature search, new autopsy or independent review is claimed.

The complete selections below name the finite native collections reviewed. Other repository records and the broader literature are outside this checkpoint. Case counts are review tasks, not inscriptions, independent witnesses or fully attributed alternative pairs.

| Complete native selection | Rows |
|---|---:|
| `research/disagreement-register.json/items` | 4 |

Use the case query to read the finding together with the complete native evidence, including any named author/publication, source locator, inspection state, qualification and source dependence. Missing metadata stays missing; a source ID alone is not proof of direct consultation.

```sh
python scripts/attribution_review.py --check
python scripts/attribution_review.py --case 'AH-DIS-001'
python scripts/evidence_query.py --list attribution-review
```

| Review ID | Type | Finding | Remaining work |
|---|---|---|---|
| AH-DIS-001 | CLASSIFICATION | A preserved period conflict and unknown assignments do not constitute two directly consulted scholarly chronologies. | Recover exact per-record source assertions and consultation states; do not infer dates from ordering. |
| AH-DIS-002 | COUNT_OR_IDENTITY | Grouped sigla, blocks, fragments, texts and digital entries are not interchangeable entities. | Use edition-specific inventory and joining evidence for each relation. |
| AH-DIS-003 | SOURCE_ROLE | eDiAna explicitly adjusts its Hawkins-derived transliterations; repetition is not independent confirmation. | Collate both exact edition loci before describing reading agreement. |
| AH-DIS-004 | COVERAGE_GAP | Edition access is still a prerequisite for disputed sign/variant reconciliation. | Acquire lawful editions and exact sign contexts; authority-specific inventories remain separate. |

`research/attribution-review.json` pins every referenced native artifact by SHA-256 and records exact JSON pointers. `analysis/attribution-review-audit.json` is replayed by the checker. Queries reject changed input bytes before returning any case. The earlier native records remain unchanged.

Pair-attribution states describe documentary limitations, not scientific acceptance. A partial located comparison can be a real scholarly alternative without full typographic, physical-position or independent collation. `NOT_APPLICABLE` marks controls and interpretations for which a two-reading pair is not the appropriate unit. No unknown pair/witness total is replaced with zero.
