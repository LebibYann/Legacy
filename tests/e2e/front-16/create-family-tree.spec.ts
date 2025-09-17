import { test, expect } from '@playwright/test';

// base URL for the tests in english
const urlBase = 'http://localhost:2316/en';

test('f16-faef1 - Create a family tree: from an empty file', async ({ page, browser }) => {
  await page.goto(urlBase);
  await page.getByRole('listitem').filter({ hasText: 'from an empty file (gwc)' }).getByRole('link').click();
  await page.getByRole('textbox').click();
  await page.getByRole('textbox').fill('chromatophilic');
  await page.getByRole('button', { name: 'Create' }).click();
  await page.getByRole('button', { name: 'Ok' }).click();
  await expect(page.getByRole('link', { name: 'http://localhost:2317/chromatophilic' })).toBeVisible();
});