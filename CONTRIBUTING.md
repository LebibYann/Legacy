# 🤝 Contributing Guide

This document explains how to submit high‑quality contributions and keep history clean.

---

## 🧭 Core Principles

- Readability and maintainability first.
- Every change should be traceable (Issue ↔ PR ↔ Commits).
- Small, focused PRs > large, hard-to-review PRs.
- Code ships with tests + docs (not later).
- Automate what can be automated (lint, format, tests, security).

---

## ⚙️ Git Configuration Setup

**Important for Windows users**: Configure Git to use Unix line endings (LF) instead of Windows line endings (CRLF) to maintain consistency across different operating systems.

### Initial Git Setup

Run these commands once after cloning the repository:

```bash
# Configure line ending handling globally (recommended)
git config --global core.autocrlf false
git config --global core.eol lf

# Or configure only for this repository
git config core.autocrlf false
git config core.eol lf

# Ensure existing files use correct line endings
git add --renormalize .
git commit -m "chore: normalize line endings to LF"
```

### Verify Configuration

Check your Git configuration:

```bash
git config --list | grep -E "(autocrlf|eol)"
```

Expected output:
```
core.autocrlf=false
core.eol=lf
```

### Why This Matters

- **Consistency**: All developers work with the same line endings regardless of OS
- **CI/CD**: Prevents build failures due to line ending differences
- **Diffs**: Avoids false changes in Git diffs caused by line ending conversions
- **Cross-platform**: Ensures code works identically on Linux, macOS, and Windows

### .gitattributes File

The repository includes a `.gitattributes` file that enforces LF line endings for text files. This works in conjunction with your Git configuration.

---

## 🌿 Branching Strategy

* `main`: always deployable
* `dev`: main development branch
* `issueID-issue`: new issue

---

## 📝 Commit Messages

Use (simplified) Conventional Commits:

```
type(scope?): concise imperative subject

Optional body: explain in details.
Optional Refs: #ISSUE
```

Types: feat, fix, docs, chore, refactor, test, perf, ci, build, revert.

Example:
```
feat(api): add /health endpoint
```

---

## 🧪 Quality & Local Checks

Before pushing, please run all tests.
No PR should decrease test or coverage thresholds.

---

## 🔐 Security

Never commit secrets (API keys, tokens).
Report vulnerabilities privately (security contact / SECURITY.md).
Avoid unmaintained or license-unclear dependencies.

---

## 🧩 Contribution Workflow

1. Create / locate an Issue (avoid duplicates).
2. Clarify scope if ambiguous.
3. Branch from dev.
4. Implement in small atomic commits.
5. Add/update tests + docs + CHANGELOG (if used).
6. Run lint / tests locally.
7. Open a Pull Request using the template.
8. Address review feedback.
9. Clean up your branch history before merge if requested:
   - **Rebase**: use it if your commits are already clean, logical, and well-structured (keeps full history).
   - **Squash**: use it if you made many small, noisy, or fix commits (combines them into one or a few meaningful commits).
10. Merge according to project policy.

---

## 🔍 Code Review Checklist

Author:
- [ ] Issue linked
- [ ] Scope focused
- [ ] Tests added/updated
- [ ] No dead/debug code (print / console.log)
- [ ] Clear naming
- [ ] Docs / README updated
- [ ] No obvious duplication
- [ ] Consistent error handling

Reviewer:
- [ ] Intent quickly understandable
- [ ] Critical paths covered by tests
- [ ] No unnecessary tech debt introduced
- [ ] Consistent with existing patterns
- [ ] Performance acceptable
- [ ] Input validation / security considered
- [ ] No secret leakage

---

## 🗂 Issue Management

Suggested labels:

- **Type**
  - `type: bug` → Fix incorrect behavior
  - `type: feature` → Implement a new functionality
  - `type: task` → Maintenance, refactor, or non-feature work

- **Priority**
  - `priority: P0` → Must-have, blocker
  - `priority: P1` → Important, but not blocking
  - `priority: P2` → Nice-to-have / low impact

- **Size (effort estimation)**
  - `size: XS` → < 1h
  - `size: S` → < 0.5 day
  - `size: M` → 1–2 days
  - `size: L` → 3–5 days
  - `size: XL` → > 1 week

- **Process**
  - `status: backlog` → Needs clarification
  - `status: ready` → Ready to work on
  - `status: in-progress` → Being worked on
  - `status: in-review` → Being reviewed
  - `status: done` → Completed Issue

