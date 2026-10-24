# graph/

Seed data for the Custodian graph and the script that checks it.

| File | What it is |
|---|---|
| [graph.yaml](graph.yaml) | The graph: nodes and edges following [docs/graph-schema.md](../docs/graph-schema.md). |
| [check.py](check.py) | Validates `graph.yaml` against the schema and computes axiom-candidate status. |
| [test_check.py](test_check.py) | Tests for `check.py` on small synthetic graphs. |

## Running the check

Needs Python 3.9 or later and PyYAML. Nothing else.

```bash
python3 -m pip install pyyaml
```

On macOS the system interpreter at `/usr/bin/python3` already ships PyYAML, so `/usr/bin/python3 graph/check.py` works with no install. If `pip` refuses because the Python is externally managed (Homebrew), use the system interpreter or a virtualenv.

```bash
python3 graph/check.py
```

This prints two sections and exits non-zero if validation finds errors:

1. **Validation.** Every node has the nine required properties with allowed values, every `source` has `links`, no duplicate ids, every edge has `id`, `type`, `from`, `to`, `created`, `provenance`, `status`, edge types are from the schema, no dangling references, no self-loops, `retention` is `permanent` or an ISO date, `verification_status` is one of the three markers. Errors fail the run. Warnings (duplicate edges, status inconsistencies, properties not in the schema) do not, unless you pass `--strict`.
2. **Axiom report.** For every `claim`: its active `supports` edges, every pair of supporters and whether the pair is independent or which rule collapsed it, which pair qualified it if any, and which active `contradicts` edges point at it. Then a summary.

Flags:

| Flag | Effect |
|---|---|
| `--provenance-rule literal` (default) | Independence rule 4 compares each supporter's `provenance` property as written. Two nodes recorded by the same agent string are not independent. |
| `--provenance-rule off` | Skips rule 4. The schema's rule 4 is about the source's author group or publishing organisation, which the schema has no property for yet. See "Readings" below. |
| `--write` | Sets `type: axiom-candidate` on qualifying claims and `status: disputed` on those with an active `contradicts` edge; reverts stale `axiom-candidate` nodes to `claim`. Edits only those lines; comments and anchors stay. Refused while validation has errors. Off by default: the report is the product, the file is Markús's. |
| `--strict` | Warnings count as errors for the exit code. |
| `--no-report` | Validation only. |

Run the tests with:

```bash
python3 graph/test_check.py
```

## What the script computes

The axiom rule, from the schema: a claim qualifies when it has two or more active incoming `supports` edges from nodes that are independent of each other and have different `verification_tier` values. `n/a` is not a tier for this rule.

Independence is checked per pair of supporters:

1. Not linked by `same-as`, directly or through a chain (union of all active `same-as` edges).
2. Neither `derives-from` the other, and they do not both derive from the same node. `derives-from` is followed transitively, and `same-as` groups count as one node along the way.
3. Neither `cites` the other (a direct active `cites` edge in either direction).
4. Their `provenance` differs (literal reading, see above), unless `--provenance-rule off`.

Only `supports` edges with `status: active` count. The node's own `status` does not affect the count. An active `contradicts` edge never removes the status; the report shows it next to the claim and the claim's status should be `disputed`.

The report is a set of claims that can be challenged, not a verdict ([agents.md](../agents.md), rule c).

## Readings the script had to pick

The schema leaves some things open. The script picks one reading for each and says so here, so the choice can be turned into a `decision` node or overturned. None of these is a decision; Markús decides.

- **Rule 4, "different provenance".** The node property `provenance` records who created the node (mostly the agent that seeded it), but the rule's text is about the source's authors or publisher. The schema has no property for that. Default: compare the property literally. Alternative: `--provenance-rule off`. The report prints both outcomes for every claim.
- **Same organisation publishing twice.** Under a publisher-level reading, are two Alþingi documents (a committee report and a bill) one provenance or two? The same question applies to two ECHR documents. Not implemented either way until a property exists to hold it.
- **`cites` edges into a claim** are listed as "cited by" and never counted as support, in either direction.
- **Rule 3 direction and depth.** A `cites` edge between two supporters collapses them whichever way it points. Only direct edges are followed, not chains.
- **Rule 2 depth.** `derives-from` is followed transitively. The schema says "directly or through a chain" only for `same-as`; the script applies the same to derivation because a summary of a summary still rests on the original.
- **Edge `status` values** are taken to be the same four as node status; the schema lists them only for nodes.
- **Eligible nodes.** The schema says "a node qualifies", and in the file primitives, design items and conflicts also receive `supports` edges. The script evaluates only `claim` (and existing `axiom-candidate`) nodes for status, and lists the other node types that meet the rule for information.
- **Supporter status.** A `supports` edge from a `withdrawn` or `superseded` node still counts if the edge itself is `active`. The schema speaks only of edge status.
- **`disputed` scope.** The schema states the `disputed` rule inside the axiom section. The script reports every node that is the target of an active `contradicts` edge but is not `disputed`, and every `disputed` node with no such edge, as warnings on all node types; `--write` only changes nodes it also marks `axiom-candidate`.
- **Claim tier.** The schema says a claim lists the highest tier among its sources but does not rank tiers. The script only warns when a claim's tier is not among its supporters' tiers.
