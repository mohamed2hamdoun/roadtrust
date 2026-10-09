# ADR12: Ruff, strict mypy, pre-commit and Hypothesis

Status: accepted · 9 October 2026 · Decided by: Mohamed Hamdoun (tool set); settings
proposed by Claude, open to change · Plan step 0.4

## Decision

| Tool | Version locked | Setting | Job |
|---|---|---|---|
| Ruff | 0.16.10 | line length 100; rules E, W, F, I, B, UP, SIM, RUF; `docs/` excluded | Lint and format Python |
| mypy | 2.4.0 | `strict = true` on `core/` and `tools/` | Type checking |
| pre-commit | 4.6.2 | Local hooks calling `uv run --locked …` | Run the checks on every commit |
| Hypothesis | 6.168.5 | Installed; first property tests arrive with the P3 schema | Generated-input tests |
| pytest | 9.1.1 | `core/tests` | Test runner (from ADR11) |

The copied registry validator (`tools/research/validate_registry.py`) was reformatted and
given type hints to pass these checks. Its output is byte-identical before and after.

## Why

- **Ruff** replaces black, isort and flake8 with one fast tool and one config.
- **Strict mypy from day one** is cheap on new code and expensive to add later. The data
  contract (P3) and feature units (P5) carry units and missing-value rules where a type
  checker catches real mistakes.
- **pre-commit with local hooks** reuses the versions locked in `uv.lock`, so a commit
  that passes locally passes in CI. No second list of tool versions to keep in sync.
- **Hypothesis** suits feature code: heading wrap, unit conversion, out-of-order
  timestamps and missing values are exactly the edge cases random generation finds.
- **Docs excluded from Ruff**: Ruff 0.16 also formats code blocks inside Markdown; the
  research documents are prose and stay untouched by formatters.

## Pros

- One command set, same result locally and in CI.
- Problems are caught before a PR exists.
- Strict typing documents data shapes in the code itself.

## Cons

- Strict mypy slows the first draft of new code and needs stubs or `type: ignore` for
  untyped third-party libraries (likely: some simulator and blockchain clients).
- pre-commit hooks need `uv` installed and add a few seconds to each commit.
- Hypothesis tests run longer than example tests and need a fixed seed profile in CI to
  stay reproducible (to add with the first property test).
- Rule selection is a judgment call; some rules (for example `SIM`) are stylistic.

## Alternatives considered

| Alternative | Why not chosen | When it would be better |
|---|---|---|
| black + isort + flake8 | Three tools and configs doing what Ruff does | If a required plugin exists only for flake8 |
| Pyright instead of mypy | Equally good; mypy is more common in research code | If the team uses VS Code/Pylance and wants the same checker in the editor |
| Non-strict mypy | Lets untyped code accumulate | If a third-party-heavy module makes strict typing impractical (exclude that module only) |
| pre-commit with upstream hook repos | Pins tool versions twice (hook rev and `uv.lock`) | If contributors won't have `uv` installed |
| No Hypothesis until P5 | Owner chose to set it up now | — |

## How to retest

```bash
uv sync --locked
uv run ruff check && uv run ruff format --check
uv run mypy
uv run pytest
uv run pre-commit run --all-files     # all four hooks: Passed
```

## How to change or revert

Edit `[tool.ruff]`, `[tool.ruff.lint]` or `[tool.mypy]` in `pyproject.toml`. Disable a
hook by deleting it from `.pre-commit-config.yaml`; remove all hooks with
`uv run pre-commit uninstall`. Remove a tool with `uv remove --dev <tool>`.

## Revisit trigger

A dependency cannot be typed, check time per commit exceeds about 10 seconds, or the team
changes editors.
