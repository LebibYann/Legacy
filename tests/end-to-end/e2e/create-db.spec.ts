import { test, expect } from '@playwright/test';
import assert from "assert";

const url = process.env.FRONT_SETUP_URL;
assert(url, 'FRONT_SETUP_URL is not defined');
const name = process.env.NAME;
assert(name, 'NAME is not defined');


test('f16-faef1 - Create a family tree: from an empty file', async ({ page, browser }) => {
  await page.goto(url);
  // await page.waitForURL("commit");
  await page.getByRole('listitem').filter({ hasText: 'from an empty file (gwc)' }).getByRole('link').click();
  await page.getByRole('textbox').click();
  await page.getByRole('textbox').fill('chromatophilic');
  await page.getByRole('button', { name: 'Create' }).click();
  await page.getByRole('button', { name: 'Ok' }).click();
  await expect(page.getByRole('link', { name: 'http://localhost:2317/chromatophilic' })).toBeVisible();
});