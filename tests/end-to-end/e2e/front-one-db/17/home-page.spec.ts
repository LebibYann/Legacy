import { test, expect, defineConfig } from '@playwright/test';
import assert from "assert";

const url = process.env.FRONT_USER_URL;
assert(url, 'FRONT_USER_URL is not defined');
const urlBase = url + '/chromatophilic?lang=en';
const name = process.env.NAME;
assert(name, 'NAME is not defined');

export default defineConfig({
  use: {
    storageState: 'state.json', // Reuse the authentication state
  },
});


test('f17-hp3 - Home Page: Check individuals count', async ({ page }) => {
  await page.goto(urlBase);
  await expect(page.locator('#welcome')).toContainText('5 individuals');
});

test('f17-hp4 - Home Page: Search for individual', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('combobox', { name: 'First name·s' }).click();
  await page.getByRole('combobox', { name: 'First name·s' }).fill('john');
  await page.getByRole('button', { name: ' Search' }).click();
  await expect(page.locator('#content')).toContainText('john doe 1980–2050');
});
