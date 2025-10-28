const { test, expect } = require('@playwright/test');

test.describe('Performance Tests', () => {
  test('should load homepage within acceptable time', async ({ page }) => {
    const startTime = Date.now();

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const loadTime = Date.now() - startTime;

    console.log(`Page load time: ${loadTime}ms`);

    // Page should load within 10 seconds
    expect(loadTime).toBeLessThan(10000);

    await page.screenshot({ path: 'test-results/performance-homepage.png' });
  });

  test('should have good Core Web Vitals', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Measure performance
    const performanceMetrics = await page.evaluate(() => {
      const navigation = performance.getEntriesByType('navigation')[0];
      return {
        domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
        loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
        domInteractive: navigation.domInteractive,
      };
    });

    console.log('Performance Metrics:', performanceMetrics);

    // DOM should be interactive quickly
    expect(performanceMetrics.domInteractive).toBeLessThan(5000);
  });

  test('should handle multiple concurrent requests', async ({ page }) => {
    const promises = [];

    // Make multiple requests concurrently
    for (let i = 0; i < 5; i++) {
      promises.push(
        page.evaluate(() =>
          fetch('http://localhost:8001/health').then(r => r.json())
        )
      );
    }

    await page.goto('/');

    const results = await Promise.all(promises);

    // All requests should succeed
    expect(results.length).toBe(5);
    results.forEach(result => {
      expect(result.status).toBe('healthy');
    });
  });

  test('should measure API response times', async ({ request }) => {
    const measurements = [];

    // Make 10 requests and measure response time
    for (let i = 0; i < 10; i++) {
      const startTime = Date.now();
      const response = await request.get('http://localhost:8001/health');
      const responseTime = Date.now() - startTime;

      expect(response.ok()).toBeTruthy();
      measurements.push(responseTime);
    }

    const avgResponseTime = measurements.reduce((a, b) => a + b, 0) / measurements.length;
    const maxResponseTime = Math.max(...measurements);

    console.log(`Average response time: ${avgResponseTime}ms`);
    console.log(`Max response time: ${maxResponseTime}ms`);

    // Average response time should be under 1 second
    expect(avgResponseTime).toBeLessThan(1000);
  });

  test('should check resource loading', async ({ page }) => {
    await page.goto('/');

    // Get all loaded resources
    const resources = await page.evaluate(() => {
      const entries = performance.getEntriesByType('resource');
      return entries.map(entry => ({
        name: entry.name,
        type: entry.initiatorType,
        duration: entry.duration,
        size: entry.transferSize
      }));
    });

    console.log(`Total resources loaded: ${resources.length}`);

    // Log slow resources
    const slowResources = resources.filter(r => r.duration > 1000);
    if (slowResources.length > 0) {
      console.log('Slow resources:', slowResources);
    }

    // Most resources should load quickly
    const fastResources = resources.filter(r => r.duration < 1000);
    expect(fastResources.length).toBeGreaterThan(0);
  });

  test('should measure memory usage', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Check if performance.memory is available
    const memoryInfo = await page.evaluate(() => {
      if (performance.memory) {
        return {
          usedJSHeapSize: performance.memory.usedJSHeapSize,
          totalJSHeapSize: performance.memory.totalJSHeapSize,
          jsHeapSizeLimit: performance.memory.jsHeapSizeLimit
        };
      }
      return null;
    });

    if (memoryInfo) {
      console.log('Memory Usage:', memoryInfo);

      // Memory usage should be reasonable (less than 100MB)
      const usedMemoryMB = memoryInfo.usedJSHeapSize / (1024 * 1024);
      console.log(`Used memory: ${usedMemoryMB.toFixed(2)} MB`);
    }
  });
});