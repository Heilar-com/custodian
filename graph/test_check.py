#!/usr/bin/env python3
"""Tests for graph/check.py. Run with:  python3 graph/test_check.py

Standard library only (unittest). The fixtures are synthetic; they exist to exercise the
schema checks and the four independence rules, which the seed graph does not all trigger.
"""

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check  # noqa: E402


def node(nid, ntype, tier, provenance="p", status="active", links=None, extra=None):
    n = {
        "id": nid, "type": ntype, "label": nid, "created": "2026-10-24", "provenance": provenance,
        "status": status, "verification_tier": tier, "verification_status": "confirmed",
        "retention": "permanent",
    }
    if ntype == "source":
        n["links"] = links or [f"https://example.org/{nid}"]
    if extra:
        n.update(extra)
    return n


def edge(eid, etype, src, dst, status="active"):
    return {"id": eid, "type": etype, "from": src, "to": dst, "created": "2026-10-24",
            "provenance": "e", "status": status}


def run(data, *args):
    """Write data to a temp file, run check.main on it, return (exit code, stdout)."""
    import yaml
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "g.yaml"
        path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = check.main([str(path), *args])
        written = path.read_text(encoding="utf-8")
    return code, out.getvalue(), written


class ValidationTests(unittest.TestCase):
    def test_clean_file_passes(self):
        data = {"nodes": [node("src:a", "source", "preprint"), node("clm:c", "claim", "preprint")],
                "edges": [edge("e:1", "supports", "src:a", "clm:c")]}
        code, out, _ = run(data, "--strict")
        self.assertEqual(code, 0, out)
        self.assertIn("errors: 0   warnings: 0", out)

    def test_errors_are_reported_per_item(self):
        bad = node("clm:b", "claimx", "blog", provenance="", status="open")
        bad["label"] = ""
        bad["created"] = "24-10-2026"
        bad["verification_status"] = "checked"
        bad["retention"] = "soon"
        data = {"nodes": [
                    node("src:a", "source", "n/a", extra={"links": None}),
                    node("src:a", "source", "preprint"),
                    bad,
                    node("clm:c", "claim", "n/a"),
                    node("src:ok", "source", "preprint"),
                ],
                "edges": [
                    edge("e:1", "supports", "src:a", "clm:c"),
                    edge("e:2", "likes", "clm:c", "clm:c", status="maybe"),
                    edge("e:3", "cites", "clm:c", "clm:missing"),
                    edge("e:1", "cites", "clm:c", "src:a"),
                    edge("e:4", "supports", "src:ok", "clm:c"),
                ]}
        del data["nodes"][0]["links"]
        del data["edges"][2]["provenance"]
        code, out, _ = run(data, "--no-report")
        self.assertEqual(code, 1)
        for needle in (
            "node src:a: verification_tier `n/a` is not allowed on a source",
            "node src:a: source node has no `links`",
            "node src:a: duplicate id",
            "node clm:b: type `claimx` is not a schema node type",
            "node clm:b: `label` must be a non-empty string",
            "node clm:b: `created` must be an ISO 8601 date",
            "node clm:b: `provenance` must be a non-empty string",
            "node clm:b: status `open` not in",
            "node clm:b: verification_tier `blog` not in",
            "node clm:b: verification_status `checked` not in",
            "node clm:b: `retention` must be `permanent` or an ISO date",
            "edge e:2: type `likes` is not a schema edge type",
            "edge e:2: status `maybe` not in",
            "edge e:2: self-loop on `clm:c`",
            "edge e:3: missing required property `provenance`",
            "edge e:3: `to` points at unknown node `clm:missing`",
            "edge e:1: duplicate id",
            # clm:c has tier n/a but an active support from a preprint source
            "node clm:c: verification_tier is `n/a` but it has active supports",
        ):
            self.assertIn(needle, out, needle)

    def test_retention_accepts_iso_date_and_rejects_other_text(self):
        ok = node("clm:c", "claim", "n/a", extra={"retention": "2027-01-01"})
        ok["verification_status"] = "not-verified"
        code, out, _ = run({"nodes": [ok], "edges": []}, "--strict", "--no-report")
        self.assertEqual(code, 0, out)

    def test_disputed_consistency_is_a_warning_not_an_error(self):
        data = {"nodes": [node("clm:a", "claim", "preprint", status="disputed"),
                          node("clm:b", "claim", "preprint"),
                          node("clm:c", "claim", "preprint")],
                "edges": [edge("e:1", "contradicts", "clm:a", "clm:b")]}
        code, out, _ = run(data, "--no-report")
        self.assertEqual(code, 0)
        self.assertIn("node clm:a: status `disputed` but no active contradicts edge points at it", out)
        self.assertIn("node clm:b: is the target of an active contradicts edge but its status is `active`", out)
        code, _, _ = run(data, "--no-report", "--strict")
        self.assertEqual(code, 1)


