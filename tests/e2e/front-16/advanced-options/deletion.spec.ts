import { test, expect } from '@playwright/test';

const urlBase = 'http://localhost:2316/en';

test('d1 - Verify No Database Message', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('link', { name: 'delete' }).click();
  await expect(page.getByRole('cell')).toContainText('- here is no database at present');
});

test('d2 - Verify Deletion Functionality', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('link', { name: 'delete' }).click();
  await page.locator('input[name="test"]').check();
  await page.getByRole('button', { name: 'Check' }).click();
  await page.getByRole('button', { name: 'Delete' }).click();
  await expect(page.locator('body')).toContainText('test');
});