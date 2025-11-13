import { test, expect } from '@playwright/test';

/**
 * AI Nutritionist Chat E2E Tests
 * ===============================
 *
 * Tests the AI chat functionality:
 * - Send messages
 * - Receive AI responses
 * - View chat history
 * - Ask nutrition questions
 */

test.describe('AI Nutritionist Chat', () => {

  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('[name="email"]', 'patient@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/dashboard/);
  });

  test('should open chat interface', async ({ page }) => {
    await page.goto('/chat');

    // Should show chat container
    await expect(page.locator('[data-testid="chat-container"]')).toBeVisible();
    await expect(page.locator('[data-testid="chat-input"]')).toBeVisible();

    // Should show welcome message
    await expect(page.locator('text=Hola, soy tu nutricionista virtual')).toBeVisible();
  });

  test('should send a message and receive response', async ({ page }) => {
    await page.goto('/chat');

    // Type a question
    const question = '¿Cuántas calorías tiene una manzana?';
    await page.fill('[data-testid="chat-input"]', question);

    // Send message
    await page.click('[data-testid="send-button"]');

    // Should show user message
    await expect(page.locator(`text=${question}`)).toBeVisible();

    // Should show typing indicator
    await expect(page.locator('[data-testid="typing-indicator"]')).toBeVisible();

    // Should receive AI response (timeout longer for AI)
    await expect(page.locator('[data-testid="ai-message"]').last()).toBeVisible({ timeout: 20000 });

    // Response should contain relevant information
    const lastMessage = page.locator('[data-testid="ai-message"]').last();
    await expect(lastMessage).toContainText(/calorías|energía|manzana/i);
  });

  test('should ask about nutrition recommendations', async ({ page }) => {
    await page.goto('/chat');

    await page.fill('[data-testid="chat-input"]', '¿Qué debo comer para ganar masa muscular?');
    await page.click('[data-testid="send-button"]');

    // Should get response with recommendations
    await expect(page.locator('[data-testid="ai-message"]').last()).toBeVisible({ timeout: 20000 });

    const response = page.locator('[data-testid="ai-message"]').last();
    await expect(response).toContainText(/proteína|músculo|ejercicio/i);
  });

  test('should ask about food alternatives', async ({ page }) => {
    await page.goto('/chat');

    await page.fill('[data-testid="chat-input"]', '¿Con qué puedo sustituir el azúcar?');
    await page.click('[data-testid="send-button"]');

    await expect(page.locator('[data-testid="ai-message"]').last()).toBeVisible({ timeout: 20000 });

    const response = page.locator('[data-testid="ai-message"]').last();
    await expect(response).toContainText(/stevia|miel|edulcorante/i);
  });

  test('should handle long conversations', async ({ page }) => {
    await page.goto('/chat');

    // Send multiple messages
    const questions = [
      '¿Qué es una dieta balanceada?',
      '¿Cuánta agua debo tomar al día?',
      '¿Es malo comer carbohidratos en la noche?'
    ];

    for (const question of questions) {
      await page.fill('[data-testid="chat-input"]', question);
      await page.click('[data-testid="send-button"]');

      // Wait for response
      await page.waitForTimeout(3000);
    }

    // Should show all messages in history
    const messages = page.locator('[data-testid="chat-message"]');
    expect(await messages.count()).toBeGreaterThanOrEqual(6); // 3 questions + 3 responses
  });

  test('should clear chat history', async ({ page }) => {
    await page.goto('/chat');

    // Send a message
    await page.fill('[data-testid="chat-input"]', '¿Hola?');
    await page.click('[data-testid="send-button"]');

    await page.waitForTimeout(2000);

    // Clear chat
    await page.click('[data-testid="clear-chat"]');

    // Confirm clear
    await page.click('[data-testid="confirm-clear"]');

    // Should only show welcome message
    const messages = page.locator('[data-testid="chat-message"]');
    expect(await messages.count()).toBeLessThanOrEqual(1);
  });

  test('should handle error when AI is unavailable', async ({ page }) => {
    // This test would need to mock API failure
    await page.goto('/chat');

    // Intercept API call to simulate error
    await page.route('**/api/v1/nutritionist-chat/send', route => {
      route.fulfill({
        status: 500,
        body: JSON.stringify({ error: 'Service unavailable' })
      });
    });

    await page.fill('[data-testid="chat-input"]', 'Test message');
    await page.click('[data-testid="send-button"]');

    // Should show error message
    await expect(page.locator('text=Error al enviar mensaje')).toBeVisible();
  });

  test('should not send empty messages', async ({ page }) => {
    await page.goto('/chat');

    // Try to send empty message
    await page.click('[data-testid="send-button"]');

    // Send button should be disabled or nothing happens
    const messagesBefore = await page.locator('[data-testid="chat-message"]').count();
    await page.waitForTimeout(1000);
    const messagesAfter = await page.locator('[data-testid="chat-message"]').count();

    expect(messagesBefore).toBe(messagesAfter);
  });

  test('should show suggested questions', async ({ page }) => {
    await page.goto('/chat');

    // Should show quick question buttons
    await expect(page.locator('[data-testid="suggested-questions"]')).toBeVisible();

    // Click a suggested question
    await page.click('[data-testid="suggested-question"]');

    // Should send that question
    await expect(page.locator('[data-testid="ai-message"]').last()).toBeVisible({ timeout: 20000 });
  });
});
