#!/usr/bin/env python3
"""Fail-closed publication-state checks for the PTBCC repository."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CANONICAL_NAME = "MachineLearning-Nerd"
CANONICAL_EMAIL = "MachineLearning-Nerd@users.noreply.github.com"
EXPECTED_BRANCHES = {
    "main",
    "baseline/validated-six-datasets",
    "baseline/frozen-runtime",
    "audit/exact-11-dataset-corpus",
    "audit/exact-baselines-ablation",
    "audit/legacy-fgbcc-semantics",
    "benchmark/cpu-runtime",
    "audit/claim-verifier",
}
EXPECTED_VERDICTS = {
    1: "VERIFIED",
    2: "VERIFIED",
    3: "BLOCKED",
    4: "BLOCKED",
    5: "BLOCKED",
}
REQUIRED_FILES = {
    "README.md",
    "STATUS.md",
    "claims.json",
    "CLAIM_EVIDENCE.md",
    "BRANCH_AUDIT.md",
    "SOURCE_AUDIT.md",
    "ENVIRONMENT.md",
    "CITATION.cff",
    "EVIDENCE_MANIFEST.json",
    "paper_2508.02123.pdf",
    "source/arxiv/2508.02123.tar",
    "source/Formatting-Instructions-LaTeX-2026.tex",
}


def run(*args: str) -> str:
    return subprocess.run(
        args,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()


def fail(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        fail(errors, (ROOT / relative).is_file(), f"missing required file: {relative}")

    claims_path = ROOT / "claims.json"
    if claims_path.is_file():
        claims = json.loads(claims_path.read_text())
        observed = {entry["id"]: entry["status"] for entry in claims["claims"]}
        fail(errors, set(observed) == {f"C{i}" for i in range(1, 6)}, "claims.json must contain C1-C5")
        fail(
            errors,
            all(observed.get(f"C{i}") == EXPECTED_VERDICTS[i] for i in range(1, 6)),
            "claims.json verdicts do not match the committed evidence contract",
        )

    for claim_id, expected in EXPECTED_VERDICTS.items():
        path = ROOT / ".openresearch" / "artifacts" / f"claim_{claim_id}" / "independent_checker.json"
        control_path = path.parent / "negative_control.json"
        if not path.is_file() or not control_path.is_file():
            errors.append(f"missing claim evidence for claim {claim_id}")
            continue
        result = json.loads(path.read_text())
        control = json.loads(control_path.read_text())
        fail(errors, result.get("claim_id") == claim_id, f"claim {claim_id} has the wrong id")
        fail(errors, result.get("verdict") == expected, f"claim {claim_id} verdict mismatch")
        fail(errors, result.get("valid_evidence") is True, f"claim {claim_id} evidence is invalid")
        fail(errors, control.get("rejected") is True, f"claim {claim_id} negative control was not rejected")

    manifest_path = ROOT / "EVIDENCE_MANIFEST.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text())
        fail(errors, set(manifest["expected_final_branches"]) == EXPECTED_BRANCHES, "manifest branch inventory mismatch")
        for entry in manifest["files"]:
            path = ROOT / entry["path"]
            if not path.is_file():
                errors.append(f"manifest file is missing: {entry['path']}")
                continue
            fail(errors, sha256(path) == entry["sha256"], f"manifest hash mismatch: {entry['path']}")

    try:
        branches = set(run("git", "for-each-ref", "--format=%(refname:strip=2)", "refs/heads").splitlines())
        fail(errors, branches == EXPECTED_BRANCHES, "local branch inventory does not match the final inventory")
        remote = run("git", "remote", "get-url", "origin").removesuffix(".git")
        fail(errors, remote == "https://github.com/MachineLearning-Nerd/icml26-annotator-prototype-learning", "origin URL is not the final repository")
        all_refs = run("git", "for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes/origin").splitlines()
        fail(errors, not any("/orx/" in ref for ref in all_refs), "legacy orx branch ref remains")
        commits = run("git", "rev-list", "--all").splitlines()
        for commit in commits:
            identity = run("git", "show", "-s", "--format=%an%x00%ae%x00%cn%x00%ce", commit)
            fields = identity.split("\x00")
            fail(
                errors,
                fields == [CANONICAL_NAME, CANONICAL_EMAIL, CANONICAL_NAME, CANONICAL_EMAIL],
                f"non-canonical identity in commit {commit}",
            )
        messages = run("git", "log", "--all", "--format=%B")
        fail(errors, "Co-authored-by:" not in messages and "Co-Authored-By:" not in messages, "co-author trailer remains")
    except subprocess.CalledProcessError as exc:
        errors.append(f"git publication-state check failed: {exc}")

    if errors:
        print("VERIFY_FINAL_FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VERIFY_FINAL_PASS: {len(REQUIRED_FILES)} required files, {len(EXPECTED_BRANCHES)} branches, {len(EXPECTED_VERDICTS)} claim contracts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