---

## 💬 Communication

Quick questions: GitHub Discussions / internal chat.
Architecture decisions: captured in Issue or ADR (docs/adr/NNN-title.md).

---

## 🧱 Technical Debt

Track debt via dedicated issues (label: tech-debt).
Do not leave silent TODOs.

TODO format:
```
// TODO(#123): reason + intended resolution
```

---

## 🐛 Issue Template

Copy/paste:

```
# 🎯 Goal
_A clear and concise description of the purpose of this issue.
Why is this change needed?_

---

# ✅ Tasks
- [ ] Describe task 1
- [ ] Describe task 2
- [ ] Describe task 3

---

# 📦 Deliverables
_List the concrete outputs expected._
- Deliverable 1
- Deliverable 2
- Deliverable 3

---

# 🔗 Linked Issues
_Related references._
- Related to #ISSUE_NUMBER
- Part of Epic #ISSUE_NUMBER
```

---

## 🔀 Pull Request Template

```
## 🎯 Goal
Describe the main purpose of this PR.
- What problem does it solve?
- Why is it needed?
- (Optional) Screenshots / diagrams

---

## ✅ Tasks
Check what applies:

- [ ] Project setup / refactor
- [ ] New feature
- [ ] Fix / bug correction
- [ ] Tests (unit / functional / e2e)
- [ ] Documentation update
- [ ] CI / CD changes
- [ ] Docker / Infra changes

_Subtasks (if any):_
- [ ] Added /health endpoint
- [ ] Configured mypy
- [ ] Updated docker-compose.yml

---

## 📦 Deliverables
Examples:
- Backend API with health check
- Dockerized environment (PostgreSQL)
- CI pipeline (lint + tests)
- Updated README

---

## 🔗 Linked Issues
Closes #XX
Relates to #YY
```

---

## 🧪 Testing Strategy (Suggested)

- Unit: pure logic (fast).
- Integration: module / DB / external service interaction.
- E2E: minimal critical flows.
- Coverage: aim for threshold appropriate to legacy state.
- Every bug fix adds a regression test.

---

## 🗃 Legacy Areas

Please never push a modification of the legacy code. The old program
is used as an oracle for our modernization and must never change.

---

## 🔍 Project-Specific Conventions (Post-Audit)

This section replaces the generic placeholders with the actual tools and practices adopted by the project.

- **Linters**
  - Python: `flake8`, `isort`
  - Frontend: `eslint` (with TypeScript rules)

- **Formatters**
  - Python: `black`
  - Frontend: `prettier`

- **Stack**
  - Backend: FastAPI (Python 3.12) with SQLAlchemy + Alembic
  - Frontend: Svelte 5 with TypeScript
  - Database: PostgreSQL (Dockerized)

- **CI/CD**
  - Platform: GitHub Actions
  - Jobs: `lint & typecheck`, `unit & functional tests`, `docker build validation`, `quality gate`

- **Deployment Flow**
  - `dev` → development branch (feature branches merged here)
  - `main` → stable branch (release-ready, production reference)

- **Database Migration Tooling**
  - Alembic (managed via Poetry)
  - Migrations must be generated after any schema change:
    ```bash
    poetry run alembic revision --autogenerate -m "describe change"
    poetry run alembic upgrade head
    ```

- **Coverage Thresholds**
  - Backend (pytest): 80% minimum coverage
  - Frontend (Jest/Cypress): 80% minimum coverage

- **Containerization**
  - Backend service: Dockerfile (Poetry-based)
  - Orchestration: `docker-compose.yml` (backend + PostgreSQL)
  - Entrypoint automatically runs Alembic migrations before starting the FastAPI app

## 📂 Component-Specific Guidelines

In addition to this global guide, some parts of the project include their own
`CONTRIBUTING.md` with technical details and conventions specific to that area:

- [`new_geneweb/backend/CONTRIBUTING.md`](./backend/CONTRIBUTING.md) → FastAPI, Alembic, SQLAlchemy, Pytest
- [`new_geneweb/backoffice/CONTRIBUTING.md`](./backoffice/CONTRIBUTING.md) → Svelte 5, Typescript, Vitest
- [`new_geneweb/frontend/CONTRIBUTING.md`](./frontend/CONTRIBUTING.md) → Svelte 5, Typescript, Vitest

Always check the local guide before contributing to a specific component.
