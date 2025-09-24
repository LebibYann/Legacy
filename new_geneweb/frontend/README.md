# 🖥️ GeneWeb Frontend

Frontend web application for the modernized **GeneWeb** project, built with **SvelteKit**, **TypeScript**, and **TailwindCSS**.  
It provides an administrative interface for managing genealogy data and integrates with the GeneWeb backend.

---

## 📦 Requirements

- **Node.js 20+**
- **npm** (or pnpm/yarn)
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Setup

### Local Environment (without Docker)

1. Clone the repository:

   ```bash
   git clone https://github.com/EpitechPGE45-2025/G-ING-900-PAR-9-1-legacy-11.git
   cd new_geneweb/frontend
   ```

2. Install dependencies:

   ```bash
   npm ci
   ```

3. Configure environment variables:

   ```bash
   cp .env.example .env
   ```

4. Start the development server:

   ```bash
   npm run dev
   ```

5. Open the application in your browser:
   [http://localhost:5174](http://localhost:5174)

---

### Docker Environment

1. Build and start containers:

   ```bash
   docker compose up --build
   ```

2. The following services will be available:
   - Frontend → [http://localhost:5174](http://localhost:5174)

---

## 🧪 Tests & Quality

Run locally with npm:

```bash
# Unit, functional tests and e2e tests
npm run test

# Linting
npm run lint

# Type checking
npm run check

# Accessibility & Lighthouse audits
npm run lighthouse
```

If Playwright is not installed, install Chromium:

```bash
npx playwright install --with-deps chromium
```

---

## ⚙️ Project Structure

```
frontend/
├── src/
│   ├── routes/         # SvelteKit routes
│   ├── lib/            # Utilities
│   ├── components/     # UI components
│   └── app.d.ts        # Global types
├── tests/              # Unit & functional tests
├── e2e/                # e2e tests
├── Dockerfile
├── package.json
└── vite.config.ts
```

---

## 📖 Documentation

Once running, the frontend provides an admin interface for GeneWeb.
For API details, see the [Backend README](../backend/README.md).

---

## 🤝 Contributing

Please read the [CONTRIBUTING.md](./CONTRIBUTING.md) for details on:

- Branching strategy
- Commit conventions (Conventional Commits)
- Code style rules
- PR review process
