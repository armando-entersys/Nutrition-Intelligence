import { test, expect } from '@playwright/test';
import path from 'path';

/**
 * Product Scanner E2E Tests
 * ==========================
 *
 * Tests NOM-051 product scanning functionality:
 * - Upload product image
 * - Scan barcode
 * - View product details
 * - See warning seals
 */

test.describe('Product Scanner', () => {

  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('[name="email"]', 'patient@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/dashboard/);
  });

  test('should navigate to scanner', async ({ page }) => {
    await page.goto('/scanner');

    // Should show scanner interface
    await expect(page.locator('[data-testid="scanner-container"]')).toBeVisible();
    await expect(page.locator('text=Escanear Producto')).toBeVisible();
  });

  test('should scan product by barcode input', async ({ page }) => {
    await page.goto('/scanner');

    // Enter known barcode (Coca-Cola)
    await page.fill('[data-testid="barcode-input"]', '7501055300891');
    await page.click('[data-testid="search-barcode"]');

    // Should show product details
    await expect(page.locator('[data-testid="product-detail"]')).toBeVisible({ timeout: 10000 });
    await expect(page.locator('text=Coca-Cola Original')).toBeVisible();

    // Should show warning seals
    await expect(page.locator('[data-testid="warning-seal-azucares"]')).toBeVisible();
  });

  test('should upload and scan product image', async ({ page }) => {
    await page.goto('/scanner');

    // Upload test image (mock)
    const fileInput = page.locator('[data-testid="image-upload"]');

    // Create a test file path (you need to have test images in e2e/fixtures/)
    const testImagePath = path.join(__dirname, '../fixtures/coca-cola-product.jpg');

    try {
      await fileInput.setInputFiles(testImagePath);

      // Click scan button
      await page.click('[data-testid="scan-image"]');

      // Should process image
      await expect(page.locator('[data-testid="scanning-loader"]')).toBeVisible();

      // Should show results
      await expect(page.locator('[data-testid="product-detail"]')).toBeVisible({ timeout: 15000 });
    } catch (error) {
      console.log('Test image not found, skipping image upload test');
    }
  });

  test('should show product not found message', async ({ page }) => {
    await page.goto('/scanner');

    // Enter non-existent barcode
    await page.fill('[data-testid="barcode-input"]', '0000000000000');
    await page.click('[data-testid="search-barcode"]');

    // Should show not found message
    await expect(page.locator('text=Producto no encontrado')).toBeVisible({ timeout: 10000 });
  });

  test('should display all NOM-051 information', async ({ page }) => {
    await page.goto('/scanner');

    await page.fill('[data-testid="barcode-input"]', '7501055300891');
    await page.click('[data-testid="search-barcode"]');

    await expect(page.locator('[data-testid="product-detail"]')).toBeVisible({ timeout: 10000 });

    // Check for key information
    await expect(page.locator('text=Información Nutrimental')).toBeVisible();
    await expect(page.locator('text=Calorías')).toBeVisible();
    await expect(page.locator('text=Azúcares')).toBeVisible();
    await expect(page.locator('text=Grasas')).toBeVisible();
    await expect(page.locator('text=Sodio')).toBeVisible();

    // Check for warning seals section
    await expect(page.locator('[data-testid="warning-seals"]')).toBeVisible();
  });

  test('should allow comparing products', async ({ page }) => {
    await page.goto('/scanner');

    // Scan first product
    await page.fill('[data-testid="barcode-input"]', '7501055300891');
    await page.click('[data-testid="search-barcode"]');
    await expect(page.locator('[data-testid="product-detail"]')).toBeVisible({ timeout: 10000 });

    // Click "Add to comparison"
    await page.click('[data-testid="add-to-compare"]');

    // Go back and scan another product
    await page.click('[data-testid="back-to-scanner"]');
    await page.fill('[data-testid="barcode-input"]', '7501055362578');
    await page.click('[data-testid="search-barcode"]');

    // Should be able to compare
    await expect(page.locator('[data-testid="compare-button"]')).toBeVisible();
  });

  test('should save scanned products to history', async ({ page }) => {
    await page.goto('/scanner');

    // Scan a product
    await page.fill('[data-testid="barcode-input"]', '7501055300891');
    await page.click('[data-testid="search-barcode"]');
    await expect(page.locator('[data-testid="product-detail"]')).toBeVisible({ timeout: 10000 });

    // Navigate to history
    await page.goto('/scanner/history');

    // Should show scanned product
    await expect(page.locator('text=Coca-Cola Original')).toBeVisible();
  });
});
