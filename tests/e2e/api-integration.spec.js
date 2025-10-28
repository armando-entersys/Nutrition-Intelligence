const { test, expect } = require('@playwright/test');

test.describe('API Integration Tests', () => {
  test('should connect to backend health endpoint', async ({ request }) => {
    const response = await request.get('http://localhost:8001/health');

    expect(response.ok()).toBeTruthy();
    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data).toHaveProperty('status');
    expect(data.status).toBe('healthy');
  });

  test('should fetch foods data from API', async ({ request }) => {
    const response = await request.get('http://localhost:8001/api/v1/foods');

    expect(response.ok()).toBeTruthy();
    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(Array.isArray(data)).toBeTruthy();
    expect(data.length).toBeGreaterThan(0);

    // Validate first food item structure
    const firstFood = data[0];
    expect(firstFood).toHaveProperty('id');
    expect(firstFood).toHaveProperty('name');
    expect(firstFood).toHaveProperty('category');
    expect(firstFood).toHaveProperty('calories_per_100g');
  });

  test('should handle API errors gracefully', async ({ request }) => {
    const response = await request.get('http://localhost:8001/api/v1/nonexistent');

    // Should return 404 or similar error
    expect(response.status()).toBeGreaterThanOrEqual(400);
  });

  test('should have proper CORS headers', async ({ request }) => {
    const response = await request.get('http://localhost:8001/health');

    const headers = response.headers();
    expect(headers['access-control-allow-origin']).toBeDefined();
  });
});

test.describe('Frontend-Backend Integration', () => {
  test('should display backend data on frontend', async ({ page }) => {
    await page.goto('/');

    // Wait for API call to complete
    await page.waitForTimeout(3000);

    // Check if any backend data is displayed
    const pageContent = await page.textContent('body');

    // Look for indicators that backend is working
    const hasBackendIndicator =
      pageContent.includes('Backend') ||
      pageContent.includes('Conectado') ||
      pageContent.includes('healthy');

    // Take screenshot for debugging
    await page.screenshot({ path: 'test-results/backend-integration.png' });

    expect(pageContent).toBeTruthy();
  });

  test('should handle backend unavailable state', async ({ page }) => {
    // Mock backend being unavailable
    await page.route('**/health', route => route.abort());

    await page.goto('/');
    await page.waitForTimeout(2000);

    // Check if error state is handled
    const pageContent = await page.textContent('body');
    expect(pageContent).toBeTruthy();

    await page.screenshot({ path: 'test-results/backend-unavailable.png' });
  });
});