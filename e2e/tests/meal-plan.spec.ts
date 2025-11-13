import { test, expect } from '@playwright/test';

/**
 * Meal Plan E2E Tests
 * ====================
 *
 * Tests meal plan creation and management:
 * - Create meal plan
 * - Add foods to meal plan
 * - Edit meal plan
 * - View nutrition summary
 */

test.describe('Meal Plan Management', () => {

  test.beforeEach(async ({ page }) => {
    // Login as patient
    await page.goto('/login');
    await page.fill('[name="email"]', 'patient@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/dashboard/);
  });

  test('should create new meal plan', async ({ page }) => {
    await page.goto('/meal-plans');

    // Click create new plan
    await page.click('[data-testid="create-meal-plan"]');

    // Fill form
    await page.fill('[name="planName"]', 'Mi Plan Semanal');
    await page.selectOption('[name="duration"]', '7'); // 7 days
    await page.fill('[name="caloriesGoal"]', '2000');

    // Submit
    await page.click('[data-testid="save-meal-plan"]');

    // Should show success and redirect
    await expect(page.locator('text=Plan creado exitosamente')).toBeVisible();
    await expect(page).toHaveURL(/\/meal-plans\/\d+/);
  });

  test('should add breakfast to meal plan', async ({ page }) => {
    // Assuming meal plan exists
    await page.goto('/meal-plans/1');

    // Click add breakfast for day 1
    await page.click('[data-testid="add-breakfast-day-1"]');

    // Search for food
    await page.fill('[data-testid="food-search"]', 'huevo');
    await page.press('[data-testid="food-search"]', 'Enter');

    // Select first result
    await page.click('[data-testid="food-result"]');

    // Set portion
    await page.fill('[data-testid="portion-input"]', '2');

    // Add to meal
    await page.click('[data-testid="add-to-meal"]');

    // Should show in breakfast section
    await expect(page.locator('[data-testid="breakfast-day-1"] text=huevo')).toBeVisible();
  });

  test('should view nutrition summary', async ({ page }) => {
    await page.goto('/meal-plans/1');

    // Should show nutrition dashboard
    await expect(page.locator('[data-testid="nutrition-summary"]')).toBeVisible();

    // Should show macros
    await expect(page.locator('text=Calorías totales')).toBeVisible();
    await expect(page.locator('text=Proteínas')).toBeVisible();
    await expect(page.locator('text=Carbohidratos')).toBeVisible();
    await expect(page.locator('text=Grasas')).toBeVisible();

    // Should show charts
    await expect(page.locator('[data-testid="macros-chart"]')).toBeVisible();
  });

  test('should edit meal in plan', async ({ page }) => {
    await page.goto('/meal-plans/1');

    // Click edit on existing meal
    await page.click('[data-testid="edit-breakfast-day-1"]');

    // Change portion
    await page.fill('[data-testid="portion-input"]', '3');

    // Save changes
    await page.click('[data-testid="save-changes"]');

    // Should update nutrition summary
    await page.waitForTimeout(1000);

    // Verify changes reflected
    await expect(page.locator('[data-testid="nutrition-summary"]')).toBeVisible();
  });

  test('should remove food from meal', async ({ page }) => {
    await page.goto('/meal-plans/1');

    // Click remove on food item
    await page.click('[data-testid="remove-food-item"]');

    // Confirm removal
    await page.click('[data-testid="confirm-remove"]');

    // Should be removed from list
    await expect(page.locator('text=Alimento eliminado')).toBeVisible();
  });

  test('should copy day to another day', async ({ page }) => {
    await page.goto('/meal-plans/1');

    // Click copy day 1
    await page.click('[data-testid="copy-day-1"]');

    // Select target day
    await page.selectOption('[data-testid="target-day"]', '2');

    // Confirm copy
    await page.click('[data-testid="confirm-copy"]');

    // Day 2 should have same meals as day 1
    const day1Meals = await page.locator('[data-testid="meals-day-1"]').textContent();
    const day2Meals = await page.locator('[data-testid="meals-day-2"]').textContent();

    expect(day1Meals).toBe(day2Meals);
  });

  test('should export meal plan to PDF', async ({ page }) => {
    await page.goto('/meal-plans/1');

    // Click export button
    const [download] = await Promise.all([
      page.waitForEvent('download'),
      page.click('[data-testid="export-pdf"]')
    ]);

    // Verify download
    expect(download.suggestedFilename()).toContain('.pdf');
  });

  test('should share meal plan with nutritionist', async ({ page }) => {
    await page.goto('/meal-plans/1');

    // Click share button
    await page.click('[data-testid="share-plan"]');

    // Select nutritionist
    await page.selectOption('[data-testid="nutritionist-select"]', '1');

    // Add message
    await page.fill('[data-testid="share-message"]', 'Por favor revisa mi plan');

    // Send
    await page.click('[data-testid="send-share"]');

    // Should show confirmation
    await expect(page.locator('text=Plan compartido exitosamente')).toBeVisible();
  });

  test('should handle empty meal plan', async ({ page }) => {
    await page.goto('/meal-plans');

    // Create new empty plan
    await page.click('[data-testid="create-meal-plan"]');
    await page.fill('[name="planName"]', 'Plan Vacío');
    await page.selectOption('[name="duration"]', '3');
    await page.click('[data-testid="save-meal-plan"]');

    // Should show empty state
    await expect(page.locator('text=Agrega alimentos para comenzar')).toBeVisible();
  });
});
