# End-to-End GeneWeb Tests with Playwright

This guide explains **how to run the tests from scratch** on Windows/macOS/Linux, both locally and via Docker. It is designed for the team, with ready-to-copy commands.

---

## 🔧 Prerequisites

* **Docker** or **Docker Desktop on Windows**
* **Node.js 20 LTS** and **npm**
* Install **Playwright extension** on vscode to run tests easily

---

## 📁 Directory Structure

```
Legacy/
├─ geneweb/
│  ├─ Dockerfile
│  └─ docker-compose.yml
├─ new_geneweb/
├─ tests/
│  ├─ package.json
│  ├─ tsconfig.json
│  ├─ playwright.config.ts
│  └─ e2e/
│     └─ e2e/
│        ├─ tests folders...
│        └─ tests files...
├─ docs/
└─ .gitignore
```

---

## 🏷️ Test Naming Convention

All test names follow the format:

```
fXX-yyy - Page: Description
```

### Breakdown

* **`fXX`** → the frontend / feature area under test.
  Example: `f16` = feature 16, the Home Page.

* **`yyy`** → the unique test identifier.
  Example: `hp1` = first test for the Home Page.

* **`Page: Description`** → explains the location (page or component) and what the test does.
  Example: `Home Page: Home Page Elements Visibility` = verifies that the expected elements on the Home Page are visible.

#### Example

```
f16-hp1 - Home Page: Home Page Elements Visibility
```

* **f16** = Home Page frontend.
* **hp1** = first test for the Home Page.
* **Home Page: Home Page Elements Visibility** = checks that elements on the Home Page are visible.

---

## 🚀 Getting Started

1. Run Docker

```bash
cd geneweb_docker
docker compose --profile ephemeral up --build
```
> The ephemeral profile will create a temporary environment for testing. It guarantees a clean state for each run of the tests. You however need to restart the container to reset its state. So do not forget to restart it between tests runs.

* It will take some time to build the first time you run it; next time it's quicker to run.

2. Install Playwright dependencies:

```bash
cd tests
npm i
npm run install:browsers
```

3. Run the tests:

* To run the tests

```bash
cd tests/end-to-end
npm test
```

* To run a specific test using the code of a test

```bash
cd tests/end-to-end
npx playwright test --grep "${code} --project=chromium-*"
```

```bash
cd tests
npx playwright test --grep "${code} --project=chromium-*"
```

* To run tests on a specific web browser
- chromium
- firefox
- webkit

```bash
cd tests/end-to-end
npm run test:name_of_browser
```

---

## 🧪 Useful Commands

* To remove all the Docker volumes (do this if you run all the tests multiple times):

```bash
docker compose down -v
docker compose up -d
docker compose up --build
```

* To use codegen to make a test easier and quicker:
```bash
npx playwright codegen http://localhost:2316/en
```

---

## ✅ CI/CD Checklist

<!-- Add your CI/CD checklist here -->

---

## 🧪 E2E Test Coverage

Below is a summary of the E2E test files and their coverage:

| Test Code     | File                                         | Quick Description (edit as needed)                     |
|---------------|----------------------------------------------|--------------------------------------------------------|
| f16-hp1       | e2e/front-16/home-page.spec.ts               | Home Page: Elements visibility                         |
| f16-hp2       | e2e/front-16/home-page.spec.ts               | Home Page: Navigation                                  |
| f16-hp3       | e2e/front-16/home-page.spec.ts               | Home Page: Other checks                                |
| f16-d1        | e2e/front-16/advanced-options.spec.ts        | Advanced Options: Demo/test                            |
| f16-cu1       | e2e/front-16/consult.spec.ts                 | Consult: Family tree navigation                        |
| f16-ft1       | e2e/front-16/create-family-tree.spec.ts      | Create Family Tree: Initial creation                   |
| f16-faef1     | e2e/front-16/save.spec.ts                    | Save: Features after DB creation                       |
| f16-ft2       | e2e/front-16/create-family-tree.spec.ts      | Create Family Tree: Additional scenarios               |
| f17-hp1       | e2e/front-17/home-page.spec.ts               | Home Page (front 17): Elements visibility              |
| f17-hp2       | e2e/front-17/home-page.spec.ts               | Home Page (front 17): Navigation                       |
| f17-af1       | e2e/front-17/books.spec.ts                   | Books: Add/Edit/Delete/View                            |
| f17-hp3       | e2e/front-17/home-page.spec.ts               | Home Page (front 17): Other checks                     |
| f17-hp4       | e2e/front-17/home-page.spec.ts               | Home Page (front 17): Additional scenarios             |
| f17-con1      | e2e/front-17/tools.spec.ts                   | Tools: Consult/utility                                 |
| f17-an1       | e2e/front-17/tools.spec.ts                   | Tools: Analysis                                        |
| f17-ans1      | e2e/front-17/tools.spec.ts                   | Tools: Analysis scenario 1                             |
| f17-ps1       | e2e/front-17/tools.spec.ts                   | Tools: Post-save actions                               |
| f17-ani1      | e2e/front-17/tools.spec.ts                   | Tools: Animation 1                                     |
| f17-ani2      | e2e/front-17/tools.spec.ts                   | Tools: Animation 2                                     |
| f17-ani3      | e2e/front-17/tools.spec.ts                   | Tools: Animation 3                                     |
| f17-ca1       | e2e/front-17/tools.spec.ts                   | Tools: Calculation                                     |
| f17-st1       | e2e/front-17/tools.spec.ts                   | Tools: Statistics                                      |
| f17-fn1       | e2e/front-17/tools.spec.ts                   | Tools: Functionality                                   |
| f17-oc1       | e2e/front-17/tools.spec.ts                   | Tools: Other checks                                    |

---
