"""Fail closed on unreviewed files/topics; heuristic scans do not prove secrecy.

This script does not contact any service, change files, or approve publication.
Run after initializing this independent repository and before each public push.
"""

import ast
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def check() -> list[str]:
    errors = []
    manifest = json.loads((ROOT / "publication_manifest.json").read_text(encoding="utf-8"))
    files = manifest["files"]
    if len(files) != len(set(files)):
        errors.append("duplicate allowlist entry")
    if not (ROOT / ".git").exists():
        return ["initialize an independent repository before checking publication"]
    inventory = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT, check=True, capture_output=True,
    ).stdout.decode("utf-8").split("\0")
    actual = {p for p in inventory if p}
    expected = set(files)
    for path in sorted(actual - expected):
        errors.append(f"unapproved file: {path}")
    for path in sorted(expected - actual):
        errors.append(f"allowlisted file missing from public inventory: {path}")
    patterns = [
        ("private repository URL", re.compile(r"https?://github\.com/[^/\s]+/(?:PFICC|P-University)(?:[/#?]|\b)", re.I)),
        ("absolute Windows path", re.compile(r"\b[A-Z]:[\\/]")),
        ("credential-like token", re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})")),
        ("private key", re.compile(r"-----BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY-----")),
    ]
    for name in files:
        path = ROOT / name
        if not path.is_file():
            errors.append(f"not a file: {name}")
            continue
        if path.is_symlink() or ROOT not in path.resolve().parents:
            errors.append(f"file escapes repository: {name}")
            continue
        raw = path.read_bytes()
        if len(raw) > 512_000:
            errors.append(f"unexpectedly large export: {name}")
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"non-UTF8 export not approved: {name}")
            continue
        for label, pattern in patterns:
            if pattern.search(content):
                errors.append(f"{label}: {name}")
        if name.startswith("src/") and name.endswith(".py"):
            tree = ast.parse(content, filename=name)
            # Small initial stdlib math package: no network/filesystem/account integration.
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    modules = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    modules = [] if node.level else [node.module or ""]
                else:
                    continue
                for module in modules:
                    if module.split(".")[0] not in {"__future__", "math", "typing"}:
                        errors.append(f"runtime import outside initial allowlist: {name}: {module}")
    precedents = json.loads((ROOT / "data/open_source_precedents.json").read_text(encoding="utf-8"))
    if precedents["publication_gate"]["precedent_is_sufficient_for_export"] is not False:
        errors.append("public precedent must not imply export approval")
    sources = {s["id"]: s for s in precedents["sources"]}
    topics = {t["topic"]: t for t in precedents["topic_gates"]}
    for topic in manifest["approved_topics"]:
        gate = topics.get(topic, {})
        if gate.get("status") != "PRECEDENT_FOUND" or not gate.get("sources"):
            errors.append(f"no reviewed precedent; HOLD: {topic}")
        for source_id in gate.get("sources", []):
            source = sources.get(source_id, {})
            if not re.fullmatch(r"[0-9a-f]{40}", source.get("reviewed_commit", "")):
                errors.append(f"source not pinned: {source_id}")
            if not source.get("license_path") or not source.get("implementation_paths"):
                errors.append(f"source lacks license/implementation evidence: {source_id}")
            if source.get("code_copied") is not False:
                errors.append(f"third-party copy outside initial approval: {source_id}")
    archive_dir = ROOT / "curve"
    if archive_dir.is_dir():
        spec = importlib.util.spec_from_file_location("reviewed_curve_archive", ROOT / "scripts/curve_archive.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for snapshot_path in sorted(archive_dir.glob("*/snapshot.json")):
            try:
                snapshot = module.load_snapshot(snapshot_path)
                module.validate_snapshot(snapshot, public=True)
                if snapshot_path.parent.name != snapshot["snapshot_id"]:
                    raise ValueError("snapshot ID differs from directory")
                for name in ["index.html", *[m["id"] + ".svg" for m in snapshot["markets"]]]:
                    if not (snapshot_path.parent / name).is_file():
                        raise ValueError("missing archived artifact: " + name)
            except (ValueError, OSError) as exc:
                errors.append(f"public archive rejected: {snapshot_path.parent.name}: {exc}")
    return errors


if __name__ == "__main__":
    failures = check()
    if failures:
        print("PUBLICATION CHECK FAILED\n" + "\n".join(failures), file=sys.stderr)
        raise SystemExit(1)
    print("PASS: exact public file/topic allowlists and bounded heuristic scans; human review still required")
