import { test, expect } from '@playwright/test';
import assert from "assert";

const url = process.env.FRONT_USER_URL;
assert(url, 'FRONT_USER_URL is not defined');
const urlBase = url + '/chromatophilic?lang=en';

test('f17-fn1 - First names: See all first names', async ({ page }) => {
    await page.goto(urlBase);
    await page.getByRole('button', { name: ' First names' }).click();
    await expect(page.locator('#main-content')).toContainText('alice');
    await expect(page.locator('#main-content')).toContainText('jane');
    await expect(page.locator('#main-content')).toContainText('john');
    await expect(page.locator('#main-content')).toContainText('johny');
    await expect(page.locator('#main-content')).toContainText('lisa');
});

test('f17-oc1 - Occupations: See all occupations', async ({ page }) => {
    await page.goto(urlBase);
    await page.getByRole('button', { name: ' Occupations' }).click();
    await expect(page.locator('#main-content')).toContainText('Artist');
    await expect(page.locator('#main-content')).toContainText('Doctor');
    await expect(page.locator('#main-content')).toContainText('Engineer');
    await expect(page.locator('#main-content')).toContainText('Musician');
    await expect(page.locator('#main-content')).toContainText('Student');
    await expect(page.getByLabel('sub-caracter-selection-heading')).toContainText('A');
    await expect(page.getByLabel('sub-caracter-selection-heading')).toContainText('D');
    await expect(page.getByLabel('sub-caracter-selection-heading')).toContainText('E');
    await expect(page.getByLabel('sub-caracter-selection-heading')).toContainText('M');
    await expect(page.getByLabel('sub-caracter-selection-heading')).toContainText('S');
});