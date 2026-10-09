"""Check research-record integrity. Does not validate application readiness."""

import json
import re
import subprocess
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
    "threats",
    "targets",
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

# Threat catalog (ADR18): closed vocabularies so coverage can be counted reliably.
THREAT_VOCAB = {
    "attacker_types": {"OUT", "INS", "RSU", "SENS", "ENV"},
    "profiles": {"rsu", "obu"},
}
for row in records["threats"]:
    for field, allowed in THREAT_VOCAB.items():
        assert set(row[field]) <= allowed, f"threats/{row['id']}: bad {field} {row[field]}"
    assert row["coverage"] in {"dataset", "simulate", "gap"}, f"threats/{row['id']}: coverage"
    assert row["coverage"] != "dataset" or row["dataset_ids"], f"threats/{row['id']}: no dataset"

# Operational targets (ADR19): every target is typed, scoped and marked provisional or final.
for row in records["targets"]:
    assert row["operator"] in {"<=", ">="}, f"targets/{row['id']}: operator"
    assert isinstance(row["value"], int | float), f"targets/{row['id']}: value"
    assert set(row["applies_to"]) <= THREAT_VOCAB["profiles"], f"targets/{row['id']}: profile"
    assert row["status"] in {"provisional", "accepted"}, f"targets/{row['id']}: status"

names = [f["name"] for f in records["features"]]
assert len(names) == 17 and len(set(names)) == 17, "Baseline feature inventory incomplete"
for p in DOCS.rglob("*.md"):
    for dest in re.findall(r"\]\(([^)]+)\)", p.read_text()):
        if "://" not in dest and not dest.startswith("#"):
            assert (p.parent / dest.split("#")[0]).exists(), f"Broken link: {p.name}: {dest}"
    for source_id in re.findall(r"\bS\d{2}\b", p.read_text()):
        assert source_id in ids["sources"], f"Unknown source {source_id} in {p.name}"

# Record system (ADR14): accepted decisions and change records carry every required section,
# the change-record index matches the files, and commits cited in the registry exist in git.
ADR_HEADINGS = (
    "Decision",
    "Why",
    "Pros",
    "Cons",
    "Alternatives considered",
    "How to retest",
    "How to change or revert",
    "Revisit trigger",
)
CR_HEADINGS = (
    "Finding and evidence",
    "What exactly changed",
    "Why this option",
    "Pros",
    "Cons",
    "Alternatives considered",
    "How to retest",
    "How to change or revert",
)


def require_headings(path: Path, headings: tuple[str, ...]) -> None:
    assert path.is_file(), f"Missing record file: {path.relative_to(ROOT)}"
    present = set(re.findall(r"^## (.+?)\s*$", path.read_text(), re.M))
    missing = [h for h in headings if h not in present]
    assert not missing, f"{path.relative_to(ROOT)} lacks sections: {missing}"


registered = set()
for row in records["decisions"]:
    if row.get("record"):
        registered.add(row["record"])
    if row["status"] == "accepted":
        assert row.get("record"), f"{row['id']}: accepted without a record file"
        require_headings(DOCS / row["record"], ADR_HEADINGS)
adr_files = {f"decisions/{p.name}" for p in (DOCS / "decisions").glob("ADR*.md")}
assert adr_files <= registered, f"ADR files not in decisions.json: {sorted(adr_files - registered)}"

cr_files = {p.name[:6]: p for p in (DOCS / "changes").glob("CR-*.md")}
index = (DOCS / "changes" / "README.md").read_text()
indexed = set(re.findall(r"^\| (CR-\d{3}) \|", index, re.M))
assert indexed == set(cr_files), f"Change-record index and files differ: {indexed ^ set(cr_files)}"
for path in cr_files.values():
    require_headings(path, CR_HEADINGS)

cited = [(row["id"], sha) for row in records["decisions"] for sha in row.get("commits", [])]
in_git = (
    subprocess.run(["git", "rev-parse", "--git-dir"], cwd=ROOT, capture_output=True).returncode == 0
)
for record_id, sha in cited if in_git else []:
    found = subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"], cwd=ROOT, capture_output=True
    )
    assert found.returncode == 0, f"{record_id}: cited commit {sha} not in git (shallow clone?)"

print(
    json.dumps(
        {
            "status": "PASS",
            "records": {k: len(v) for k, v in records.items()},
            "record_files": {"decisions": len(adr_files), "changes": len(cr_files)},
            "cited_commits": f"{len(cited)} verified" if in_git else "skipped: not a git checkout",
            "scope": "IDs, cross-references, local links, baseline feature inventory, "
            "planned-result honesty, record sections and cited commits",
        },
        indent=2,
    )
)
