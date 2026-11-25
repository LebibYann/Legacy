import { test, expect } from '@playwright/test';
import assert from "assert";

const url = process.env.FRONT_SETUP_URL;
assert(url, 'FRONT_SETUP_URL is not defined');
const name = process.env.NAME;
assert(name, 'NAME is not defined');

test('f16-ft1 - Family Trees: click list, check no database message', async ({ page }) => {
  await page.goto(url);
  await page.getByRole('link', { name: 'list' }).click();
  await expect(page.getByRole('listitem')).toContainText('here is no database at present');
});