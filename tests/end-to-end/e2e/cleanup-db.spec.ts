import { test, expect } from '@playwright/test';
import assert from "assert";

const url = process.env.FRONT_SETUP_URL;
assert(url, 'FRONT_SETUP_URL is not defined');
const name = process.env.NAME;
assert(name, 'NAME is not defined');


test('f16-cu2 - Cleanup: Verify Cleanup Functionality', async ({ page }) => {
  await page.goto(url);
  await page.getByRole('link', { name: 'cleanup' }).click();
  await page.getByRole('row', { name: 'chromatophilic' }).getByRole('radio').check();
  await page.getByRole('button', { name: 'Clean up' }).click();
  await page.getByRole('button', { name: 'Ok' }).click();
  await expect(page.getByRole('link', { name: 'http://localhost:2317/chromatophilic' })).toBeVisible();
});