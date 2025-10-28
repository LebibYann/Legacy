// playwright.config.ts
import { defineConfig, devices, ViewportSize } from '@playwright/test';

import dotenv from 'dotenv';
import path from 'path';
import assert from "assert";

// Determine which environment to load based on command line argument or environment variable
const envFile = process.env.ENV_FILE || '.env.caml';
// Load the specific environment file
const envPath = path.resolve(process.cwd(), envFile);
dotenv.config({ path: envPath, quiet: true });

assert(process.env.FRONT_USER_URL, 'FRONT_USER_URL is not defined');
assert(process.env.FRONT_SETUP_URL, 'FRONT_SETUP_URL is not defined');

const browserLanguage = process.env.BROWSER_LANGUAGE || 'en-US';

const browsers = [
  {
    name: 'chromium',
    use: {
      ...devices['Desktop Chrome'],
      locale: browserLanguage,
      // For Chromium, you can also set specific language preferences
      launchOptions: {
        args: [`--lang=${browserLanguage}`]
      }
    }
  },
  {
    name: 'firefox',
    use: {
      ...devices['Desktop Firefox'],
      locale: browserLanguage,
      // For Firefox, you can set language preference
      launchOptions: {
        firefoxUserPrefs: {
          'intl.accept_languages': browserLanguage.replace('-', ',').toLowerCase()
        }
      }
    }
  },
  {
    name: 'webkit',
    use: {
      ...devices['Desktop Safari'],
      locale: browserLanguage
    }
  },
];

type Project = {
  name: string;
  testDir?: string;
  testMatch?: RegExp;
  retries?: number;
};

type BrowserUse = {
  viewport: ViewportSize;
  userAgent: string;
  deviceScaleFactor: number;
  isMobile: boolean;
  hasTouch: boolean;
  defaultBrowserType: "chromium" | "firefox" | "webkit";
}

type Browser = {
    name: string;
    use: BrowserUse;
}

function generateProjectOrder(browser: Browser, projects: Project[]): Object[] {
  let orderedProjects: Object[] = [];
  let prevName: string | null = null;

  for (const p of projects) {
    const full_name = `${browser.name}-${p.name}`;
    let project: Object = {
      name: full_name,
      use: browser.use,
    }
    if (p.retries) {
      (project as any).retries = p.retries;
    }
    if (p.testDir) {
      (project as any).testDir = p.testDir;
    } else {
      (project as any).testMatch = p.testMatch;
    }
    if (prevName) {
      (project as any).dependencies = [prevName];
    }
    orderedProjects.push(project);
    prevName = full_name;
  }

  return orderedProjects;
}

// génère les projects pour chaque navigateur et chaque étape
const projects = browsers.flatMap((browser) => generateProjectOrder(browser, [
    { name: 'front-no-db', testDir: './e2e/front-no-db' },
    { name: 'create-db', testMatch: /.*create-db\.spec\.ts/ },
    { name: 'front-one-db-empty', testDir: './e2e/front-one-db-empty' },
    { name: 'create-family', testMatch: /.*create-family\.spec\.ts/ },
    { name: 'front-one-db', testDir: './e2e/front-one-db' },
    { name: 'create-second-db', testMatch: /.*create-second-db\.spec\.ts/ },
    { name: 'front-two-db', testDir: './e2e/front-two-db' },
    { name: 'cleanup-db', testMatch: /.*cleanup-db\.spec\.ts/ },
    { name: 'delete-db', testMatch: /.*delete-db\.spec\.ts/ },
  ]));

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false, // ⚡ Ensure tests are run in order
  retries: 1,
  reporter: 'html',
  use: {
    headless: false,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    httpCredentials: {
      username: 'admin',
      password: 'admin',
    },
  },
  projects
});

