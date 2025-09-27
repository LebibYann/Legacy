import { test, expect } from '@playwright/test';
import assert from "assert";

const url = process.env.FRONT_SETUP_URL;
assert(url, 'FRONT_SETUP_URL is not defined');

test('f16-hp1 - Home Page: Home Page Elements Visibility', async ({ page }) => {
  await page.goto(url);
  await expect(page.getByText('Consult', { exact: true })).toBeVisible();
  await expect(page.getByText('Create Family Tree')).toBeVisible();
  await expect(page.getByText('Save')).toBeVisible();
  await expect(page.getByText('Advanced Options')).toBeVisible();
  await expect(page.getByText('Configure')).toBeVisible();
});

test('f16-hp2 - Home Page: Language Selection Functionality', async ({ page }) => {
  await page.goto(url);
  const elem_to_check: string[][] = [
    ['Corsu', 'Ghjestione è Creazione'],
    ['Deutsch', 'Verwaltung und Erstellung'],
    ['English', 'Management and creation'],
    ['Español', 'Ggestión y Creación'],
    ['Français', 'Gestion et création'],
    ['Italiano', 'Gestione e la creazione'],
    ['Latviesu', 'Vadiba un veidosana'],
    ['Svenska', 'ledning och skapande'],
  ];
  for (const [lang, title] of elem_to_check) {
    await page.getByRole('link', { name: lang }).click();
    await expect(page.getByText(title)).toBeVisible()
  }
});

test('f16-hp3 - Home Page: GitHub Link Functionality', async ({ page }) => {
  await page.goto(url);
  await page.getByRole('link').filter({ hasText: /^$/ }).click();
  await expect(page).toHaveURL('https://github.com/geneweb/geneweb/');
});

test('f16-hp4 - Home Page: Check All Links Exist (Ommits gwb related href)', async ({ page }) => {
  await page.goto(url);

  const hrefs: string[] = [
    "list",
    "errors",
    "gwc",
    "cleanup",
    "delete",
    "merge",
    "consang",
    "update_nldb",
    "connex",
    "gwdiff",
    "gwfixbase",
    ".gwf",
    "gwd",
    "cache_files",
    "doc",
  ]

  for (const href of hrefs) {
    await expect(page.getByRole('link', { name: href }).first()).toBeVisible();
  }
});