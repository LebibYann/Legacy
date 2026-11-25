import { test, expect } from '@playwright/test';
import assert from "assert";

const url = process.env.FRONT_SETUP_URL;
assert(url, 'FRONT_SETUP_URL is not defined');
const name = process.env.NAME;
assert(name, 'NAME is not defined');

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
    ['English', (name === "caml" ? 'Management and creation' : 'Management and Creation')],
    ['Español', (name === "caml" ? 'Ggestión y Creación' : "Gestión y Creación")],
    ['Français', (name === "caml" ? 'Gestion et création' : 'Gestion et Création')],
    ['Italiano', (name === "caml" ? 'Gestione e la creazione' : 'Gestione e Creazione')],
    ['Latviesu', (name === "caml" ? 'Vadiba un veidosana' : 'Vadība un Veidošana')],
    ['Svenska', (name === "caml" ? 'ledning och skapande' : 'Hantering och Skapande')],
  ];

  for (const [lang, title] of elem_to_check) {
    // Cherche d'abord un bouton, sinon un lien
    const langButton = page.getByRole('button', { name: lang });
    const langLink = page.getByRole('link', { name: lang });

    if (await langButton.count()) {
      await page.waitForLoadState('networkidle');
      await langButton.click();
    } else if (await langLink.count()) {
      await langLink.click();
    } else {
      throw new Error(`Language switch for ${lang} not found`);
    }

    await expect(page.getByText(title)).toBeVisible();
  }
});

test('f16-hp3 - Home Page: GitHub Link Functionality', async ({ page }) => {
  await page.goto(url);
  if (name === "caml") {
    await page.getByRole('link').filter({ hasText: /^$/ }).click();
  } else {
    await page.locator('a[href="https://github.com/geneweb/geneweb/"]').click();
  }
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