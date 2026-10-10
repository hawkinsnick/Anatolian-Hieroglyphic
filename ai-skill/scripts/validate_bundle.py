#!/usr/bin/env python3
"""Validate Anatolian Hieroglyphic native input hashes; not master-contract certification."""
import hashlib, json, pathlib, sys
root = pathlib.Path(__file__).resolve().parents[2]
index = json.loads((root / "ai-skill/generated/research-bundle-index.json").read_text())
manifest = json.loads((root / "ai-skill/manifest.json").read_text())
errors = []
if manifest.get("master_contract_0_3_1") != "NOT_CERTIFIED":
    errors.append("master contract unexpectedly certified")
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
print("PASS: native listed-input integrity; master contract NOT CERTIFIED")
