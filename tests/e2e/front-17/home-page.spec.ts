import { test, expect } from '@playwright/test';
import { defineConfig } from '@playwright/test';

export default defineConfig({
  use: {
    storageState: 'state.json', // Réutilise l'état dans tous les tests
  },
});

const urlBase = 'http://localhost:2317/chromatophilic?lang=en';

test('hp1 - Home Page: Check database name', async ({ page }) => {
  await page.goto(urlBase);
  await expect(page.getByRole('heading')).toContainText('Genealogical database chromatophilic');
});

