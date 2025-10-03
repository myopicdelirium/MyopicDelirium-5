# Contributing to MyopicDelirium-5

## Branching
- `main` is protected. **Never push directly.**
- Use short-lived topic branches:
  - `feat/<name>` for new features
  - `fix/<name>` for bug fixes
  - `hotfix/<name>` only if `main` is broken and must be repaired immediately

## Workflow
1. Create an issue with clear acceptance criteria.
2. Create a branch from `main`:  
   `git checkout -b feat/<short-name>`
3. Make changes and commit with descriptive messages.
4. Run `scripts/verify.sh` locally. It must pass before opening a PR.
5. Open a pull request into `main`.
6. PRs must include:
   - Problem statement
   - Approach taken
   - Files changed
   - Test plan (commands run + expected results)
   - Risk / rollback plan
7. PRs require:
   - At least **1 approval**
   - Passing CI (which runs `scripts/verify.sh`)
   - Linear history (squash or rebase, no merge commits)

## Pre-commit
- Run `pre-commit run --all-files` before pushing.
- Fix formatting/lint errors locally; do **not** bypass CI unless in a `hotfix/*` branch.

## Commands
- **Smoke run**:  
  ```bash
  PYTHONPATH=src python -m tholos.cli.run_sim --config configs/base.yaml
