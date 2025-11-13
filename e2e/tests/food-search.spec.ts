import { test, expect } from '@playwright/test';

/**
 * Food Search E2E Tests
 * ======================
 *
 * Tests food and recipe search functionality:
 * - Search foods by name
 * - Filter by categories
 * - View food details
 * - Add to meal plan
 */

test.describe('Food Search', () => {

  test.beforeEach(async ({ page }) => {
    // Login as patient
    await page.goto('/login');
    await page.fill('[name="email"]', 'patient@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/dashboard/);
  });

  test('should search for foods', async ({ page }) => {
    await page.goto('/foods');

    // Search for "pollo"
    await page.fill('[data-testid="search-input"]', 'pollo');
    await page.press('[data-testid="search-input"]', 'Enter');

    // Should show results
    await expect(page.locator('[data-testid="food-card"]')).toHaveCount(3, { timeout: 10000 });

    // Results should contain "pollo"
    const firstResult = page.locator('[data-testid="food-card"]').first();
    await expect(firstResult).toContainText(/pollo/i);
  });

  test('should filter foods by SMAE group', async ({ page }) => {
    await page.goto('/foods');

    // Select "Frutas" filter
    await page.click('[data-testid="filter-frutas"]');

    // Should show only fruits
    await page.waitForTimeout(1000); // Wait for filter to apply

    const foodCards = page.locator('[data-testid="food-card"]');
    const count = await foodCards.count();

    expect(count).toBeGreaterThan(0);

    // All results should be fruits
    for (let i = 0; i < Math.min(count, 5); i++) {
      const card = foodCards.nth(i);
      await expect(card).toContainText(/Frutas/i);
    }
  });

  test('should view food details', async ({ page }) => {
    await page.goto('/foods');

    // Click first food card
    await page.click('[data-testid="food-card"]');

    // Should open detail modal or page
    await expect(page.locator('[data-testid="food-detail"]')).toBeVisible();

    // Should show nutrition information
    await expect(page.locator('text=Calorías')).toBeVisible();
    await expect(page.locator('text=Proteínas')).toBeVisible();
    await expect(page.locator('text=Carbohidratos')).toBeVisible();
  });

  test('should search with no results', async ({ page }) => {
    await page.goto('/foods');

    await page.fill('[data-testid="search-input"]', 'xyznonexistent123');
    await page.press('[data-testid="search-input"]', 'Enter');

    // Should show "no results" message
    await expect(page.locator('text=No se encontraron resultados')).toBeVisible();
  });

  test('should paginate results', async ({ page }) => {
    await page.goto('/foods');

    // Should show pagination if more than 10 results
    const pagination = page.locator('[data-testid="pagination"]');

    if (await pagination.isVisible()) {
      // Click next page
      await page.click('[data-testid="next-page"]');

      // URL should update with page parameter
      await expect(page).toHaveURL(/page=2/);

      // Should show different results
      await expect(page.locator('[data-testid="food-card"]')).toHaveCount(10, { timeout: 10000 });
    }
  });

  test('should add food to meal plan', async ({ page }) => {
    await page.goto('/foods');

    // Open first food detail
    await page.click('[data-testid="food-card"]');

    // Click "Add to meal plan"
    await page.click('[data-testid="add-to-meal-plan"]');

    // Should show success message
    await expect(page.locator('text=agregado al plan')).toBeVisible({ timeout: 5000 });
  });
});

test.describe('Recipe Search', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'patient@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
  });

  test('should search for recipes', async ({ page }) => {
    await page.goto('/recipes');

    await page.fill('[data-testid="search-input"]', 'ensalada');
    await page.press('[data-testid="search-input"]', 'Enter');

    // Should show recipe results
    await expect(page.locator('[data-testid="recipe-card"]')).toHaveCount(2, { timeout: 10000 });
  });

  test('should view recipe details', async ({ page }) => {
    await page.goto('/recipes');

    await page.click('[data-testid="recipe-card"]');

    // Should show recipe details
    await expect(page.locator('[data-testid="recipe-detail"]')).toBeVisible();
    await expect(page.locator('text=Ingredientes')).toBeVisible();
    await expect(page.locator('text=Preparación')).toBeVisible();
  });

  test('should filter recipes by category', async ({ page }) => {
    await page.goto('/recipes');

    await page.click('[data-testid="filter-desayuno"]');

    await page.waitForTimeout(1000);

    const recipeCards = page.locator('[data-testid="recipe-card"]');
    expect(await recipeCards.count()).toBeGreaterThan(0);
  });
});
