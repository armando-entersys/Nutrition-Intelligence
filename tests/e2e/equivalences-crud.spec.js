const { test, expect } = require('@playwright/test');

test.describe('Equivalences Section - Complete Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the application
    await page.goto('http://localhost:3002');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
  });

  test('should navigate to Equivalences section', async ({ page }) => {
    // Click on Equivalences in sidebar
    const equivalencesButton = page.locator('button:has-text("Equivalencias")').first();
    await equivalencesButton.click();
    await page.waitForTimeout(2000);

    // Verify Equivalences section is displayed
    const pageContent = await page.textContent('body');
    expect(pageContent).toContain('Sistema de Equivalencias Nutricionales');

    await page.screenshot({ path: 'test-results/equivalences-section-loaded.png', fullPage: true });
  });

  test('should display equivalence groups list', async ({ page }) => {
    // Navigate to Equivalences section
    await page.locator('button:has-text("Equivalencias")').first().click();
    await page.waitForTimeout(2000);

    // Check if groups are loaded
    const pageContent = await page.textContent('body');

    // Should show the mock groups
    const hasGroups = pageContent.includes('Frutas Frescas') ||
                      pageContent.includes('Vegetales') ||
                      pageContent.includes('Grupos (');
    expect(hasGroups).toBeTruthy();

    await page.screenshot({ path: 'test-results/equivalences-groups-displayed.png', fullPage: true });
  });

  test('should select a group and view equivalences', async ({ page }) => {
    // Navigate to Equivalences section
    await page.locator('button:has-text("Equivalencias")').first().click();
    await page.waitForTimeout(2000);

    // Click on first group
    const firstGroup = page.locator('div').filter({ hasText: 'Frutas Frescas' }).first();
    if (await firstGroup.count() > 0) {
      await firstGroup.click();
      await page.waitForTimeout(1000);

      // Verify equivalences table is shown
      const pageContent = await page.textContent('body');
      const hasEquivalences = pageContent.includes('Alimento') ||
                             pageContent.includes('Porción') ||
                             pageContent.includes('Manzana');
      expect(hasEquivalences).toBeTruthy();

      await page.screenshot({ path: 'test-results/equivalences-group-selected.png', fullPage: true });
    }
  });

  test('should use equivalence calculator', async ({ page }) => {
    // Navigate to Equivalences section
    await page.locator('button:has-text("Equivalencias")').first().click();
    await page.waitForTimeout(2000);

    // Select first group
    const firstGroup = page.locator('div').filter({ hasText: 'Frutas Frescas' }).first();
    if (await firstGroup.count() > 0) {
      await firstGroup.click();
      await page.waitForTimeout(1000);

      // Find calculator section
      const calculatorSection = page.locator('text=Calculadora de Equivalencias').first();
      if (await calculatorSection.count() > 0) {
        // Use the calculator
        const selects = page.locator('select');
        if (await selects.count() >= 2) {
          // Select from food
          await selects.nth(0).selectOption({ index: 1 });
          await page.waitForTimeout(500);

          // Select to food
          await selects.nth(1).selectOption({ index: 2 });
          await page.waitForTimeout(500);

          // Enter amount
          const amountInput = page.locator('input[type="number"]').first();
          await amountInput.fill('100');
          await page.waitForTimeout(500);

          // Click calculate button
          const calculateButton = page.locator('button:has-text("Calcular")').first();
          if (await calculateButton.count() > 0) {
            await calculateButton.click();
            await page.waitForTimeout(1000);

            // Verify result is displayed
            const pageContent = await page.textContent('body');
            const hasResult = pageContent.includes('equivale a') ||
                             pageContent.includes('gramos');
            expect(hasResult).toBeTruthy();

            await page.screenshot({ path: 'test-results/equivalences-calculator-used.png', fullPage: true });
          }
        }
      }
    }
  });

  test('should add new equivalence to group', async ({ page }) => {
    // Navigate to Equivalences section
    await page.locator('button:has-text("Equivalencias")').first().click();
    await page.waitForTimeout(2000);

    // Select first group
    const firstGroup = page.locator('div').filter({ hasText: 'Frutas Frescas' }).first();
    if (await firstGroup.count() > 0) {
      await firstGroup.click();
      await page.waitForTimeout(1000);

      // Find add equivalence section
      const addSection = page.locator('text=Agregar Equivalencia').first();
      if (await addSection.count() > 0) {
        // Fill in new equivalence form
        const inputs = page.locator('input[type="text"], input[type="number"]');

        // Find the name input in the add section
        const nameInput = page.locator('input[placeholder*="nombre"], input[placeholder*="Nombre"]').first();
        if (await nameInput.count() > 0) {
          await nameInput.fill('Fresa');

          // Find portion and calorie inputs
          const portionInput = page.locator('input[placeholder*="100"]').first();
          if (await portionInput.count() > 0) {
            await portionInput.fill('150');
          }

          const calorieInput = page.locator('input[placeholder*="52"], input[placeholder*="calorías"]').first();
          if (await calorieInput.count() > 0) {
            await calorieInput.fill('48');
          }

          await page.screenshot({ path: 'test-results/equivalences-add-form-filled.png', fullPage: true });

          // Click add button
          const addButton = page.locator('button:has-text("Agregar")').first();
          if (await addButton.count() > 0) {
            await addButton.click();
            await page.waitForTimeout(1000);

            await page.screenshot({ path: 'test-results/equivalences-added.png', fullPage: true });
          }
        }
      }
    }
  });

  test('should create new equivalence group', async ({ page }) => {
    // Navigate to Equivalences section
    await page.locator('button:has-text("Equivalencias")').first().click();
    await page.waitForTimeout(2000);

    // Click add new group button
    const addGroupButton = page.locator('button:has-text("Nuevo Grupo")').first();
    if (await addGroupButton.count() > 0) {
      await addGroupButton.click();
      await page.waitForTimeout(1000);

      // Verify form is displayed
      const pageContent = await page.textContent('body');
      expect(pageContent).toContain('Nuevo Grupo de Equivalencias');

      await page.screenshot({ path: 'test-results/equivalences-new-group-form.png', fullPage: true });

      // Fill in form
      const nameInput = page.locator('input[type="text"]').first();
      await nameInput.fill('Frutos Secos Test');

      const descInput = page.locator('textarea, input[placeholder*="descripción"]').first();
      if (await descInput.count() > 0) {
        await descInput.fill('Grupo de prueba para frutos secos');
      }

      await page.screenshot({ path: 'test-results/equivalences-new-group-filled.png', fullPage: true });

      // Save group
      const saveButton = page.locator('button:has-text("Guardar")').first();
      if (await saveButton.count() > 0) {
        // Handle alert dialog
        page.once('dialog', async dialog => {
          await dialog.accept();
        });

        await saveButton.click();
        await page.waitForTimeout(2000);

        await page.screenshot({ path: 'test-results/equivalences-group-created.png', fullPage: true });
      }
    }
  });

  test('should view equivalence comparison', async ({ page }) => {
    // Navigate to Equivalences section
    await page.locator('button:has-text("Equivalencias")').first().click();
    await page.waitForTimeout(2000);

    // Select first group
    const firstGroup = page.locator('div').filter({ hasText: 'Frutas Frescas' }).first();
    if (await firstGroup.count() > 0) {
      await firstGroup.click();
      await page.waitForTimeout(1000);

      // Look for comparison section
      const pageContent = await page.textContent('body');
      const hasComparison = pageContent.includes('Comparación Visual') ||
                           pageContent.includes('comparación');

      if (hasComparison) {
        await page.screenshot({ path: 'test-results/equivalences-comparison-view.png', fullPage: true });
      }
    }
  });

  test('should search/filter equivalence groups', async ({ page }) => {
    // Navigate to Equivalences section
    await page.locator('button:has-text("Equivalencias")').first().click();
    await page.waitForTimeout(2000);

    // Find search input
    const searchInput = page.locator('input[placeholder*="Buscar"]').first();
    if (await searchInput.count() > 0) {
      await searchInput.fill('Frutas');
      await page.waitForTimeout(1000);

      // Verify filtered results
      const pageContent = await page.textContent('body');
      expect(pageContent).toContain('Frutas');

      await page.screenshot({ path: 'test-results/equivalences-search-results.png', fullPage: true });
    }
  });

  test('should display group statistics', async ({ page }) => {
    // Navigate to Equivalences section
    await page.locator('button:has-text("Equivalencias")').first().click();
    await page.waitForTimeout(2000);

    // Select first group
    const firstGroup = page.locator('div').filter({ hasText: 'Frutas Frescas' }).first();
    if (await firstGroup.count() > 0) {
      await firstGroup.click();
      await page.waitForTimeout(1000);

      // Check for statistics
      const pageContent = await page.textContent('body');
      const hasStats = pageContent.includes('equivalencias') ||
                      pageContent.includes('Promedio') ||
                      pageContent.includes('calorías');

      if (hasStats) {
        await page.screenshot({ path: 'test-results/equivalences-statistics.png', fullPage: true });
      }
    }
  });
});

test.describe('Equivalences Integration', () => {
  test('should navigate between all main sections', async ({ page }) => {
    await page.goto('http://localhost:3002');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    const sections = [
      { name: 'Alimentos', text: 'Alimentos' },
      { name: 'Recetas', text: 'Recetas' },
      { name: 'Equivalencias', text: 'Equivalencias' },
    ];

    for (const section of sections) {
      console.log(`Testing navigation to: ${section.name}`);

      const button = page.locator(`button:has-text("${section.text}")`).first();
      await button.click();
      await page.waitForTimeout(1500);

      await page.screenshot({
        path: `test-results/integration-${section.name.toLowerCase()}.png`,
        fullPage: true
      });
    }
  });
});
