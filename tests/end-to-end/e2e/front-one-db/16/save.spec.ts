import { test, expect } from '@playwright/test';
import assert from "assert";

const url = process.env.FRONT_SETUP_URL;
assert(url, 'FRONT_SETUP_URL is not defined');

test('f16-sgwsf1 - Save: Save a GeneWeb source file', async ({ page }) => {
  await page.goto(url);
  await page.getByRole('listitem').filter({ hasText: 'a GeneWeb source file (gwu)' }).getByRole('link').click();
  await page.getByRole('row', { name: 'chromatophilic' }).getByRole('radio').check();
  await page.locator('input[name="o"]').click();
  await page.locator('input[name="o"]').fill('chromatophilic');
  await page.locator('input[name="isolated"]').check();
  await page.getByRole('button', { name: 'Extract' }).click();
  await page.getByRole('button', { name: 'Ok' }).click();
});