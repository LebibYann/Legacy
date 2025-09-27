import { test, expect } from '@playwright/test';
import assert from "assert";

const url = process.env.FRONT_USER_URL;
assert(url, 'FRONT_USER_URL is not defined');
const urlBase = url + '/chromatophilic?lang=en';

test('f17-con1 - Configuration: Check configuration', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('button', { name: 'Configuration' }).click();
  await expect(page.locator('#bvar-list')).toContainText('Mode: Classic: chromatophilic.gwf ');
});

//feature not yet available
test('f17-an1 - Add note: Create a new note', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('button', { name: 'Add note', exact: true }).click();
  await page.getByRole('textbox', { name: 'Name of the new note: Name of' }).click();
  await page.getByRole('textbox', { name: 'Name of the new note: Name of' }).fill('test note chromatophilic 1');
  await page.getByRole('textbox', { name: 'Name of the new note: Name of' }).press('Enter');
  await page.getByRole('link', { name: ' Display' }).click();
  await expect(page.getByTitle('Modify the note')).toBeVisible();
  await expect(page.getByTitle('Modify the section')).toBeVisible();
});

test('f17-ans1 - Add notes: View all notes', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('button', { name: 'Add notes' }).click();
  await page.getByRole('link', { name: 'View' }).click();
  await expect(page.getByTitle('Modify the note')).toBeVisible();
  await expect(page.getByTitle('Modify the section')).toBeVisible();
});

test('f17-ps1 - Places / Surname: Search for a place', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('button', { name: 'Places/surname' }).click();
  await page.getByRole('link', { name: 'Berlin' }).click();
  await expect(page.getByRole('searchbox', { name: 'Place (k)' })).toHaveValue('Berlin');
  await page.getByRole('link', { name: '1', exact: true }).click();
  await expect(page.locator('body')).toContainText('jane smith');
});

test('f17-ani1 - Anniversaries: See all anniversaries', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('button', { name: 'Anniversaries' }).click();
  await page.getByRole('link', { name: 'Birthdays' }).click();
  await page.getByRole('button', { name: 'Submit' }).click();
  await expect(page.getByRole('paragraph')).toContainText('No anniversary.');
});

test('f17-ani2 - Anniversaries: See all anniversaries of dead people', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('button', { name: 'Anniversaries' }).click();
  await page.getByRole('link', { name: 'Anniversaries of dead people' }).click();
  await page.getByRole('combobox').selectOption('2');
  await page.getByRole('button', { name: 'Submit' }).click();
  await expect(page.locator('body')).toContainText('jane smith');
});

test('f17-ani3 - Anniversaries: See all weddings anniversaries', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('button', { name: 'Anniversaries' }).click();
});


const today = new Date();
const day = today.getDate();
const month = today.getMonth() + 1;   // 0 → 11 → on ajoute +1
const year = today.getFullYear();

test('f17-ca1 - Calendars: Check calendar', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('button', { name: 'Calendars' }).click();
  await expect(page.locator('tbody')).toContainText('Gregorian');
  await expect(page.locator('select[name="mg"]')).toHaveValue(month.toString());
  await expect(page.locator('input[name="dg"]')).toHaveValue(day.toString());
  await expect(page.locator('input[name="yg"]')).toHaveValue(year.toString());
});

test('f17-st1 - Statistics: See latest 20 births', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('button', { name: 'Statistics' }).click();
  await page.getByRole('link', { name: 'latest 20 births' }).click();
  await expect(page.locator('body')).toContainText('July 2014lisa junior, born on 7 July 2014.');
  await expect(page.locator('body')).toContainText('May 2012alice junior, born on 5 May 2012.');
  await expect(page.locator('body')).toContainText('March 2010johny junior, born on 3 March 2010.');
  await expect(page.locator('body')).toContainText('February 1982jane smith, born on 2 February 1982.');
  await expect(page.locator('body')).toContainText('January 1980john doe, born on 1 January 1980.');
});