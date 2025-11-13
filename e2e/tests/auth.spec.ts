import { test, expect } from '@playwright/test';

/**
 * Authentication E2E Tests
 * =========================
 *
 * Tests the complete authentication flow:
 * - User registration
 * - Login
 * - Logout
 * - Password reset
 */

test.describe('Authentication Flow', () => {

  test('should allow user to register', async ({ page }) => {
    await page.goto('/register');

    // Fill registration form
    await page.fill('[name="firstName"]', 'Juan');
    await page.fill('[name="lastName"]', 'Pérez');
    await page.fill('[name="email"]', `test${Date.now()}@example.com`);
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.fill('[name="confirmPassword"]', 'SecurePass123!');

    // Select role
    await page.click('[data-testid="role-patient"]');

    // Submit form
    await page.click('button[type="submit"]');

    // Should redirect to dashboard
    await expect(page).toHaveURL(/\/dashboard/);

    // Should show welcome message
    await expect(page.locator('text=Bienvenido')).toBeVisible();
  });

  test('should allow user to login', async ({ page }) => {
    await page.goto('/login');

    // Fill login form
    await page.fill('[name="email"]', 'patient@example.com');
    await page.fill('[name="password"]', 'password123');

    // Submit
    await page.click('button[type="submit"]');

    // Should redirect to dashboard
    await expect(page).toHaveURL(/\/dashboard/);

    // Should show user menu
    await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
  });

  test('should show error on invalid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[name="email"]', 'wrong@example.com');
    await page.fill('[name="password"]', 'wrongpassword');

    await page.click('button[type="submit"]');

    // Should show error message
    await expect(page.locator('text=Credenciales inválidas')).toBeVisible();

    // Should stay on login page
    await expect(page).toHaveURL('/login');
  });

  test('should allow user to logout', async ({ page }) => {
    // Login first
    await page.goto('/login');
    await page.fill('[name="email"]', 'patient@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/\/dashboard/);

    // Logout
    await page.click('[data-testid="user-menu"]');
    await page.click('[data-testid="logout-button"]');

    // Should redirect to home or login
    await expect(page).toHaveURL(/\/(login)?$/);
  });

  test('should handle password reset flow', async ({ page }) => {
    await page.goto('/forgot-password');

    await page.fill('[name="email"]', 'patient@example.com');
    await page.click('button[type="submit"]');

    // Should show success message
    await expect(page.locator('text=correo enviado')).toBeVisible();
  });

  test('should validate form fields', async ({ page }) => {
    await page.goto('/register');

    // Try to submit empty form
    await page.click('button[type="submit"]');

    // Should show validation errors
    await expect(page.locator('text=campo requerido')).toHaveCount(5); // firstName, lastName, email, password, confirmPassword
  });

  test('should validate password strength', async ({ page }) => {
    await page.goto('/register');

    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'weak');

    // Should show weak password message
    await expect(page.locator('text=contraseña debe tener al menos 8 caracteres')).toBeVisible();
  });
});
