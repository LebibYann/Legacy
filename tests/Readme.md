# Tests End‑to‑End GeneWeb avec Playwright

Ce guide explique **comment lancer les tests de zéro** sur Windows/macOS/Linux, en local et via Docker. Il est pensé pour l’équipe, avec des commandes prêtes à copier‑coller.

---

## 🔧 Prérequis

* **Docker Desktop** (si vous utilisez le service GeneWeb en conteneur)
  • Windows : activer **WSL2** et le moteur Linux dans Docker Desktop.
* **Node.js 20 LTS** et **npm** (pour l’option “local”).
* GeneWeb lancé localement sur `http://localhost:2316` (gwd) et `http://localhost:2317` (gwsetup).

> Si vous partez de zéro : `docker compose up -d` à la racine du projet (là où se trouve `docker-compose.yml`).

---

## 📁 Arborescence recommandée

```
mon-projet/
├─ docker-compose.yml
├─ genweb/
│  └─ Dockerfile
├─ tests/
│  ├─ package.json
│  ├─ tsconfig.json
│  ├─ playwright.config.ts
│  └─ e2e/
│     └─ gwsetup.spec.ts (exemples de tests)
└─ .gitignore
```

---

## 🧩 Fichiers “tests” (modèle)

**tests/package.json**

```json
{
  "name": "geneweb-e2e",
  "private": true,
  "type": "module",
  "devDependencies": {
    "@playwright/test": "^1.47.0",
    "typescript": "^5.5.0",
    "@types/node": "^22.0.0"
  },
  "scripts": {
    "install:browsers": "playwright install",
    "test": "playwright test",
    "test:ui": "playwright test --ui",
    "codegen": "playwright codegen"
  }
}
```

**tests/tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "types": ["node", "@playwright/test"],
    "baseUrl": "."
  },
  "include": ["**/*.ts"]
}
```

**tests/playwright.config.ts**

```ts
import { defineConfig, devices } from '@playwright/test';

const baseURL = process.env.PLAYWRIGHT_BASE_URL ?? 'http://localhost:2316';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  retries: 1,
  reporter: 'html',
  use: {
    baseURL,
    headless: true, // passer à false localement si vous voulez voir le navigateur
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox',  use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit',   use: { ...devices['Desktop Safari'] } }
  ]
});
```

**tests/e2e/gwsetup.spec.ts** (exemple simple)

```ts
import { test, expect } from '@playwright/test';

test('gwsetup accessible et premier formulaire interactif', async ({ page }) => {
  await page.goto('http://localhost:2317/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('body')).toContainText(/gwsetup|GeneWeb/i);

  const forms = page.locator('form');
  const count = await forms.count();
  if (count > 0) {
    const firstForm = forms.first();
    const submit = firstForm.locator('input[type="submit"], button[type="submit"]').first();
    if (await submit.count()) {
      await submit.click();
    }
  }
});
```

**.gitignore** (minimal)

```gitignore
node_modules/
playwright-report/
test-results/
blob-report/
trace/
trace.zip
*.log
.DS_Store
Thumbs.db
```

---

## 🚀 Démarrage – Option A (Local Node.js)

1. Installer les dépendances Playwright :

```bash
cd tests
npm i
npm run install:browsers
```

2. S’assurer que GeneWeb tourne :

```bash
cd ..
docker compose up -d geneweb
```

3. Lancer les tests :

```bash
cd tests
npm test
```

4. Voir le rapport HTML : `tests/playwright-report/index.html`

> Pour **voir le navigateur** : `npm run test:ui` ou mettez `headless: false` dans `playwright.config.ts`.

---

## 🐳 Démarrage – Option B (100% Docker)

Ajoutez ce service à votre `docker-compose.yml` :

```yaml
services:
  geneweb:
    # ... votre service existant ...
    healthcheck:
      test: ["CMD-SHELL", "wget -qO- http://127.0.0.1:2317/ > /dev/null 2>&1 || exit 1"]
      interval: 10s
      timeout: 3s
      retries: 10

  pw:
    image: mcr.microsoft/playwright:latest
    working_dir: /tests
    depends_on:
      geneweb:
        condition: service_healthy
    environment:
      PLAYWRIGHT_BASE_URL: http://geneweb:2316
      GW_BASE: mafamille  # (si vos tests l’utilisent)
    volumes:
      - ./tests:/tests
    command: ["npx", "playwright", "test", "--reporter=line"]
```

Lancer uniquement les tests :

```bash
docker compose up --build pw
```

Les rapports s’écrivent dans `tests/playwright-report/` via le volume monté.

---

## 🧪 Scripts utiles

* `npm test` → lance tous les tests en headless.
* `npm run test:ui` → lance l’UI Playwright (débogage, navigateur visible).
* `npm run codegen` → ouvre l’enregistreur d’actions (génère un test de base).

ASTUCE : Exécuter un seul test :

```bash
npx playwright test e2e/gwsetup.spec.ts --project=chromium --headed
```

---

## 🌱 Variables d’environnement

* `PLAYWRIGHT_BASE_URL` (par défaut `http://localhost:2316`) : base URL de gwd.
* `GW_BASE` : nom de la base GeneWeb utilisée par certains tests.

Exemple (PowerShell) :

```powershell
$env:PLAYWRIGHT_BASE_URL="http://localhost:2316"
$env:GW_BASE="mafamille"
npm test
```

---

## 🩺 Dépannage rapide

* **`Cannot find name 'process'`** → installez `@types/node` et vérifiez `tsconfig.json` ci‑dessus.
* **Avertissement `moduleResolution node10`** → utilisez `module: "NodeNext"` et `moduleResolution: "NodeNext"`.
* **Voir le test se dérouler** → `npm run test:ui` ou `headless: false` dans la config.
* **Docker ne répond pas (Windows)** → Docker Desktop en mode **Linux/WSL2**, redémarrer via *Troubleshoot* si besoin.
* **404 sur gwd** → créez une base via `http://localhost:2317/` puis accédez à `http://localhost:2316/?b=<nom_de_base>`.

---

## ✅ Check‑list CI/CD (optionnel)

* Utilisez l’image `mcr.microsoft/playwright:latest` pour éviter d’installer les navigateurs.
* Marquez les artefacts Playwright (rapport HTML, traces) comme *build artifacts* de votre pipeline.
* Rendez le service `pw` dépendant d’un **healthcheck** sur `geneweb`.

---

Besoin d’ajuster ce README à votre stack (Svelte v5, Tailwind v4, proxy, HTTPS) ? Dites‑nous et on ajoute les sections nécessaires.
