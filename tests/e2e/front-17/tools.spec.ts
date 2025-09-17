import { test, expect } from '@playwright/test';

const urlBase = 'http://localhost:2317/chromatophilic?lang=en';

test('f17-af1 - Add Family: Create a new family', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('button', { name: 'Add family' }).click();
  // Fill all parent fields
  await page.getByRole('textbox', { name: 'First name (M)' }).fill('john');
  await page.getByRole('textbox', { name: 'Surname' }).nth(0).fill('doe');
  await page.locator('input[name="pa1b_mm"]').fill('01');
  await page.locator('input[name="pa1b_dd"]').fill('01');
  await page.locator('input[name="pa1b_yyyy"]').fill('1980');
  await page.locator('input[name="pa1b_pl"]').fill('Paris');
  await page.locator('input[name="pa1d_mm"]').fill('12');
  await page.locator('input[name="pa1d_dd"]').fill('12');
  await page.locator('input[name="pa1d_yyyy"]').fill('2050');
  await page.locator('input[name="pa1d_pl"]').fill('London');
  await page.locator('input[name="pa1_occu"]').fill('Engineer');
  await page.getByRole('textbox', { name: 'First name (F)' }).fill('jane');
  await page.locator('input[name="pa2_sn"]').fill('smith');
  await page.locator('input[name="pa2b_mm"]').fill('02');
  await page.locator('input[name="pa2b_dd"]').fill('02');
  await page.locator('input[name="pa2b_yyyy"]').fill('1982');
  await page.locator('input[name="pa2b_pl"]').fill('Berlin');
  await page.locator('input[name="pa2d_mm"]').fill('11');
  await page.locator('input[name="pa2d_dd"]').fill('11');
  await page.locator('input[name="pa2d_yyyy"]').fill('2070');
  await page.locator('input[name="pa2d_pl"]').fill('Rome');
  await page.locator('input[name="pa2_occu"]').fill('Doctor');
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
  await page.locator('input[name="ch1_fn"]').fill('johny');
  await page.locator('input[name="ch1_sn"]').fill('junior');
  await page.locator('input[name="ch1b_mm"]').fill('03');
  await page.locator('input[name="ch1b_dd"]').fill('03');
  await page.locator('input[name="ch1b_yyyy"]').fill('2010');
  await page.locator('input[name="ch1b_pl"]').fill('Madrid');
  await page.locator('input[name="ch1d_mm"]').fill('04');
  await page.locator('input[name="ch1d_dd"]').fill('04');
  await page.locator('input[name="ch1d_yyyy"]').fill('2080');
  await page.locator('input[name="ch1d_pl"]').fill('Lisbon');
  await page.locator('input[name="ch1_occu"]').fill('Student');
  await page.locator('#ch1_p_selct').selectOption('Create');
  await page.locator('#ch1_p_selct_sex').getByText('M').click();
  // 2nd child
  await page.locator('input[name="ch2_fn"]').fill('alice');
  await page.locator('input[name="ch2_sn"]').fill('junior');
  await page.locator('input[name="ch2b_mm"]').fill('05');
  await page.locator('input[name="ch2b_dd"]').fill('05');
  await page.locator('input[name="ch2b_yyyy"]').fill('2012');
  await page.locator('input[name="ch2b_pl"]').fill('Vienna');
  await page.locator('input[name="ch2d_mm"]').fill('06');
  await page.locator('input[name="ch2d_dd"]').fill('06');
  await page.locator('input[name="ch2d_yyyy"]').fill('2090');
  await page.locator('input[name="ch2d_pl"]').fill('Prague');
  await page.locator('input[name="ch2_occu"]').fill('Artist');
  await page.locator('#ch2_p_selct').selectOption('Create');
  await page.locator('#ch2_p_selct_sex').getByText('F').click();
  // 3rd child
  await page.locator('input[name="ch3_fn"]').fill('lisa');
  await page.locator('input[name="ch3_sn"]').fill('junior');
  await page.locator('input[name="ch3b_mm"]').fill('07');
  await page.locator('input[name="ch3b_dd"]').fill('07');
  await page.locator('input[name="ch3b_yyyy"]').fill('2014');
  await page.locator('input[name="ch3b_pl"]').fill('Brussels');
  await page.locator('input[name="ch3d_mm"]').fill('08');
  await page.locator('input[name="ch3d_dd"]').fill('08');
  await page.locator('input[name="ch3d_yyyy"]').fill('2100');
  await page.locator('input[name="ch3d_pl"]').fill('Amsterdam');
  await page.locator('input[name="ch3_occu"]').fill('Musician');
  await page.locator('#ch3_p_selct').selectOption('Create');
  await page.locator('#ch3_p_selct_sex').getByRole('radio', { name: 'F' }).check();
  // Submit
  await page.locator('#updfam div').filter({ hasText: 'Comment <HTML> <br/> <hr' }).getByLabel('Submit').click();
});

test('f17-co1 - Configuration: Check configuration', async ({ page }) => {
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

test('f17-ca1 - Calendars: Check calendar', async ({ page }) => {
  await page.goto(urlBase);
  await page.getByRole('button', { name: 'Calendars' }).click();
  await expect(page.locator('tbody')).toContainText('Gregorian');
  await expect(page.locator('select[name="mg"]')).toHaveValue('9');
  await expect(page.locator('input[name="dg"]')).toHaveValue('17');
  await expect(page.locator('input[name="yg"]')).toHaveValue('2025');
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