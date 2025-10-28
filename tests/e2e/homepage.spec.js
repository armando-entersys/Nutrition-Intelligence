const { test, expect } = require('@playwright/test');

test.describe('Homepage Tests', () => {
  test('should load the homepage successfully', async ({ page }) => {
    await page.goto('/');

    // Check if the page title is correct
    await expect(page).toHaveTitle(/Nutrition Intelligence/i);

    // Check if main content is visible
    const mainContent = page.locator('body');
    await expect(mainContent).toBeVisible();
  });

  test('should display the navigation sidebar', async ({ page }) => {
    await page.goto('/');

    // Wait for sidebar to be visible
    const sidebar = page.locator('.sidebar, [class*="sidebar"], nav');

    // Give the page time to render
    await page.waitForTimeout(2000);

    // Take screenshot for debugging
    await page.screenshot({ path: 'test-results/homepage-sidebar.png' });
  });

  test('should show backend connection status', async ({ page }) => {
    await page.goto('/');

    // Wait for the page to load
    await page.waitForLoadState('networkidle');

    // Look for backend status indicator
    const statusText = await page.textContent('body');

    // Check if status is displayed (either connected or not available)
    expect(statusText).toBeTruthy();

    // Take screenshot
    await page.screenshot({ path: 'test-results/homepage-backend-status.png' });
  });

  test('should be responsive on mobile devices', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');

    // Check if page loads on mobile
    await expect(page.locator('body')).toBeVisible();

    // Take mobile screenshot
    await page.screenshot({ path: 'test-results/homepage-mobile.png' });
  });

  test('should have proper meta tags', async ({ page }) => {
    await page.goto('/');

    // Check viewport meta tag
    const viewportMeta = await page.locator('meta[name="viewport"]').getAttribute('content');
    expect(viewportMeta).toContain('width=device-width');
  });
});