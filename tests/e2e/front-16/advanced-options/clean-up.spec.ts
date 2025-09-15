import { test, expect } from '@playwright/test';

const urlBase = 'http://localhost:2316/en';

test('cu1 - Verify No Database Message', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('link', { name: 'cleanup' }).click();
  await expect(page.getByRole('cell')).toContainText('- here is no database at present');
});

test('cu2 - Verify Cleanup Functionality', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('link', { name: 'cleanup' }).click();
  await page.getByRole('row', { name: 'test' }).getByRole('radio').check();
  await page.getByRole('button', { name: 'Clean up' }).click();
  await page.getByRole('button', { name: 'Ok' }).click();
  await expect(page.getByRole('link', { name: 'http://localhost:2317/test' })).toBeVisible();
});