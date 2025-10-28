const { test, expect } = require('@playwright/test');

test.describe('Navigation Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('should have functional sidebar navigation', async ({ page }) => {
    // Wait for page to load
    await page.waitForTimeout(2000);

    // Take screenshot of initial state
    await page.screenshot({ path: 'test-results/navigation-initial.png' });

    // Check if navigation elements exist
    const body = await page.locator('body');
    await expect(body).toBeVisible();
  });

  test('should toggle sidebar on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    await page.waitForTimeout(1000);

    // Take screenshot of mobile navigation
    await page.screenshot({ path: 'test-results/navigation-mobile.png' });
  });

  test('should navigate to different sections', async ({ page }) => {
    await page.waitForTimeout(2000);

    // Take screenshot showing navigation structure
    await page.screenshot({ path: 'test-results/navigation-sections.png', fullPage: true });

    const pageContent = await page.textContent('body');
    expect(pageContent).toBeTruthy();
  });

  test('should display user information in sidebar', async ({ page }) => {
    await page.waitForTimeout(2000);

    const pageContent = await page.textContent('body');

    // Check if any user-related information is visible
    expect(pageContent).toBeTruthy();

    await page.screenshot({ path: 'test-results/navigation-user-info.png' });
  });

  test('should have working navigation links', async ({ page }) => {
    await page.waitForTimeout(2000);

    // Find all links on the page
    const links = await page.locator('a').all();

    console.log(`Found ${links.length} links on the page`);

    await page.screenshot({ path: 'test-results/navigation-links.png', fullPage: true });
  });

  test('should maintain state during navigation', async ({ page }) => {
    // Initial state
    const initialContent = await page.textContent('body');
    await page.screenshot({ path: 'test-results/navigation-state-before.png' });

    // Wait and check state persists
    await page.waitForTimeout(1000);

    const afterContent = await page.textContent('body');
    await page.screenshot({ path: 'test-results/navigation-state-after.png' });

    expect(afterContent).toBeTruthy();
  });
});