import { test, expect } from '@playwright/test';

const url = 'http://localhost:2316';
const urlBase = 'http://localhost:2316/en';

// command npx playwright codegen http://localhost:2316/en 

test('hp1 - Home Page: Home Page Elements Visibility', async ({ page }) => {
  await page.goto(urlBase);
  await expect(page.getByText('Consult', { exact: true })).toBeVisible();
  await expect(page.getByText('Create Family Tree')).toBeVisible();
  await expect(page.getByText('Save')).toBeVisible();
  await expect(page.getByText('Advanced Options')).toBeVisible();
  await expect(page.getByText('Configure')).toBeVisible();
});

test('hp2 - Home Page: Language Selection Functionality', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('link', { name: 'Corsu' }).click();
  await expect(page).toHaveURL(url + '/co');
  await page.getByRole('link', { name: 'Deutsch' }).click();
  await expect(page).toHaveURL(url + '/de');
  await page.getByRole('link', { name: 'English' }).click();
  await expect(page).toHaveURL(url + '/en');
  await page.getByRole('link', { name: 'Español' }).click();
  await expect(page).toHaveURL(url + '/es');
  await page.getByRole('link', { name: 'Français' }).click();
  await expect(page).toHaveURL(url + '/fr');
  await page.getByRole('link', { name: 'Italiano' }).click();
  await expect(page).toHaveURL(url + '/it');
  await page.getByRole('link', { name: 'Latviesu' }).click();
  await expect(page).toHaveURL(url + '/lv');
  await page.getByRole('link', { name: 'Svenska' }).click();
  await expect(page).toHaveURL(url + '/sv');
});

test('hp3 - Home Page: GitHub Link Functionality', async ({ page }) => {
  await page.goto('http://localhost:2316/en');
  await page.getByRole('link').filter({ hasText: /^$/ }).click();
  await expect(page).toHaveURL('https://github.com/geneweb/geneweb/');
});

// not working
// test('hp4 - Home Page: Documentation Link Functionality', async ({ page }) => {
//   await page.goto('http://localhost:2316/en');
//   await page.getByRole('link', { name: 'doc' }).click();
//   await expect(page).toHaveURL('http://geneweb.tuxfamily.org/wiki/manual');
// });
