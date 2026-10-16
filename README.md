# gha-monorepo-changed-services

In a monorepo, testing everything on every change wastes time. This workflow works out **which services a change touches** and tests only those, with one stable `gate` check that stays reliable when jobs are skipped.

```
changes (git diff -> matrix JSON) -> test (matrix, only changed services) -> gate (roll-up)
```

## The rules (`scripts/changed.py`, unit-tested)

| Changed file | Tests run for |
|---|---|
| `services/b/...` | service `b` only |
| `shared/`, `scripts/`, the CI workflow | every service (they affect all) |
| README, docs | nothing |

## What ran (2026-10-16)

- **First push** (no earlier commit to compare with): tested **both** services, then the gate passed.
- **A change inside `services/b` only:** `changes`, `test (b)` and `gate` ran; **`test (a)` did not run**.
- **A README-only change:** `changes` and `gate` ran, **`test` was skipped** (no services to test), and the gate still passed, so a docs edit costs seconds.
- The detector has 5 unit tests (single service, two services, shared means all, docs mean none, unknown service ignored), run in CI before it is used.

## Decisions

- **`fetch-depth: 0`** so the base commit exists for the diff.
- **Skip the matrix when nothing changed** (`if: any == 'true'`): an empty matrix makes the job error.
- **A `gate` job with `if: always()`** is the one check to require in branch protection. Matrix job names change and a skipped job is not a failed one; the gate fails only on a real failure or cancellation.
- **Path rules in code, with tests,** not scattered across workflow `paths:` filters.

## Honest limits

- Path rules are hand-written; a dependency graph (Bazel, Nx, Turborepo) does this properly. A service that imports another is not modelled.
- For a pull request the base is the PR's base commit; for a push it is `github.event.before`. A force-push or a very first push falls back to "test everything".
- Only unit tests of two toy services; no build or deploy stage.

MIT licensed.
