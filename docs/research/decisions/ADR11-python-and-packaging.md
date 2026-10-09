# ADR11: Python 3.12, managed by uv, one root project with code in `core/`

Status: accepted · 9 October 2026 · Decided by: Mohamed Hamdoun (Python version); layout
proposed by Claude, open to change · Plan step 0.4

## Decision

- **Python 3.12 only** (`requires-python = "==3.12.*"`, `.python-version` = `3.12`).
  Local interpreter: 3.12.10.
- **uv** manages the interpreter, dependencies and the lockfile (`uv.lock`). Local uv
  version: 0.7.13.
- **One `pyproject.toml` at the repository root.** It builds the package `roadtrust` from
  `core/roadtrust/` (hatchling backend). Tests live in `core/tests/`.

## Why

- 3.12 is the version the hackathon model was trained on (E01) and has the widest wheel
  support among scientific and simulator bindings likely in P4–P6. E01 showed 3.13 gives
  identical results for the old system, so 3.12 costs nothing in reproducibility.
- The E01 finding was that the old lockfile pinned packages but not Python. Pinning the
  minor version closes that gap.
- uv was already used by the hackathon project, is fast, and writes one cross-platform
  lockfile.
- One root `pyproject.toml` is the smallest setup that still keeps Python code inside
  `core/` as ADR09 requires; repository tools (`tools/`) run from the same environment.

## Pros

- Same interpreter minor version for every developer and CI.
- `uv sync --locked` reproduces the exact environment.
- One file to read for all Python settings.

## Cons

- 3.12 is not the newest; maintained until about October 2028. Moving to 3.13/3.14 later
  is a deliberate change with its own record.
- Patch version (3.12.x) is not pinned; patch releases are expected to be compatible.
- If `sim/` or `chain/` later need their own Python tools with conflicting dependencies,
  the single root project must become a uv workspace.
- Local uv 0.7.13 is from June 2025; CI pins the same version so the lockfile format
  matches. Upgrading uv is a separate change.

## Alternatives considered

| Alternative | Why not chosen | When it would be better |
|---|---|---|
| Python 3.13 | Owner chose 3.12 for broader binding support | Once every dependency the plan needs ships 3.13 wheels |
| Python 3.14 | Newest; some scientific/simulator packages may lag | For a project with only pure-Python dependencies |
| `pyproject.toml` inside `core/` | Root tools would need a second environment | If the repository grows several independent Python projects |
| uv workspace (root + `core/` member) | Extra configuration with only one Python package today | As soon as a second Python package appears |
| pip + venv + requirements.txt | No single cross-platform lockfile; slower | If uv becomes unavailable |
| Poetry / PDM | Equivalent features; uv already in use | If the team already standardizes on one of them |

## How to retest

```bash
uv sync --locked
uv run python --version      # Python 3.12.x
uv run pytest                # 1 passed (package imports from core/)
```

## How to change or revert

Change `requires-python` and `.python-version`, run `uv lock`, rerun the tests, and record
the change. To move code out of `core/`, edit `[tool.hatch.build.targets.wheel]` and
`[tool.pytest.ini_options]`.

## Revisit trigger

A required dependency lacks 3.12 wheels, 3.12 nears end of life, or a second Python
package is added.
