import { test, expect } from '@playwright/test';

const urlBase = 'http://localhost:2316/en';



test('cu2 - Cleanup: Verify Cleanup Functionality', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('link', { name: 'cleanup' }).click();
  await page.getByRole('row', { name: 'chromatophilic' }).getByRole('radio').check();
  await page.getByRole('button', { name: 'Clean up' }).click();
  await page.getByRole('button', { name: 'Ok' }).click();
  await expect(page.getByRole('link', { name: 'http://localhost:2317/test' })).toBeVisible();
});

test('cu1 - Cleanup: Verify No Database Message', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('link', { name: 'cleanup' }).click();
  await expect(page.getByRole('cell')).toContainText('- here is no database at present');
});

test('d1 - Deletion: Verify No Database Message', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('link', { name: 'delete' }).click();
  await expect(page.getByRole('cell')).toContainText('- here is no database at present');
});

test('d2 - Deletion: Verify Deletion Functionality', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('link', { name: 'delete' }).click();
  await page.locator('input[name="test"]').check();
  await page.getByRole('button', { name: 'Check' }).click();
  await page.getByRole('button', { name: 'Delete' }).click();
  await expect(page.locator('body')).toContainText('chromatophilic');
});

