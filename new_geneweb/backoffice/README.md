# 🖥️ GeneWeb Backoffice

Backoffice web application for the modernized **GeneWeb** project, built with **SvelteKit**, **TypeScript**, and **TailwindCSS**.
It provides an administrative interface for managing genealogy data and integrates with the GeneWeb backend.

This project might not work properly without the backend running.
Please ensure that the backend is up and running before using the backoffice or run the docker at the root of this project.

---

## 📦 Requirements

- **Node.js 20+**
- **npm** (or pnpm/yarn)
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Getting Started

### Installation

1. Clone the repository and navigate to the backoffice directory:

   ```bash
   git clone https://github.com/EpitechPGE45-2025/G-ING-900-PAR-9-1-legacy-11.git
   cd new_geneweb/backoffice
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

   This will automatically run the postinstall script to compile Paraglide translations.

3. Configure environment variables:

   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file as needed for your environment.

### Development

Start the development server with hot reload:

```bash
npm run dev
```

The application will be available at [http://localhost:5173](http://localhost:5173)

#### Additional Development Commands

- `npm run prepare` - Sync SvelteKit configuration
- `npm run check` - Type check the project
- `npm run check:watch` - Type check in watch mode

#### API SDK

The API SDK is automatically generated using the following command:

```bash
npx openapi-typescript http://localhost:2317/api/openapi.json -o src/lib/api/schema.ts
```

If the endpoints change in the [backend](../backend/README.md), re-run the command to update the SDK.
While having the backend up, the current url set in the command up there assume you have started the backend from the provided docker.

---

## 🏗️ Building

### Production Build

Build the application for production:

```bash
npm run build
```

This will:

1. Compile Paraglide translations
2. Build the SvelteKit application

The built application will be in the `build/` directory.

### Preview Production Build

Preview the production build locally:

```bash
npm run preview
```

### Run build

```bash
node build
```

---

## 🧪 Testing

### Unit Tests

Run unit tests using Vitest:

```bash
npm run test:unit
```

For watch mode during development:

```bash
npm run test:unit -- --watch
```

The project uses:

- **Vitest** for unit testing
- **@vitest/browser** for browser-based testing
- **vitest-browser-svelte** for Svelte component testing
- **@vitest/coverage-v8** for code coverage

Test results and coverage reports are generated in the `coverage/` directory.

---

## 🔍 Code Quality

### Linting

The project uses ESLint for code linting:

```bash
npm run lint:check    # Check for lint errors
npm run lint:fix      # Fix automatically fixable lint errors
```

### Formatting

The project uses Prettier for code formatting:

```bash
npm run lint:format   # Format all files
npm run lint:check    # Check if files are properly formatted
```

### Combined Linting and Formatting

```bash
npm run lint          # Run both formatting and linting
```

---

## ⚡ Performance Testing

### Lighthouse

Run Lighthouse performance audits:

```bash
npm run lighthouse
```

This will:

1. Build the production version
2. Run Lighthouse CI automated tests

Lighthouse reports are generated in the `.lighthouseci/` directory.

## Complete Test Suite

Run all tests (unit tests, linting, and Lighthouse):

```bash
npm run tests
```

---

## 🐳 Docker Environment

### Using Docker Compose

1. Go to the root of the project.
2. Build and start containers:

   ```bash
   docker compose up --build
   ```

3. The following services will be available:
   - Backoffice → [http://localhost:5173](http://localhost:5173)

### Using Docker Directly

```bash
# Build Docker image
docker build -t backoffice .

# Run container
docker run -p 5173:5173 backoffice
```

---

## 🛠️ Technology Stack

- **SvelteKit** - Full-stack web framework
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Paraglide** - Internationalization (i18n)
- **Vite** - Build tool and development server
- **Vitest** - Unit testing framework
- **ESLint** - Code linting
- **Prettier** - Code formatting
- **Lighthouse CI** - Performance testing

---

## 📁 Project Structure

```
src/
├── components/         # Reusable Svelte components
├── lib/                # Shared utilities and stores
├── paraglide/          # Internationalization files
├── routes/             # SvelteKit routes and pages
└── utils/              # Utility functions

static/                 # Static assets
messages/               # Translation files
tests/                  # Test files
coverage/               # Test coverage reports
.lighthouseci/          # Lighthouse audit results
```

---

## 🌍 Internationalization

The project supports multiple languages using Paraglide:

- English (en)
- French (fr)
- German (de)
- Spanish (es)
- Italian (it)
- Latvian (lv)
- Swedish (sv)
- Corsican (co)

Translation files are located in the `messages/` directory.

---

## 📖 Documentation

Once running, the backoffice provides an admin interface for GeneWeb.
For API details, see the [Backend README](../backend/README.md).

---

## 🤝 Contributing

1. Follow the existing code style
2. Run `npm run lint` before committing
3. Ensure all tests pass with `npm run tests`
4. Add tests for new features

Please read the [CONTRIBUTING.md](../../CONTRIBUTING.md) for details on:

- Branching strategy
- Commit conventions (Conventional Commits)
- Code style rules
- PR review process
