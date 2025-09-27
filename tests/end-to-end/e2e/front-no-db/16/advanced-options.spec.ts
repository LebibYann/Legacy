import { test, expect } from '@playwright/test';
import assert from "assert";

const url = process.env.FRONT_SETUP_URL;
assert(url, 'FRONT_SETUP_URL is not defined');

test('f16-cu1 - Cleanup: Verify No Database Message', async ({ page }) => {
  await page.goto(url);
  await page.getByRole('link', { name: 'cleanup' }).click();
  await expect(page.getByRole('cell')).toContainText('- here is no database at present');
});

test('f16-d1 - Deletion: Verify No Database Message', async ({ page }) => {
  await page.goto(url);
  await page.getByRole('link', { name: 'delete' }).click();
  await expect(page.getByRole('cell')).toContainText('- here is no database at present');
});