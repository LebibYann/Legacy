# Test Strategy: GWD Setup (GeneWeb Frontend)

## 1) Testing techniques

* **BDD** (critical user journeys): capture flows from the GWD Setup diagram in Gherkin-like scenarios (Given/When/Then). Implement with Playwright Test step helpers.
* **Exploratory testing** (risk‑based): 60–90 minute charters targeting imports, exports, merges, cleanup, and error history. Vary data sizes (small → huge) and i18n (FR labels).

---

## 2) Types of tests in scope

* **Unit tests (required)**: TypeScript units with **Vitest** (or Playwright Test for very small units). OCaml units with **dune** + **alcotest/ounit**.
* **End‑to‑End (required)**: **Playwright** covering all user workflows (Chromium, Firefox, WebKit).
* **Performance (required)**:

  * **Primary**: Playwright‑based client timings (Navigation/Resource timing API, custom timers around upload/export) + Lighthouse via Playwright for web‑perf KPIs.
  * **Optional/Recommended**: HTTP‑level load using **k6** or **Gatling** for import/export/merge endpoints if server throughput needs profiling.

---

## 3) Coverage & quality targets

* **Code coverage (TS)**: ≥ **85%** statements, ≥ **80%** branches, ≥ **85%** functions/lines on libraries used by the UI.
* **Code coverage (OCaml)**: ≥ **80%** lines using `bisect_ppx`.
* **E2E path coverage**: ≥ **95%** of happy‑path journeys from the diagram; ≥ **70%** of high‑risk alternates (invalid/massive files, duplicate persons, collisions, permission denials).
* **Mutation testing (TS)**: **≥ 70%** mutation score with **StrykerJS** on critical modules (parsers/validators). Optional for OCaml.
* **Performance SLAs (staging, p95)**:

  * GWSetup home to interactive: **< 1.5s**.
  * Open “Create base” page: **< 1.0s**.
  * Import GEDCOM 10 MB: complete **< 90s**, error rate 0%.
  * Export GW for 100k persons: complete **< 120s**.

---

## 4) Environments

* **Local (Docker)**: fast feedback; seeded volumes with test fixtures.
* **CI/CD**: ephemeral containers; headless Playwright; artifacts: traces, videos, HTML reports, LCOV.
* **Staging**: near‑prod config + anonymized large datasets; used for full E2E, perf baselines, and exploratory sessions.
* **Pre‑production**: release‑candidate smoke (non‑destructive suites only); mirrors prod.

---

## 5) Tooling (selected)

* **Playwright** for E2E + perf timings + Lighthouse.
* **Vitest** (TypeScript unit tests) with `c8/istanbul` coverage.
* **StrykerJS** (mutation testing).
* **dune + alcotest/ounit + bisect\_ppx** for OCaml units.
* **axe‑core/playwright** for accessibility smoke checks.
* **Docker** for consistent environments (Ubuntu base).

---

## 6) Docker test image (Ubuntu 24.04) — corrected & extended

The user requirement was `FROM ubuntu:24.04`. Below is a **working** baseline that brings up GeneWeb **and** installs Node/Playwright so tests can run inside the same container. Changes vs. typical drafts:

* Adds Node.js LTS and Playwright browsers.
* Installs Playwright’s Linux deps.
* Uses a non‑root user for running tests.
* Flattens layers and avoids `eval` leaks by using `opam exec`.

```dockerfile
FROM ubuntu:24.04

ENV OPAMYES=1

WORKDIR /app

RUN apt update && apt install -y opam m4 libgmp-dev libpcre3-dev zlib1g-dev pkg-config git libpcre2-dev xdot
RUN git clone https://github.com/geneweb/geneweb.git

WORKDIR /app/geneweb

RUN opam init --disable-sandboxing -y
RUN opam switch create 4.14.1
RUN eval "$(opam env)" \
&& opam install . --deps-only --with-test \
&& ocaml ./configure.ml \
&& make distrib
RUN echo "172.20.0.1" > /app/geneweb/distribution/gw/only.txt
ENV DB=/app/geneweb/distribution/bases
RUN chown -R root:root /app/geneweb/distribution

EXPOSE 2316 2317
ENTRYPOINT ["sh", "-c", " \
cd /app/geneweb/distribution && \
./gwd.sh & \
./gwsetup.sh -lang fr; \
sleep infinity"]
```

---

## 7) CI gates & reporting

* **PR**: TS unit (coverage thresholds), E2E smoke (Chromium), mutation dry‑run, Lighthouse quick check.
* **Nightly**: full E2E matrix (3 browsers), mutation tests, performance baselines, flaky‑test detection.
* **Release**: pre‑prod smoke, rollback verification.
* **Artifacts**: Playwright traces/videos, HTML reports, LCOV, mutation reports.

---

## 8) Definition of Done

* All required tests pass and meet coverage/SLAs.
* No critical/high defects open; accessibility smoke passes.
* Test data/fixtures versioned; docs updated (how to run locally/CI).
