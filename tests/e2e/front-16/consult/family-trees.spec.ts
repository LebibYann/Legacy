import { test, expect } from '@playwright/test';

// base URL for the tests in french
const urlBase = 'http://localhost:2316/en';

test('ft1 - Family Trees: click list, check no database message', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('link', { name: 'list' }).click();
  await expect(page.getByRole('listitem')).toContainText('here is no database at present');
});





