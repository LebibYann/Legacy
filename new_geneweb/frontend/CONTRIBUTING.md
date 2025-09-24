# 🤝 Contributing to GeneWeb Frontend

Thanks for considering contributing to the **GeneWeb frontend**!  
This document provides guidelines to ensure consistency and maintain quality across the project.

---

## 🛠 Development Setup

1. Fork and clone the repository:

   ```bash
   git clone https://github.com/EpitechPGE45-2025/G-ING-900-PAR-9-1-legacy-11.git
   cd new_geneweb/frontend
   ```

2. Install dependencies:

   ```bash
   npm ci
   ```

3. Copy environment variables:

   ```bash
   cp .env.example .env
   ```

4. Start the development server:

   ```bash
   npm run dev
   ```

5. Open the application:
   [http://localhost:5174](http://localhost:5174)

---

## 🌱 Branching Strategy

We follow a simple Git branching model:

- `dev`: main development branch.
- `feature/*`: new features.
- `fix/*`: bug fixes.
- `chore/*`: tooling, configuration, CI/CD.
- `docs/*`: documentation only.

Branches are merged into `dev` via Pull Requests.

---

## 📝 Commit Convention

We use **[Conventional Commits](https://www.conventionalcommits.org/)**:

```
<type>(scope): short description
```

**Types:**

- `feat`: new feature.
- `fix`: bug fix.
- `chore`: maintenance, infra, tooling (CI, Docker…).
- `docs`: documentation only.
- `style`: formatting (no code change).
- `refactor`: code change without adding features or fixing bugs.
- `test`: tests only.
- `ci`: CI/CD configuration.
- `build`: build system or dependencies.

**Examples:**

- `feat(auth): add admin login form`
- `fix(ui): correct navbar spacing on mobile`
- `ci(frontend): add GitHub Actions workflow for tests`

---

## 🎨 Code Style

We enforce consistent formatting and linting:

- **Prettier** → formatting
- **ESLint** → linting
- **TypeScript** → type checking
- **TailwindCSS v4** → styling

Run before committing:

```bash
npm run lint
npm run check
```

---

## 🧪 Tests

- Unit and functional tests are written with **Vitest**.
- Some tests run in a browser environment with **Playwright**.
- All new features and bug fixes must include tests.

Run tests locally:

```bash
npm run test
```

If Chromium is missing:

```bash
npx playwright install --with-deps chromium
```

---

## ✅ Pull Requests

- Open PRs against the `dev` branch.
- Ensure CI passes (lint, type-check, tests, Docker build).
- Use a clear PR title (same as commit convention).
- Include a PR description with:
  - Goal / Motivation
  - Summary of changes
  - How to test

---

## 🐳 Docker Workflow (Optional)

You can also run the frontend inside Docker:

```bash
docker compose up --build
```

Run commands inside the container:

```bash
docker compose exec frontend npm run test
```

---

## 📖 Documentation

The frontend serves as the administration interface for GeneWeb.
Refer to the [Backend README](../backend/README.md) for API details.

