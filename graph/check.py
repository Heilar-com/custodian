#!/usr/bin/env python3
"""Check graph/graph.yaml against docs/graph-schema.md and compute axiom-candidate status.

Usage:
    python3 graph/check.py                      # validate and print the axiom report
    python3 graph/check.py --write              # also set type/status on qualifying nodes in the YAML
    python3 graph/check.py --strict             # treat warnings as errors

Needs Python 3.9 or later and PyYAML. No other dependencies.

Exit code is 1 when validation finds errors (or warnings with --strict), 0 otherwise.
The axiom report is a set of claims that can be challenged, not a verdict.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "PyYAML is missing. Install it with:  python3 -m pip install pyyaml\n"
        "On macOS the system interpreter ships with it:  /usr/bin/python3 graph/check.py\n"
    )
    sys.exit(2)

# ---------------------------------------------------------------------------
# Schema constants (docs/graph-schema.md)
# ---------------------------------------------------------------------------

NODE_TYPES = {
    "claim", "source", "primitive", "design-item", "decision", "conflict", "axiom-candidate",
}
EDGE_TYPES = {"supports", "contradicts", "derives-from", "same-as", "cites"}
STATUS_VALUES = {"active", "disputed", "superseded", "withdrawn"}
TIERS = {
    "peer-reviewed-journal", "preprint", "institutional-report", "news-outlet", "creator-content", "n/a",
}
VERIFICATION_STATUS = {"confirmed", "self-description", "not-verified"}
NODE_REQUIRED = (
    "id", "type", "label", "created", "provenance", "status",
    "verification_tier", "verification_status", "retention",
)
NODE_OPTIONAL = ("links",)
EDGE_REQUIRED = ("id", "type", "from", "to", "created", "provenance", "status")
TOP_LEVEL_KNOWN = {"nodes", "edges", "provenance_default"}

# Nodes whose axiom-candidate status is computed. The schema says "a node qualifies";
# this script evaluates claims (and existing axiom-candidates, for recomputation) and only
# reports, without evaluating for status, other node types that meet the rule. See README.
ELIGIBLE_TYPES = {"claim", "axiom-candidate"}

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


def is_iso_date(value) -> bool:
    if isinstance(value, dt.date):
        return True
    if isinstance(value, str) and ISO_DATE.match(value):
        try:
            dt.date.fromisoformat(value)
            return True
        except ValueError:
            return False
    return False


def norm_provenance(value) -> str:
    return re.sub(r"\s+", " ", str(value)).strip()


class UnionFind:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(data, rep: Report):
    """Return (nodes_by_id, edges) after checking the file against the schema."""
    if not isinstance(data, dict):
        rep.error("file", "top level must be a mapping with `nodes` and `edges`")
        return {}, []

    for key in data:
        if key not in TOP_LEVEL_KNOWN:
            rep.warn("file", f"unknown top-level key `{key}`")

    raw_nodes = data.get("nodes")
    raw_edges = data.get("edges")
    if not isinstance(raw_nodes, list):
        rep.error("file", "`nodes` must be a list")
        raw_nodes = []
    if not isinstance(raw_edges, list):
        rep.error("file", "`edges` must be a list")
        raw_edges = []

    nodes: dict[str, dict] = {}
    seen_ids: dict[str, str] = {}

    # --- nodes -------------------------------------------------------------
    for i, node in enumerate(raw_nodes):
        where = f"node #{i + 1}"
        if not isinstance(node, dict):
            rep.error(where, "must be a mapping")
            continue
        nid = node.get("id")
        if not isinstance(nid, str) or not nid.strip():
            rep.error(where, "missing or non-string `id`")
            continue
        where = f"node {nid}"
        if nid in seen_ids:
            rep.error(where, f"duplicate id (already used by {seen_ids[nid]})")
            continue
        seen_ids[nid] = where
        nodes[nid] = node

        for key in NODE_REQUIRED:
            if key not in node:
                rep.error(where, f"missing required property `{key}`")
        for key in node:
            if key not in NODE_REQUIRED and key not in NODE_OPTIONAL:
                rep.warn(where, f"property `{key}` is not in the schema")

        ntype = node.get("type")
        if "type" in node and ntype not in NODE_TYPES:
            rep.error(where, f"type `{ntype}` is not a schema node type")

        label = node.get("label")
        if "label" in node and (not isinstance(label, str) or not label.strip()):
            rep.error(where, "`label` must be a non-empty string")

        if "created" in node and not is_iso_date(node["created"]):
            rep.error(where, f"`created` must be an ISO 8601 date, got {node['created']!r}")

        prov = node.get("provenance")
        if "provenance" in node and (not isinstance(prov, str) or not prov.strip()):
            rep.error(where, "`provenance` must be a non-empty string")

        status = node.get("status")
        if "status" in node and status not in STATUS_VALUES:
            rep.error(where, f"status `{status}` not in {sorted(STATUS_VALUES)}")

        tier = node.get("verification_tier")
        if "verification_tier" in node and tier not in TIERS:
            rep.error(where, f"verification_tier `{tier}` not in {sorted(TIERS)}")
        if ntype == "source" and tier == "n/a":
            rep.error(where, "verification_tier `n/a` is not allowed on a source")

        vstatus = node.get("verification_status")
        if "verification_status" in node and vstatus not in VERIFICATION_STATUS:
            rep.error(where, f"verification_status `{vstatus}` not in {sorted(VERIFICATION_STATUS)}")

        retention = node.get("retention")
        if "retention" in node and not (retention == "permanent" or is_iso_date(retention)):
            rep.error(where, f"`retention` must be `permanent` or an ISO date, got {retention!r}")

        links = node.get("links")
        if ntype == "source" and "links" not in node:
            rep.error(where, "source node has no `links`")
        if "links" in node:
            if not isinstance(links, list) or not links:
                rep.error(where, "`links` must be a non-empty list of URLs or DOIs")
            else:
                for link in links:
                    if not isinstance(link, str) or not link.strip():
                        rep.error(where, f"link {link!r} is not a string")
                    elif not re.match(r"^(https?://|doi:|10\.\d{4,})", link.strip()):
                        rep.warn(where, f"link {link!r} does not look like a URL or DOI")

    # --- edges -------------------------------------------------------------
    edges: list[dict] = []
    edge_pairs: dict[tuple, str] = {}
    for i, edge in enumerate(raw_edges):
        where = f"edge #{i + 1}"
        if not isinstance(edge, dict):
            rep.error(where, "must be a mapping")
            continue
        eid = edge.get("id")
        if not isinstance(eid, str) or not eid.strip():
            rep.error(where, "missing or non-string `id`")
            continue
        where = f"edge {eid}"
        if eid in seen_ids:
            rep.error(where, f"duplicate id (already used by {seen_ids[eid]})")
            continue
        seen_ids[eid] = where

        ok = True
        for key in EDGE_REQUIRED:
            if key not in edge:
                rep.error(where, f"missing required property `{key}`")
                ok = False
        for key in edge:
            if key not in EDGE_REQUIRED:
                rep.warn(where, f"property `{key}` is not in the schema")

        etype = edge.get("type")
        if "type" in edge and etype not in EDGE_TYPES:
            rep.error(where, f"type `{etype}` is not a schema edge type")
            ok = False
        if "created" in edge and not is_iso_date(edge["created"]):
            rep.error(where, f"`created` must be an ISO 8601 date, got {edge['created']!r}")
        prov = edge.get("provenance")
        if "provenance" in edge and (not isinstance(prov, str) or not prov.strip()):
            rep.error(where, "`provenance` must be a non-empty string")
        if "status" in edge and edge.get("status") not in STATUS_VALUES:
            rep.error(where, f"status `{edge.get('status')}` not in {sorted(STATUS_VALUES)}")

        src, dst = edge.get("from"), edge.get("to")
        for end, val in (("from", src), ("to", dst)):
            if end in edge and val not in nodes:
                rep.error(where, f"`{end}` points at unknown node `{val}`")
                ok = False
        if src is not None and src == dst:
            rep.error(where, f"self-loop on `{src}`")
            ok = False

        if ok:
            key = (etype, src, dst)
            if key in edge_pairs:
                rep.warn(where, f"duplicates {edge_pairs[key]} ({etype} {src} -> {dst})")
            else:
                edge_pairs[key] = eid
            if etype == "same-as" and nodes[src].get("type") != nodes[dst].get("type"):
                rep.warn(where, f"same-as joins a {nodes[src].get('type')} to a {nodes[dst].get('type')}")
            edges.append(edge)

    # --- cross checks ------------------------------------------------------
    active_supports_in: dict[str, list[dict]] = defaultdict(list)
    touches: dict[str, set] = defaultdict(set)
    contradicted: set = set()
    for e in edges:
        touches[e["from"]].add(e["to"])
        touches[e["to"]].add(e["from"])
        if e["status"] == "active" and e["type"] == "supports":
            active_supports_in[e["to"]].append(e)
        if e["status"] == "active" and e["type"] == "contradicts":
            contradicted.add(e["to"])

    for nid, node in nodes.items():
        where = f"node {nid}"
        ntype = node.get("type")
        tier = node.get("verification_tier")
        if ntype in ELIGIBLE_TYPES:
            sup_tiers = {
                nodes[e["from"]].get("verification_tier") for e in active_supports_in.get(nid, [])
            } - {None}
            real_tiers = sup_tiers - {"n/a"}
            if tier == "n/a" and real_tiers:
                rep.error(where, f"verification_tier is `n/a` but it has active supports from tiers "
                                 f"{sorted(real_tiers)}; a claim inherits its sources' tier")
            elif real_tiers and tier not in real_tiers:
                rep.warn(where, f"verification_tier `{tier}` is not among its supporters' tiers {sorted(real_tiers)}")
            if tier == "n/a" and node.get("verification_status") == "confirmed":
                rep.warn(where, "tier `n/a` with verification_status `confirmed`: confirmed by what?")
        if ntype == "decision":
            linked_to_tension = nid in contradicted or any(
                nodes[o].get("type") == "conflict" for o in touches.get(nid, ())
            )
            if not linked_to_tension:
                rep.warn(where, "decision has no incoming contradicts edge and no link to a conflict node")
        if node.get("status") == "disputed" and nid not in contradicted:
            rep.warn(where, "status `disputed` but no active contradicts edge points at it")

    for nid in sorted(contradicted):
        if nodes[nid].get("status") == "active":
            rep.warn(f"node {nid}", "is the target of an active contradicts edge but its status is `active`, "
                                    "not `disputed` (schema: axiom rule, operational checks)")

    return nodes, edges


# ---------------------------------------------------------------------------
# Axiom rule
# ---------------------------------------------------------------------------

class AxiomResult:
    def __init__(self, nid: str) -> None:
        self.nid = nid
        self.supports: list[dict] = []          # active supports edges into nid
        self.cited_by: list[dict] = []          # active cites edges into nid (not counted)
        self.contradicted_by: list[dict] = []   # active contradicts edges into nid
        self.pairs: list[tuple] = []            # (a, b, verdict) for every supporter pair
        self.qualifies = False
        self.witness: tuple | None = None       # (a, b) that qualified


def build_indexes(nodes: dict, edges: list):
    """Index the active structural edges used by the independence rules."""
    same_as = UnionFind()
    derives: dict[str, set] = defaultdict(set)   # node -> direct derives-from targets
    cites: set = set()                            # (from, to) active cites edges
    for e in edges:
        if e["status"] != "active":
            continue
        if e["type"] == "same-as":
            same_as.union(e["from"], e["to"])
        elif e["type"] == "derives-from":
            derives[e["from"]].add(e["to"])
        elif e["type"] == "cites":
            cites.add((e["from"], e["to"]))
    return same_as, derives, cites


def ancestors(nid: str, derives: dict, same_as: UnionFind) -> dict:
    """Everything nid derives from, transitively, keyed by same-as root -> the node actually reached."""
    out: dict = {}
    stack = [nid]
    while stack:
        cur = stack.pop()
        for parent in derives.get(cur, ()):
            root = same_as.find(parent)
            if root not in out:
                out[root] = parent
                stack.append(parent)
    return out


def via(actual: str, root_member: str) -> str:
    return actual if actual == root_member else f"{actual} (same-as {root_member})"


def collapse_reason(a: str, b: str, nodes: dict, same_as: UnionFind, derives: dict,
                    cites: set) -> str | None:
    """Return None if a and b are independent, else which rule collapses them."""
    ra, rb = same_as.find(a), same_as.find(b)
    if ra == rb:
        return "rule 1: linked by same-as"
    anc_a, anc_b = ancestors(a, derives, same_as), ancestors(b, derives, same_as)
    if rb in anc_a:
        return f"rule 2: {a} derives-from {via(anc_a[rb], b)}"
    if ra in anc_b:
        return f"rule 2: {b} derives-from {via(anc_b[ra], a)}"
    shared = sorted(set(anc_a) & set(anc_b))
    if shared:
        return f"rule 2: both derive from {via(anc_a[shared[0]], anc_b[shared[0]])}"
    if (a, b) in cites:
        return f"rule 3: {a} cites {b}"
    if (b, a) in cites:
        return f"rule 3: {b} cites {a}"
    pa, pb = norm_provenance(nodes[a].get("provenance", "")), norm_provenance(nodes[b].get("provenance", ""))
    if pa == pb:
        return f"rule 4: same provenance ({pa})"
    return None


def compute_axiom(nodes: dict, edges: list) -> dict:
    """Evaluate the axiom rule for every node with incoming active supports edges."""
    same_as, derives, cites = build_indexes(nodes, edges)
    results: dict[str, AxiomResult] = {}

    def result(nid: str) -> AxiomResult:
        if nid not in results:
            results[nid] = AxiomResult(nid)
        return results[nid]

    for e in edges:
        if e["status"] != "active":
            continue
        if e["type"] == "supports":
            result(e["to"]).supports.append(e)
        elif e["type"] == "cites":
            result(e["to"]).cited_by.append(e)
        elif e["type"] == "contradicts":
            result(e["to"]).contradicted_by.append(e)

    for nid, r in results.items():
        supporters = sorted({e["from"] for e in r.supports})
        for i, a in enumerate(supporters):
            for b in supporters[i + 1:]:
                ta, tb = nodes[a].get("verification_tier"), nodes[b].get("verification_tier")
                if ta == "n/a" or tb == "n/a":
                    verdict = "a supporter has tier n/a (not a tier for this rule)"
                elif ta == tb:
                    verdict = f"same tier ({ta})"
                else:
                    reason = collapse_reason(a, b, nodes, same_as, derives, cites)
                    if reason is None:
                        verdict = f"INDEPENDENT, tiers {ta} + {tb}"
                        if not r.qualifies:
                            r.qualifies, r.witness = True, (a, b)
                    else:
                        verdict = f"collapsed: {reason}"
                r.pairs.append((a, b, verdict))
    return results


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def short(nodes: dict, nid: str) -> str:
    return f"{nid} ({nodes[nid].get('verification_tier')})"


def print_axiom_report(nodes: dict, results: dict) -> None:
    print("=" * 78)
    print("AXIOM-CANDIDATE REPORT")
    print("Flags here are claims that can be challenged, not verdicts.")
    print("=" * 78)

    eligible = [nid for nid, n in nodes.items() if n.get("type") in ELIGIBLE_TYPES]
    qualifying, near = [], []
    for nid in eligible:
        n = nodes[nid]
        r = results.get(nid, AxiomResult(nid))
        tiers = sorted({nodes[e["from"]].get("verification_tier") for e in r.supports})
        print()
        print(f"{nid}  [{n.get('type')}, tier {n.get('verification_tier')}, status {n.get('status')}]")
        print(f"  {str(n.get('label', ''))[:110]}")
        if not r.supports:
            print("  active supports: none -> does not qualify")
        else:
            print(f"  active supports ({len(r.supports)}):")
            for e in r.supports:
                print(f"    {e['id']}  {short(nodes, e['from'])}")
            if len(r.supports) == 1:
                print("  one support -> does not qualify (needs two independent, different tiers)")
            elif len(tiers) == 1:
                print(f"  all supports share tier {tiers[0]} -> does not qualify")
            else:
                print("  pairs:")
                for a, b, verdict in r.pairs:
                    print(f"    {a} + {b}: {verdict}")
        if r.cited_by:
            print("  cited by (cites edges, not counted as supports): "
                  + ", ".join(f"{e['from']} [{e['id']}]" for e in r.cited_by))
        if r.contradicted_by:
            print("  contradicted by (active): "
                  + ", ".join(f"{e['from']} [{e['id']}]" for e in r.contradicted_by)
                  + " -> status should be disputed")
        verdict = "QUALIFIES" if r.qualifies else "does not qualify"
        line = f"  => {verdict}"
        if r.qualifies:
            line += f" via {short(nodes, r.witness[0])} + {short(nodes, r.witness[1])}"
            qualifying.append(nid)
        elif len(tiers) >= 2:
            near.append(nid)
        print(line)

    # Nodes outside ELIGIBLE_TYPES that have active supports, for information only.
    others = []
    for nid, r in results.items():
        if nodes[nid].get("type") in ELIGIBLE_TYPES or not r.supports:
            continue
        tiers = sorted({nodes[e["from"]].get("verification_tier") for e in r.supports})
        others.append((nid, r, tiers))

    print()
    print("-" * 78)
    print("SUMMARY")
    print(f"  claims evaluated: {len(eligible)}")
    print(f"  qualify as axiom-candidate: {len(qualifying)}"
          + (": " + ", ".join(qualifying) if qualifying else ""))
    if near:
        print(f"  have supports from two or more tiers but still fail: {len(near)}: " + ", ".join(near))
    disputed = [nid for nid in eligible if results.get(nid) and results[nid].contradicted_by]
    print(f"  claims with an active contradicts edge (disputed): {len(disputed)}"
          + (": " + ", ".join(disputed) if disputed else ""))
    if others:
        print()
        print("  Nodes that are not claims but have active supports (not evaluated for status;")
        print("  the schema says 'a node qualifies', this script evaluates claims only, see README):")
        for nid, r, tiers in sorted(others):
            flag = ""
            if r.qualifies:
                flag = f"  <- meets the rule via {r.witness[0]} + {r.witness[1]}"
            print(f"    {nid} [{nodes[nid].get('type')}]: {len(r.supports)} supports, tiers {tiers}{flag}")


# ---------------------------------------------------------------------------
# --write: targeted line edits that keep comments and anchors intact
# ---------------------------------------------------------------------------

def write_back(path: Path, nodes: dict, results: dict, rep: Report) -> int:
    """Set type and status on qualifying nodes in place. Returns the number of nodes changed.

    Works on the YAML text line by line: a node block runs from its list-item line to the next
    item at the same indent or the next top-level key, whatever the indentation or key order.
    Only the block's own `type:` and `status:` lines are rewritten, so comments and anchors survive.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    def top_level(line: str) -> bool:
        return bool(line.strip()) and not line[0].isspace() and not line.startswith(("#", "- "))

    # The node list's own item indent: the first `- ` line after `nodes:`. Deeper `- ` lines
    # (for example under `links:`) belong to the node and are not boundaries.
    item_indent = None
    in_nodes = False
    for line in lines:
        if re.match(r"^nodes:\s*$", line):
            in_nodes = True
        elif in_nodes and top_level(line):
            break
        elif in_nodes:
            m = re.match(r"^(\s*)- \S", line)
            if m:
                item_indent = len(m.group(1))
                break
    if item_indent is None:
        rep.warn("file", "could not find the `nodes:` list for --write")
        return 0

    item_line = re.compile(r"^ {%d}- \S" % item_indent)
    boundaries = [i for i, line in enumerate(lines) if item_line.match(line) or top_level(line)]
    id_line = re.compile(r"^\s*(?:- )?id:\s*(\S+)\s*$")
    bounds: dict[str, tuple] = {}
    for n, i in enumerate(boundaries):
        if not item_line.match(lines[i]):
            continue
        end = boundaries[n + 1] if n + 1 < len(boundaries) else len(lines)
        for j in range(i, end):
            m = id_line.match(lines[j])
            if m and m.group(1) in nodes:
                bounds[m.group(1)] = (i, end)
                break

    changed = 0
    for nid, node in nodes.items():
        if node.get("type") not in ELIGIBLE_TYPES:
            continue
        r = results.get(nid)
        qualifies = bool(r and r.qualifies)
        new_type = "axiom-candidate" if qualifies else "claim"
        new_status = node.get("status")
        if qualifies:
            new_status = "disputed" if r.contradicted_by else "active"
        if new_type == node.get("type") and new_status == node.get("status"):
            continue
        if nid not in bounds:
            rep.warn(f"node {nid}", "could not locate its block in the file for --write")
            continue
        start, end = bounds[nid]
        for i in range(start, end):
            m = re.match(r"^(\s*(?:- )?)(type|status):\s*\S+\s*$", lines[i])
            if not m:
                continue
            prefix, key = m.groups()
            if key == "type" and new_type != node.get("type"):
                lines[i] = f"{prefix}type: {new_type}\n"
            elif key == "status" and new_status != node.get("status"):
                lines[i] = f"{prefix}status: {new_status}\n"
        changed += 1
        parts = []
        if new_type != node.get("type"):
            parts.append(f"type {node.get('type')} -> {new_type}")
        if new_status != node.get("status"):
            parts.append(f"status {node.get('status')} -> {new_status}")
        print(f"  wrote {nid}: " + ", ".join(parts))

    if changed:
        path.write_text("".join(lines), encoding="utf-8")
    return changed


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", nargs="?", default=str(Path(__file__).with_name("graph.yaml")),
                        help="path to graph.yaml (default: graph/graph.yaml next to this script)")
    parser.add_argument("--write", action="store_true",
                        help="set type: axiom-candidate and status on qualifying nodes in the YAML "
                             "(targeted line edits; comments and anchors are kept)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--no-report", action="store_true", help="validate only")
    args = parser.parse_args(argv)

    path = Path(args.file)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"error: {path} not found", file=sys.stderr)
        return 1
    except yaml.YAMLError as exc:
        print(f"error: {path} is not valid YAML: {exc}", file=sys.stderr)
        return 1

    rep = Report()
    nodes, edges = validate(data, rep)
    results = compute_axiom(nodes, edges)
    for nid, node in nodes.items():
        if node.get("type") == "axiom-candidate" and not (nid in results and results[nid].qualifies):
            rep.warn(f"node {nid}", "is typed `axiom-candidate` in the file but does not meet the rule; "
                                    "the status is stale or was set by hand")

    print("=" * 78)
    print(f"VALIDATION of {path}")
    print("=" * 78)
    print(f"  nodes: {len(nodes)}   edges: {len(edges)}")
    by_type: dict[str, int] = defaultdict(int)
    for n in nodes.values():
        by_type[str(n.get("type"))] += 1
    print("  node types: " + ", ".join(f"{k} {v}" for k, v in sorted(by_type.items())))
    by_etype: dict[str, int] = defaultdict(int)
    for e in edges:
        by_etype[str(e.get("type"))] += 1
    print("  edge types: " + ", ".join(f"{k} {v}" for k, v in sorted(by_etype.items())))
    print(f"  errors: {len(rep.errors)}   warnings: {len(rep.warnings)}")
    for msg in rep.errors:
        print(f"  ERROR    {msg}")
    for msg in rep.warnings:
        print(f"  warning  {msg}")

    failed = bool(rep.errors) or (args.strict and bool(rep.warnings))
    if rep.errors:
        print("\nValidation failed; the axiom report below is computed on the nodes and edges that parsed.")

    if not args.no_report:
        print()
        print_axiom_report(nodes, results)
        if args.write:
            print()
            if rep.errors:
                print("--write skipped: fix validation errors first.")
                return 1
            print(f"--write: updating {path}")
            changed = write_back(path, nodes, results, rep)
            print(f"  {changed} node(s) changed." if changed else "  nothing to change.")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
