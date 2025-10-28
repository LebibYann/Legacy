import { test, expect } from '@playwright/test';
import type { Page } from '@playwright';
import assert from "assert";

const url = process.env.FRONT_USER_URL;
assert(url, 'FRONT_USER_URL is not defined');
const urlBase = url + '/chromatophilic?lang=en';
const name = process.env.NAME;
assert(name, 'NAME is not defined');

function synchroniousWait(ms: number) {
  let current = Date.now();
  while (Date.now() - current < ms) {}
}

async function checkElementWhenReady(page: Page, elemLocator: string, fill: string, ) {
  const elem = page.locator(elemLocator);

  await expect(elem).toBeVisible({ timeout: 10000 });
  await expect(elem).toBeEnabled();
  await elem.fill(fill);
  // synchroniousWait(100);
}

test('f17-af1 - Add Family: Create a new family', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('button', { name: 'Add family' }).click();
  
  // Fill all parent fields
  await page.waitForLoadState("domcontentloaded");
  await page.getByRole('textbox', { name: 'First name (M)' }).fill('john');
  await page.getByRole('textbox', { name: 'Surname' }).nth(0).fill('doe');
  await checkElementWhenReady(page, 'input[name="pa1b_mm"]', '01');
  await checkElementWhenReady(page, 'input[name="pa1b_dd"]', '01');
  await checkElementWhenReady(page, 'input[name="pa1b_yyyy"]', '1980');
  await checkElementWhenReady(page, 'input[name="pa1b_pl"]', 'Paris');
  await checkElementWhenReady(page, 'input[name="pa1d_mm"]', '12');
  await checkElementWhenReady(page, 'input[name="pa1d_dd"]', '12');
  await checkElementWhenReady(page, 'input[name="pa1d_yyyy"]', '2050');
  await checkElementWhenReady(page, 'input[name="pa1d_pl"]', 'London');
  await checkElementWhenReady(page, 'input[name="pa1_occu"]', 'Engineer');
  await page.getByRole('textbox', { name: 'First name (F)' }).fill('jane');
  await checkElementWhenReady(page, 'input[name="pa2_sn"]', 'smith');
  await checkElementWhenReady(page, 'input[name="pa2b_mm"]', '02');
  await checkElementWhenReady(page, 'input[name="pa2b_dd"]', '02');
  await checkElementWhenReady(page, 'input[name="pa2b_yyyy"]', '1982');
  await checkElementWhenReady(page, 'input[name="pa2b_pl"]', 'Berlin');
  await checkElementWhenReady(page, 'input[name="pa2d_mm"]', '11');
  await checkElementWhenReady(page, 'input[name="pa2d_dd"]', '11');
  await checkElementWhenReady(page, 'input[name="pa2d_yyyy"]', '2070');
  await checkElementWhenReady(page, 'input[name="pa2d_pl"]', 'Rome');
  await checkElementWhenReady(page, 'input[name="pa2_occu"]', 'Doctor');

  // Set numbers and dropdowns for parents
  await page.locator('input[type="text"]').nth(2).fill('1'); // Number (M)
  await page.locator('select').nth(0).selectOption('Create');
  await page.locator('input[type="text"]').nth(9).fill('2'); // Number (F)
  await page.locator('select').nth(1).selectOption('Create');

  // Add children
  await page.getByText('Same sex couple').click();
  await page.getByText('child').nth(2).click();
  await page.locator('#ins_ch0_n').selectOption('2');
  await page.getByRole('button', { name: 'OK' }).nth(2).click();

  // Fill all child fields
  // 1st child
  await checkElementWhenReady(page, 'input[name="ch1_fn"]', 'johny');
  await checkElementWhenReady(page, 'input[name="ch1_sn"]', 'junior');
  await checkElementWhenReady(page, 'input[name="ch1b_mm"]', '03');
  await checkElementWhenReady(page, 'input[name="ch1b_dd"]', '03');
  await checkElementWhenReady(page, 'input[name="ch1b_yyyy"]', '2010');
  await checkElementWhenReady(page, 'input[name="ch1b_pl"]', 'Madrid');
  await checkElementWhenReady(page, 'input[name="ch1d_mm"]', '04');
  await checkElementWhenReady(page, 'input[name="ch1d_dd"]', '04');
  await checkElementWhenReady(page, 'input[name="ch1d_yyyy"]', '2080');
  await checkElementWhenReady(page, 'input[name="ch1d_pl"]', 'Lisbon');
  await checkElementWhenReady(page, 'input[name="ch1_occu"]', 'Student');
  await page.locator('#ch1_p_selct').selectOption('Create');
  await page.locator('#ch1_p_selct_sex').getByText('M').click();

  // 2nd child
  await checkElementWhenReady(page, 'input[name="ch2_fn"]', 'alice');
  await checkElementWhenReady(page, 'input[name="ch2_sn"]', 'junior');
  await checkElementWhenReady(page, 'input[name="ch2b_mm"]', '05');
  await checkElementWhenReady(page, 'input[name="ch2b_dd"]', '05');
  await checkElementWhenReady(page, 'input[name="ch2b_yyyy"]', '2012');
  await checkElementWhenReady(page, 'input[name="ch2b_pl"]', 'Vienna');
  await checkElementWhenReady(page, 'input[name="ch2d_mm"]', '06');
  await checkElementWhenReady(page, 'input[name="ch2d_dd"]', '06');
  await checkElementWhenReady(page, 'input[name="ch2d_yyyy"]', '2090');
  await checkElementWhenReady(page, 'input[name="ch2d_pl"]', 'Prague');
  await checkElementWhenReady(page, 'input[name="ch2_occu"]', 'Artist');
  await page.locator('#ch2_p_selct').selectOption('Create');
  await page.locator('#ch2_p_selct_sex').getByText('F').click();

  // 3rd child
  await checkElementWhenReady(page, 'input[name="ch3_fn"]', 'lisa');
  await checkElementWhenReady(page, 'input[name="ch3_sn"]', 'junior');
  await checkElementWhenReady(page, 'input[name="ch3b_mm"]', '07');
  await checkElementWhenReady(page, 'input[name="ch3b_dd"]', '07');
  await checkElementWhenReady(page, 'input[name="ch3b_yyyy"]', '2014');
  await checkElementWhenReady(page, 'input[name="ch3b_pl"]', 'Brussels');
  await checkElementWhenReady(page, 'input[name="ch3d_mm"]', '08');
  await checkElementWhenReady(page, 'input[name="ch3d_dd"]', '08');
  await checkElementWhenReady(page, 'input[name="ch3d_yyyy"]', '2100');
  await checkElementWhenReady(page, 'input[name="ch3d_pl"]', 'Amsterdam');
  await checkElementWhenReady(page, 'input[name="ch3_occu"]', 'Musician');
  await page.locator('#ch3_p_selct').selectOption('Create');
  await page.locator('#ch3_p_selct_sex').getByRole('radio', { name: 'F' }).check();

  // Submit
  await page.locator('#updfam div').filter({ hasText: 'Comment <HTML> <br/> <hr' }).getByLabel('Submit').click();
});