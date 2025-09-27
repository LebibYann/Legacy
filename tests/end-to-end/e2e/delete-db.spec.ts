import { test, expect } from '@playwright/test';
import assert from "assert";

const url = process.env.FRONT_SETUP_URL;
assert(url, 'FRONT_SETUP_URL is not defined');

test('f16-d2 - Deletion: Verify Deletion Functionality', async ({ page }) => {
  await page.goto(url);
  await page.getByRole('link', { name: 'delete' }).click();
  await page.locator('input[name="chromatophilic"]').check();
  await page.getByRole('button', { name: 'Check' }).click();
  await page.getByRole('button', { name: 'Delete' }).click();
  await expect(page.locator('body')).toContainText('chromatophilic');
});
