#!/usr/bin/env python3
"""Validate Anatolian Hieroglyphic native input hashes; not master-contract certification."""
import hashlib, json, pathlib, sys
root = pathlib.Path(__file__).resolve().parents[2]
index = json.loads((root / "ai-skill/generated/research-bundle-index.json").read_text())
manifest = json.loads((root / "ai-skill/manifest.json").read_text())
errors = []
if manifest.get("master_contract_0_3_1") != "IMPLEMENTED":
    errors.append("master contract adapter missing")
inputs = index.get("authoritative_inputs", [])
hashes = index.get("input_sha256", {})
if not inputs or not hashes:
    errors.append("missing native inputs or input hashes")
for path in inputs:
    p = (root / path).resolve()
    if not p.is_relative_to(root.resolve()) or not p.is_file():
        errors.append("missing or unsafe input: " + path)
        continue
    if path in hashes and hashlib.sha256(p.read_bytes()).hexdigest() != hashes[path]:
        errors.append("input SHA-256 mismatch: " + path)
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("PASS: native listed-input integrity; native integrity; fleet contract replay follows")

import runpy
runpy.run_path(str(root / "ai-skill/scripts/fleet_contract.py"))["replay"]()

# Native dependency policies are checked as part of every AI bundle validation.
import pathlib as _guard_pathlib, runpy as _guard_runpy
_guard_root=_guard_pathlib.Path(__file__).resolve().parents[2]
_guard_runpy.run_path(str(_guard_root/'scripts/check_cross_corpus_dependencies.py'))['validate'](_guard_root)
