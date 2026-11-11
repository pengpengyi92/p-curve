"""Offline repository contracts, not a security audit or a complete YAML parser.

These tests check the local targets of ordinary inline Markdown links (not remote
URLs or heading anchors), required contribution-field IDs and precedent-record
consistency. GitHub's hosted form rendering requires separate verification.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
INITIAL_TOPICS = {
    "ns_nss_given_parameters",
    "continuous_zero_discount_factor",
    "period_forward",
    "linear_zero_interpolation",
    "fixed_cashflow_pv",
    "parallel_dv01",
    "key_rate_zero_node_risk",
    "dated_sovereign_curve_archive",
}


def prose_without_fenced_code(text: str) -> str:
    """Exclude conventional fenced examples so example syntax is not a link."""
    lines = []
    fence = None
    for line in text.splitlines():
        stripped = line.lstrip()
        marker = "```" if stripped.startswith("```") else "~~~" if stripped.startswith("~~~") else None
        if marker:
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return "\n".join(lines)


class RepositoryContractTests(unittest.TestCase):
    def test_release_boundary_documents_exist(self):
        required = (
            "README.md", "AGENTS.md", "LICENSE", "CONTRIBUTING.md",
            "SECURITY.md", "docs/PUBLICATION_POLICY.md",
            "docs/OPEN_SOURCE_PRECEDENTS.md", "BENCHMARK_CARD.md", "TODO.md",
            "CHANGELOG.md", ".github/PULL_REQUEST_TEMPLATE.md",
        )
        for name in required:
            with self.subTest(path=name):
                path = ROOT / name
                self.assertTrue(path.is_file(), f"missing release boundary document: {name}")
                self.assertTrue(path.read_text(encoding="utf-8").strip())

    def test_inline_local_markdown_targets_exist_inside_repository(self):
        # Deliberately not a full Markdown parser or remote URL/anchor validator.
        documents = [*ROOT.glob("*.md"), *(ROOT / "docs").rglob("*.md"),
                     *(ROOT / "log").rglob("*.md"), ROOT / ".github/PULL_REQUEST_TEMPLATE.md"]
        pattern = re.compile(r"!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)")
        for document in documents:
            body = prose_without_fenced_code(document.read_text(encoding="utf-8"))
            for raw in pattern.findall(body):
                target = raw[1:-1] if raw.startswith("<") else raw
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                resolved = (document.parent / unquote(parsed.path)).resolve()
                with self.subTest(document=str(document.relative_to(ROOT)), target=target):
                    self.assertTrue(resolved.is_relative_to(ROOT), "local link escapes repository")
                    self.assertTrue(resolved.exists(), f"broken local Markdown target: {target}")

    def test_issue_form_contract_fields_are_present(self):
        # Field-ID checks preserve required review inputs, without pretending to
        # parse YAML or implement GitHub's entire issue-form schema in stdlib.
        required_ids = {
            "curve_proposal.yml": {"problem", "conventions", "precedent", "rights", "verification", "safeguards"},
            "repository_recommendation.yml": {"url", "relevance", "license", "evidence", "relationship", "disclosure", "safety"},
            "bug_report.yml": {"environment", "reproduction", "expected", "actual", "safety"},
            "research_discussion.yml": {"question", "sources", "protocol", "limits"},
        }
        template_root = ROOT / ".github/ISSUE_TEMPLATE"
        for name, expected in required_ids.items():
            text = (template_root / name).read_text(encoding="utf-8")
            ids = re.findall(r"^    id: ([a-z_]+)\s*$", text, re.MULTILINE)
            with self.subTest(template=name):
                self.assertEqual(len(ids), len(set(ids)), "duplicate issue-form field ID")
                self.assertTrue(expected.issubset(ids), f"missing contribution contract fields: {expected - set(ids)}")
                for key in ("name:", "description:", "body:"):
                    self.assertRegex(text, rf"(?m)^{re.escape(key)}")

    def test_precedent_records_cover_initial_topics_without_export_shortcut(self):
        record = json.loads((ROOT / "data/open_source_precedents.json").read_text(encoding="utf-8"))
        self.assertEqual(record["schema_version"], "1.0.0")
        rule = record["publication_gate"]
        self.assertIs(rule["same_topic_public_precedent_required"], True)
        self.assertEqual(rule["no_verified_precedent"], "HOLD")
        self.assertIs(rule["precedent_is_sufficient_for_export"], False)
        sources = {source["id"]: source for source in record["sources"]}
        self.assertEqual(len(sources), len(record["sources"]), "duplicate source ID")
        for source in sources.values():
            with self.subTest(source=source["id"]):
                url = urlsplit(source["canonical_url"])
                self.assertEqual(url.scheme, "https")
                self.assertTrue(url.netloc)
                self.assertRegex(source["reviewed_commit"], r"^[0-9a-f]{40}$")
                # A reviewed custom license may legitimately have no exact SPDX ID.
                self.assertTrue(source["license_label"] and source["license_path"])
                self.assertTrue(source["implementation_paths"])
                self.assertEqual(source["relationship"], "TOPIC_PRECEDENT_ONLY_NOT_DEPENDENCY_NOT_BENCHMARK")
                self.assertIs(source["code_copied"], False)
        gates = {gate["topic"]: gate for gate in record["topic_gates"]}
        self.assertEqual(len(gates), len(record["topic_gates"]), "duplicate topic gate")
        self.assertEqual(set(gates), INITIAL_TOPICS, "scope changes need explicit gate/test review")
        for topic, gate in gates.items():
            with self.subTest(topic=topic):
                self.assertEqual(gate["status"], "PRECEDENT_FOUND")
                self.assertTrue(gate["sources"])
                self.assertTrue(set(gate["sources"]).issubset(sources), "unknown source reference")
                self.assertTrue(any(topic in sources[key]["covered_topics"] for key in gate["sources"]),
                                "topic lacks a directly mapped implementation precedent")


if __name__ == "__main__":
    unittest.main()
