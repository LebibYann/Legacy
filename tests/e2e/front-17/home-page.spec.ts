import { test, expect } from '@playwright/test';
import { defineConfig } from '@playwright/test';

export default defineConfig({
  use: {
    storageState: 'state.json', // Réutilise l'état dans tous les tests
  },
});

// command npx playwright codegen http://localhost:2317/chromatophilic?lang=en

const urlBase = 'http://localhost:2317/chromatophilic?lang=en';

test('f17-hp1 - Home Page: Check database name', async ({ page }) => {
  await page.goto(urlBase);
  await expect(page.getByRole('heading')).toContainText('Genealogical database chromatophilic');
});

test('f17-hp2 - Home Page: Check individual count', async ({ page }) => {
  await page.goto(urlBase);
  await expect(page.locator('#welcome')).toContainText('5 individuals');
});

test('f17-hp3 - Home Page: Search for individual', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('combobox', { name: 'First name·s' }).click();
  await page.getByRole('combobox', { name: 'First name·s' }).fill('john');
  await page.getByRole('button', { name: ' Search' }).click();
  await expect(page.locator('#content')).toContainText('john doe 1980–2050');
});