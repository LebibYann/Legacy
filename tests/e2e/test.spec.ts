import { test, expect } from '@playwright/test';

/**
 * Remplace "mafamille" par le nom de la base que tu as créée via gwsetup.
 * Si tu ne sais pas encore, commence par créer la base dans http://localhost:2317
 */
const baseName = process.env.GW_BASE ?? 'mafamille';

test('gwd répond et sert la base', async ({ page }) => {
  await page.goto('http://localhost:2317/', { waitUntil: 'domcontentloaded' });

  // 2) Vérifier que la page est chargée
  await expect(page.locator('body')).toBeVisible();
});