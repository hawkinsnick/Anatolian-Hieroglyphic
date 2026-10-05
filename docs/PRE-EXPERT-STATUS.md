# Pre-expert status — 2.0.0

The complete 287-entry eDiAna digital identity spine is now explicit and reproducible. Each entry has a dossier, stable source link, bibliography status, source-dependence edges and explicit unknowns.

The captured principal-reference fields supply 274 bibliographic assertions on 262 entries, 71 internal cross-reference assertions and three source notices. Seven entries have empty reference fields. This is an attributed bibliography register, not direct CHLI edition collation or a claim of current-edition completeness.

Thirty-two entries have object-class assertions from explicit siglum wording. The remaining 255 stay unknown. Exact label matches to Hittite Monuments provide secondary period candidates for 118 entries. KARKAMIŠ A30h has conflicting Transition and Late assertions; both survive. The other 169 entries have no accepted period candidate. Period ranges and question marks retain their source meaning; ranges and aliases are never expanded automatically.

There are no admitted canonical physical objects, new readings or expert-verified records. A digital entry may combine or subdivide physical objects and textual units. The physical denominator remains unknown.

The next machine milestone is authority-supported object and period attribution, explicit identity/group concordance, and direct CHLI I/III edition reconciliation. Disputed readings, sign identifications and linguistic interpretation remain expert gates. Source access limitations are recorded per task and do not stop other acquisition work.

See [all dossiers](DIGITAL-ENTRY-DOSSIERS.md), `analysis/current-status.json` and `scripts/reconcile.py`. Run `python scripts/reconcile.py` and `python -m pytest -q` for offline checks. Refresh metadata explicitly with `python scripts/acquire_metadata.py` (requires beautifulsoup4); review source drift before replacing the captured baseline. The live API may return linguistic content; the acquisition script discards it and saves only identifier/bibliographic metadata and hashes.
