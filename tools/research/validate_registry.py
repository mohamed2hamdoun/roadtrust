"""Check research-record integrity. Does not validate application readiness."""

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "research"
REG = DOCS / "registries"


def load(name: str) -> tuple[list[dict[str, Any]], set[str]]:
    value = json.loads((REG / (name + ".json")).read_text())
    assert isinstance(value, list), name
    ids = [r["id"] for r in value]
    assert len(ids) == len(set(ids)), f"duplicate IDs in {name}"
    return value, set(ids)


records: dict[str, list[dict[str, Any]]] = {}
ids: dict[str, set[str]] = {}
for kind in [
    "sources",
    "datasets",
    "features",
    "experiments",
    "requirements",
    "decisions",
    "failure_cases",
]:
    records[kind], ids[kind] = load(kind)

relations = {
    "source_ids": "sources",
    "dataset_ids": "datasets",
    "experiment_ids": "experiments",
    "requirement_ids": "requirements",
    "accepted_feature_ids": "features",
}
for kind, rows in records.items():
    for row in rows:
        for field, target in relations.items():
            for ident in row.get(field, []):
                assert ident in ids[target], f"{kind}/{row['id']}: unknown {field} {ident}"
        if kind == "features":
            assert row.get("deployment_caveat") and row.get("current_definition")
            assert set(row["availability"]).issubset(ids["datasets"])
        if kind == "experiments" and row["status"] == "planned":
            assert row["result"] is None and not row["runs"] and not row["limitations_observed"], (
                f"Unrun experiment {row['id']} contains results"
            )

names = [f["name"] for f in records["features"]]
assert len(names) == 17 and len(set(names)) == 17, "Baseline feature inventory incomplete"
for p in DOCS.rglob("*.md"):
    for dest in re.findall(r"\]\(([^)]+)\)", p.read_text()):
        if "://" not in dest and not dest.startswith("#"):
            assert (p.parent / dest.split("#")[0]).exists(), f"Broken link: {p.name}: {dest}"
    for source_id in re.findall(r"\bS\d{2}\b", p.read_text()):
        assert source_id in ids["sources"], f"Unknown source {source_id} in {p.name}"

print(
    json.dumps(
        {
            "status": "PASS",
            "records": {k: len(v) for k, v in records.items()},
            "scope": "IDs, cross-references, local links, baseline feature inventory "
            "and planned-result honesty",
        },
        indent=2,
    )
)
