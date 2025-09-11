# Test Policy: GWD Setup (GeneWeb Frontend)

## 1) Testing context & scope

This policy applies to all components of the GWD Setup frontend and GeneWeb backend it interacts with. It covers TypeScript UI code, OCaml backend code, Dockerized services, and CI/CD pipelines. The policy sets organizational standards for quality, coverage, automation, and risk management for all test activities.

---

## 2) Quality rules

### Definition of Done (DoD)

A feature or bugfix is considered **done** when:

* All acceptance criteria are met and demonstrated.
* Unit tests meet or exceed coverage thresholds (≥85% statements, ≥80% branches).
* E2E and integration tests pass in all supported browsers (Chromium, Firefox, WebKit).
* Performance SLAs met (home page <1.5s, GEDCOM import/export limits as specified).
* Accessibility smoke checks pass (axe-core automated rules, WCAG 2.1 AA basic compliance).
* Security linting, dependency audits, and container scans have no critical findings.
* Documentation (code, API, tests) is updated and reviewed.

---

## 3) Overall testing strategy

* **Shift-left testing**: Tests are written as early as possible, with TDD for units and BDD for user scenarios.
* **Automation first**: All repeatable scenarios are automated using Playwright, Vitest, and OCaml dune/alcotest.
* **Risk-based exploratory testing**: Focus manual exploratory sessions on import/export edge cases, genealogy merges, and scaling.
* **Continuous integration**: All code merges require automated checks (unit, integration, E2E smoke) to pass.
* **Continuous delivery readiness**: Staging and pre-production environments mirror production for performance, security, and regression testing.
* **Regression prevention**: Automated test suites run on every commit; flaky tests triaged weekly.
* **Code quality gates**: PRs cannot merge if coverage or linting thresholds are not met.

---

## 4) Test levels

* **Unit testing**: TS and OCaml modules; strict typing enforced.
* **Integration testing**: Validates interaction between frontend and backend services.
* **End-to-end testing**: Covers user flows (diagram scenarios) in all major browsers.
* **Performance testing**: Client-side timings via Playwright + Lighthouse, server load tests as needed.
* **Accessibility testing**: Automated axe-core scans and manual audits.

---

## 5) Risk tolerance

* **Critical defects**: Zero tolerance in production; blockers must be resolved before release.
* **High defects**: Cannot ship; requires patch or rollback.
* **Medium/Low defects**: Documented with remediation plan; may defer if risk is acceptable.
* **Performance regressions**: >10% degradation triggers investigation.
* **Security issues**: No P0/P1 vulnerabilities allowed; must be patched before deployment.

---

## 6) Roles & responsibilities

| Role                               | Responsibilities                                                                                      |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **QA Lead**                        | Define testing strategy, manage coverage metrics, own risk assessments, sign off releases.            |
| **Developers**                     | Write unit tests (TDD), contribute to E2E automation, maintain test fixtures, review PRs for quality. |
| **DevOps Engineer**                | Maintain CI/CD pipelines, Docker environments, monitoring, and artifact storage.                      |
| **Product Owner**                  | Approve acceptance criteria, prioritize defects, sign off UAT.                                        |
| **Exploratory Tester/QA Engineer** | Conduct manual exploratory sessions, accessibility audits, document findings.                         |
| **Security Engineer**              | Perform audits, vulnerability scanning, and ensure compliance.                                        |

---

## 7) Review & evolution

This policy will be reviewed quarterly or after major releases to adapt coverage targets, SLAs, and risk posture as the application scales.
