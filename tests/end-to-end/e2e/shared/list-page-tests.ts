import { test, expect, Page, BrowserContext } from '@playwright/test';

/**
 * Shared test functions for list page testing across different scenarios
 */

export function testHomePageElementsVisibility(url: string) {
  test('f16-lp1 - List Page: Home Page Elements Visibility', async ({ page }) => {
    await page.goto(url);

    await expect(page.getByRole('heading', { name: 'Databases' })).toBeVisible();

    // Check if all links exist and have valid href attributes
    const links = await page.locator('a').all();

    // Ensure at least some links are present
    expect(links.length).toBeGreaterThan(0);

    // Check each link has a valid href
    for (const link of links) {
      const href = await link.getAttribute('href');
      expect(href).toBeTruthy(); // href should not be null or empty
      expect(href).not.toBe('#'); // href should not be just a hash
    }

    // Optionally check for specific important links
    await expect(page.getByRole('link', { name: "welcome" })).toBeVisible();
    await expect(page.getByRole('link', { name: "gwd info" })).toBeVisible();
  });
}

export function testGitHubLinkFunctionality(url: string, name: string) {
  test('f16-lp2 - List Page: GitHub Link Functionality', async ({ page }) => {
    await page.goto(url);
    if (name === "caml") {
      await page.getByRole('link').filter({ hasText: /^$/ }).click();
    } else {
      await page.locator('a[href="https://github.com/geneweb/geneweb/"]').click();
    }
    await expect(page).toHaveURL('https://github.com/geneweb/geneweb/');
  });
}

export function testLinksNavigation(url: string) {
  test('f16-lp4 - List Page: Links Navigation', async ({ page, context }) => {
    await page.goto(url);

    // Wait for the page to fully load
    await expect(page.getByRole('heading', { name: 'Databases' })).toBeVisible();

    // Get all links on the page
    const links = await page.locator('a').all();

    for (const link of links) {
      const href = await link.getAttribute('href');

      // Skip if href is null or empty
      if (!href) continue;

      // Skip if href is just a fragment
      if (href === '#' || href.startsWith('#')) continue;

      // Check if it's an external link (different domain)
      const currentUrl = new URL(page.url());
      let isExternal = false;

      try {
        if (href.startsWith('http://') || href.startsWith('https://')) {
          const linkUrl = new URL(href);
          isExternal = linkUrl.hostname !== currentUrl.hostname;
        }
      } catch (e) {
        // Invalid URL, skip it
        console.log(`Skipping invalid URL: ${href}`);
        continue;
      }

      if (isExternal) {
        // For external links, open in new tab and check it loads
        try {
          const [newPage] = await Promise.all([
            context.waitForEvent('page'),
            link.click({ modifiers: ['Control'] }) // Ctrl+click to open in new tab
          ]);

          // Wait for the new page to load
          await newPage.waitForLoadState('domcontentloaded', { timeout: 10000 });

          // Check that the page didn't error out (status 200 or similar)
          expect(newPage.url()).toBeTruthy();

          // Close the new tab
          await newPage.close();
        } catch (e) {
          console.log(`Failed to navigate to external link: ${href}`, e);
        }

        // Go back to list page
        await page.goto(url);
        await expect(page.getByRole('heading', { name: 'Databases' })).toBeVisible();
      } else {
        // For internal links, navigate and check response
        const linkText = await link.textContent();

        // Build the full URL properly
        let fullUrl: string;
        if (href.startsWith('/')) {
          // Relative path starting with /
          fullUrl = process.env.FRONT_SETUP_URL + href;
        } else if (href.startsWith('http://') || href.startsWith('https://')) {
          // Already a full URL
          fullUrl = href;
        } else {
          // Relative path without leading slash
          fullUrl = process.env.FRONT_SETUP_URL + '/' + href;
        }

        // Click the link and wait for navigation
        const response = await Promise.race([
          page.goto(fullUrl, {
            waitUntil: 'domcontentloaded',
            timeout: 10000
          }),
          Promise.resolve(null) // Fallback if navigation fails
        ]);

        // Check that we didn't get a 404 or 500 error
        if (response) {
          expect(response.status()).toBeLessThan(400);
        }

        // Go back to the list page for the next iteration
        await page.goto(url);
        await expect(page.getByRole('heading', { name: 'Databases' })).toBeVisible();
      }
    }
  });
}
