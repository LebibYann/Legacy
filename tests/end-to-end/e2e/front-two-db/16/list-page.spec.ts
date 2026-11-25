import { test, expect } from '@playwright/test';
import assert from "assert";
import {
  testHomePageElementsVisibility,
  testGitHubLinkFunctionality,
  testLinksNavigation
} from '../../shared/list-page-tests.js';

const url = process.env.FRONT_SETUP_URL + "/list";
assert(url, 'FRONT_SETUP_URL is not defined');
const name = process.env.NAME;
assert(name, 'NAME is not defined');

testGitHubLinkFunctionality(url, name);

if (name === "svelte") {
  testHomePageElementsVisibility(url);

  test(`f16-lp3.3 - List Page: Displays multiple databases`, async ({ page }) => {
    await page.goto(url);

    // Wait for the loading state to finish
    await expect(page.getByText("Loading databases...")).toBeHidden({ timeout: 5000 });

    // Check if all database links are visible
    for (const dbName of ['chromatophilic', 'pineapple']) {
      await expect(page.getByRole('link', { name: dbName })).toBeVisible({ timeout: 5000 });
    }
  });

  testLinksNavigation(url);
}