class AxiomRuleTests(unittest.TestCase):
    """Mirrors the schema's example subgraph: preprint P, journal version S1 (same-as P),
    news story S2 that cites the paper, a summary derived from P, and an independent S3."""

    def fixture(self):
        nodes = [
            node("src:p", "source", "preprint", provenance="p1"),
            node("src:s1", "source", "peer-reviewed-journal", provenance="p2"),
            node("src:s1-copy", "source", "news-outlet", provenance="p3"),
            node("src:s2", "source", "news-outlet", provenance="p4"),
            node("src:summary", "source", "institutional-report", provenance="p5"),
            node("src:summary2", "source", "news-outlet", provenance="p6"),
            node("src:s3", "source", "institutional-report", provenance="p7"),
            node("src:na", "source", "creator-content", provenance="p8"),
            node("clm:c1", "claim", "peer-reviewed-journal"),
            node("clm:c2", "claim", "institutional-report"),
        ]
        edges = [
            edge("e:1", "supports", "src:p", "clm:c1"),
            edge("e:2", "supports", "src:s1", "clm:c1"),
            edge("e:3", "supports", "src:s1-copy", "clm:c1"),
            edge("e:4", "supports", "src:s2", "clm:c1"),
            edge("e:5", "supports", "src:summary", "clm:c1"),
            edge("e:6", "supports", "src:s3", "clm:c1", status="withdrawn"),
            edge("e:7", "same-as", "src:p", "src:s1"),
            edge("e:8", "same-as", "src:s1", "src:s1-copy"),          # chain: p ~ s1 ~ s1-copy
            edge("e:9", "cites", "src:s2", "src:s1"),                   # s2 merely cites the paper
            edge("e:10", "derives-from", "src:summary", "src:p"),
            edge("e:11", "supports", "src:summary", "clm:c2"),
            edge("e:12", "supports", "src:summary2", "clm:c2"),
            edge("e:13", "derives-from", "src:summary2", "src:s1-copy"),  # both derive from the p group
        ]
        return {"nodes": nodes, "edges": edges}

    def test_rules_one_to_three(self):
        code, out, _ = run(self.fixture())
        self.assertEqual(code, 0, out)
        self.assertIn("src:p + src:s1: collapsed: rule 1: linked by same-as", out)
        self.assertIn("src:p + src:s1-copy: collapsed: rule 1: linked by same-as", out)
        self.assertIn("src:s1 + src:s2: collapsed: rule 3: src:s2 cites src:s1", out)
        self.assertIn("src:p + src:summary: collapsed: rule 2: src:summary derives-from src:p", out)
        self.assertIn("src:summary + src:summary2: collapsed: rule 2: both derive from", out)
        # withdrawn support edge is not counted
        self.assertNotIn("e:6", out.split("clm:c1")[1].split("=>")[0])
        # s2 (news) and p (preprint) are independent: different tiers, no link between them
        self.assertIn("clm:c1", out)
        self.assertIn("=> QUALIFIES via", out)
        self.assertIn("qualify as axiom-candidate: 1: clm:c1", out)
        self.assertIn("have supports from two or more tiers but still fail: 1: clm:c2", out)

    def test_same_tier_never_qualifies(self):
        data = {"nodes": [node("src:a", "source", "news-outlet", provenance="p1"),
                          node("src:b", "source", "news-outlet", provenance="p2"),
                          node("clm:c", "claim", "news-outlet")],
                "edges": [edge("e:1", "supports", "src:a", "clm:c"), edge("e:2", "supports", "src:b", "clm:c")]}
        _, out, _ = run(data)
        self.assertIn("all supports share tier news-outlet -> does not qualify", out)

    def test_rule_four_literal_versus_off(self):
        data = {"nodes": [node("src:a", "source", "news-outlet", provenance="same agent"),
                          node("src:b", "source", "institutional-report", provenance="same agent"),
                          node("clm:c", "claim", "institutional-report")],
                "edges": [edge("e:1", "supports", "src:a", "clm:c"), edge("e:2", "supports", "src:b", "clm:c")]}
        _, out, _ = run(data)
        self.assertIn("collapsed: rule 4: same provenance string", out)
        self.assertIn("would qualify with --provenance-rule off", out)
        self.assertIn("qualify as axiom-candidate: 0", out)
        _, out, _ = run(data, "--provenance-rule", "off")
        self.assertIn("qualify as axiom-candidate: 1: clm:c", out)

    def test_cites_into_claim_is_not_a_support(self):
        data = {"nodes": [node("src:a", "source", "news-outlet", provenance="p1"),
                          node("src:b", "source", "institutional-report", provenance="p2"),
                          node("clm:c", "claim", "news-outlet")],
                "edges": [edge("e:1", "supports", "src:a", "clm:c"), edge("e:2", "cites", "src:b", "clm:c")]}
        _, out, _ = run(data)
        self.assertIn("cited by (cites edges, not counted as supports): src:b [e:2]", out)
        self.assertIn("one support -> does not qualify", out)

    def test_write_sets_type_and_disputed_and_reverts(self):
        data = {"nodes": [node("src:a", "source", "news-outlet", provenance="p1"),
                          node("src:b", "source", "institutional-report", provenance="p2"),
                          node("src:x", "source", "preprint", provenance="p3"),
                          node("clm:c", "claim", "institutional-report"),
                          node("clm:stale", "axiom-candidate", "preprint")],
                "edges": [edge("e:1", "supports", "src:a", "clm:c"), edge("e:2", "supports", "src:b", "clm:c"),
                          edge("e:3", "contradicts", "src:x", "clm:c"),
                          edge("e:4", "supports", "src:x", "clm:stale")]}
        code, out, written = run(data, "--write")
        self.assertEqual(code, 0, out)
        self.assertIn("is typed `axiom-candidate` in the file but does not meet the rule", out)
        self.assertIn("contradicted by (active): src:x [e:3] -> status should be disputed", out)
        self.assertIn("wrote clm:c: type claim -> axiom-candidate, status active -> disputed", out)
        self.assertIn("wrote clm:stale: type axiom-candidate -> claim", out)
        self.assertIn("2 node(s) changed.", out)
        self.assertIn("type: axiom-candidate", written)
        self.assertIn("status: disputed", written)

    def test_write_refuses_on_validation_errors(self):
        data = {"nodes": [node("clm:c", "claim", "preprint")],
                "edges": [edge("e:1", "supports", "src:missing", "clm:c")]}
        code, out, _ = run(data, "--write")
        self.assertEqual(code, 1)
        self.assertIn("--write skipped: fix validation errors first.", out)


if __name__ == "__main__":
    unittest.main(verbosity=1)
