# ADR13: GitHub Actions runs every check on each pull request

Status: accepted · 9 October 2026 · Decided by: Mohamed Hamdoun (CI on GitHub Actions);
workflow details proposed by Claude, open to change · Plan step 0.4

## Decision

`.github/workflows/ci.yml` runs on every pull request and on pushes to `main`:

1. `uv sync --locked` — install the exact locked environment (fails if `uv.lock` is stale).
2. `ruff check`, `ruff format --check`, `mypy`, `pytest`.
3. `tools/research/validate_registry.py`.

Details:

- Runner `ubuntu-latest`, 10-minute timeout, read-only repository token.
- Actions pinned to full commit hashes: `actions/checkout` v7.0.1 (`3d3c42e5…`),
  `astral-sh/setup-uv` v10.2.0 (`c18668ad…`), resolved from GitHub on 9 October 2026.
- uv pinned to 0.7.13, the version that wrote `uv.lock`; dependency cache enabled.

## Why

Pre-commit hooks can be skipped (`--no-verify`) or not installed on another machine. CI is
the check nobody can skip, and its result appears on every PR. Running the same commands
as the hooks keeps one definition of "passing".

Pinning actions by commit hash prevents a moved or compromised tag from running new code
with access to the repository. A read-only token limits what a faulty step can do.

## Pros

- Every PR shows pass/fail before review.
- The environment is rebuilt from the lockfile on a clean Linux machine, which also
  catches macOS-only assumptions.
- Supply-chain exposure from third-party actions is limited to two pinned commits.

## Cons

- Private repositories on the free plan get a limited monthly allowance of Actions
  minutes (2,000 at the time of writing); this workflow should take about a minute.
- Pinned hashes do not update themselves; new action versions need a deliberate change.
- Linux-only: macOS-specific problems on the development machine are not covered.
- Only one job: later phases (web, simulator, chain) will need separate path-filtered jobs.

## Alternatives considered

| Alternative | Why not chosen | When it would be better |
|---|---|---|
| Local checks only | Can be skipped; nothing visible on PRs | Offline work, or if Actions minutes run out |
| Actions pinned by tag (`@v7`) | A tag can be moved to different code | Never for third-party actions; acceptable for GitHub's own if updates matter more |
| Matrix over Python versions | ADR11 pins one Python version | If the package is ever published for others to install |
| macOS runner too | Costs 10× the minutes of Linux runners on private repos | If a macOS-only bug appears |
| GitLab CI / self-hosted runner | Repository is on GitHub; extra setup | If minutes or data-privacy rules require it |

## How to retest

Open any pull request and check the `ci / check` status. Locally, the same steps:

```bash
uv sync --locked && uv run ruff check && uv run ruff format --check \
  && uv run mypy && uv run pytest && uv run python tools/research/validate_registry.py
```

## How to change or revert

Edit or delete `.github/workflows/ci.yml`. To update an action, look up the new release's
commit hash (`gh api repos/<owner>/<repo>/git/ref/tags/<tag>`) and replace both the hash
and the version comment. To make CI required before merging, enable branch protection on
`main` (GitHub repository settings).

## Revisit trigger

New folders with their own toolchains (`web/`, `sim/`, `chain/`), Actions minutes running
low, or a new major version of a pinned action.
