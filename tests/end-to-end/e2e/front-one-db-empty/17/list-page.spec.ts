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

  test(`f16-lp3.2 - List Page: Display database name`, async ({ page }) => {
    await page.goto(url);

    // Wait for the loading state to finish
    await expect(page.getByText("Loading databases...")).toBeHidden({ timeout: 5000 });

    // Now check if the database link is visible
    await expect(page.getByRole('link', { name: "chromatophilic" })).toBeVisible({ timeout: 5000 });
  });

  testLinksNavigation(url);
}