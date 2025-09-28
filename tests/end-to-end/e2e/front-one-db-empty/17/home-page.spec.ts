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


if (name === 'caml') {
  test('f17-hp1 - Home Page: Check database name', async ({ page }) => {
    await page.goto(urlBase);
    await expect(page.getByRole('heading')).toContainText('Genealogical database chromatophilic');
  });

  test('f17-hp2 - Home Page: Check individual count', async ({ page }) => {
    await page.goto(urlBase);
    await expect(page.locator('#welcome')).toContainText('0 individual');
  });
}