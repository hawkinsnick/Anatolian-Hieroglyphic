# Full dossier coverage in the combined corpus

The combined corpus now declares all 287 source-bound eDiAna digital-entry dossiers in `research/digital-entry-dossiers.json`. It replaces the previous 19 observed-ID rows and 32 portable-subset rows as the collection's enumerated view. Those earlier registers remain qualification/context inputs; their identifiers overlap the full layer and must not be added as new objects.

This expands combined access to existing reconciled evidence, not the native inscription population. Each dossier retains its eDiAna ID, source label, principal-reference fields, unverified edition locators, explicit object-class basis, secondary period candidates and source-dependence edges. The source snapshots and `analysis/current-status.json` are bound to the collection work ledger and AI bundle. Use `python scripts/reconcile.py` and `python scripts/build_collection_handoff.py` to replay their provenance offline.

No protected linguistic text or image is imported. Bibliographic fields are attributed to eDiAna and are not direct CHLI collation. Digital text groups and fragment labels stay intact; physical object totals, group decomposition and scientific acceptance remain unresolved. The 255 dossiers without an explicit supported object-class assertion remain unknown. Missing class never implies a monumental inscription.

Next substantive work: authority-supported classification and explicit aliases/group membership, then lawful direct CHLI I/III edition comparison. Metadata completeness is not reading completeness, chronological certainty or independent review.
