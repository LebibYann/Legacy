import { test, expect } from '@playwright/test';

const urlBase = 'http://localhost:2316/en';

test('sgwsf1 - Save: Save a GeneWeb source file', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('listitem').filter({ hasText: 'a GeneWeb source file (gwu)' }).getByRole('link').click();
  await page.getByRole('row', { name: 'chromatophilic' }).getByRole('radio').check();
  await page.locator('input[name="o"]').click();
  await page.locator('input[name="o"]').fill('chromatophilic');
  await page.locator('input[name="isolated"]').check();
  await page.getByRole('button', { name: 'Extract' }).click();
  await page.getByRole('button', { name: 'Ok' }).click();
});