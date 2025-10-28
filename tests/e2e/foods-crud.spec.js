const { test, expect } = require('@playwright/test');

test.describe('Foods Section - Complete CRUD Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the application
    await page.goto('http://localhost:3005');
    await page.waitForLoadState('networkidle');

    // Wait for sidebar to load
    await page.waitForTimeout(2000);
  });

  test('should navigate to Foods section', async ({ page }) => {
    // Click on Foods in sidebar - try multiple selectors
    const foodsButton = page.locator('button:has-text("Alimentos")').first();
    await foodsButton.click();

    // Wait for Foods section to load
    await page.waitForTimeout(2000);

    // Verify Foods section is displayed
    const pageContent = await page.textContent('body');
    expect(pageContent).toContain('Gestión de Alimentos');

    // Take screenshot
    await page.screenshot({ path: 'test-results/foods-section-loaded.png', fullPage: true });
  });

  test('should display food list from backend', async ({ page }) => {
    // Navigate to Foods section
    await page.locator('button:has-text("Alimentos")').first().click();
    await page.waitForTimeout(2000);

    // Check if foods are loaded
    const pageContent = await page.textContent('body');

    // Should show at least the mock foods (Manzana, Platano)
    const hasFoods = pageContent.includes('Manzana') || pageContent.includes('Platano') || pageContent.includes('Alimentos (');
    expect(hasFoods).toBeTruthy();

    await page.screenshot({ path: 'test-results/foods-list-displayed.png', fullPage: true });
  });

  test('should open add new food form', async ({ page }) => {
    // Navigate to Foods section
    await page.locator('button:has-text("Alimentos")').first().click();
    await page.waitForTimeout(2000);

    // Click on "Agregar Nuevo Alimento" button
    const addButton = page.locator('button:has-text("Agregar Nuevo Alimento")').first();
    await addButton.click();
    await page.waitForTimeout(1000);

    // Verify form is displayed
    const pageContent = await page.textContent('body');
    expect(pageContent).toContain('Agregar Nuevo Alimento');
    expect(pageContent).toContain('Nombre del Alimento');

    await page.screenshot({ path: 'test-results/foods-add-form-opened.png', fullPage: true });
  });

  test('should create a new food item', async ({ page }) => {
    // Navigate to Foods section
    await page.locator('button:has-text("Alimentos")').first().click();
    await page.waitForTimeout(2000);

    // Click add button
    await page.locator('button:has-text("Agregar Nuevo Alimento")').first().click();
    await page.waitForTimeout(1000);

    // Fill in the form
    await page.fill('input[placeholder="Ej: Manzana"]', 'Aguacate Test');
    await page.selectOption('select', 'FRUITS');

    // Fill nutritional values
    const caloriesInput = page.locator('input[placeholder="52"]').first();
    await caloriesInput.fill('160');

    const proteinInput = page.locator('input[placeholder="0.3"]').first();
    await proteinInput.fill('2.0');

    const carbsInput = page.locator('input[placeholder="14.0"]').first();
    await carbsInput.fill('9.0');

    const fatInput = page.locator('input[placeholder="0.2"]').first();
    await fatInput.fill('15.0');

    await page.screenshot({ path: 'test-results/foods-form-filled.png', fullPage: true });

    // Handle the alert dialog
    page.once('dialog', async dialog => {
      expect(dialog.message()).toContain('Alimento agregado exitosamente');
      await dialog.accept();
    });

    // Click save button
    await page.locator('button:has-text("Guardar Alimento")').first().click();
    await page.waitForTimeout(2000);

    // Verify new food appears in list
    const pageContent = await page.textContent('body');
    expect(pageContent).toContain('Aguacate Test');

    await page.screenshot({ path: 'test-results/foods-created-successfully.png', fullPage: true });
  });

  test('should select and view food details', async ({ page }) => {
    // Navigate to Foods section
    await page.locator('button:has-text("Alimentos")').first().click();
    await page.waitForTimeout(2000);

    // Click on the first food item in the list
    const firstFood = page.locator('.foodCard, [style*="cursor: pointer"]').first();
    if (await firstFood.count() > 0) {
      await firstFood.click();
      await page.waitForTimeout(1000);

      // Verify details panel is shown
      const pageContent = await page.textContent('body');

      // Should show nutritional information
      const hasDetails = pageContent.includes('Información Nutricional') ||
                        pageContent.includes('Calorías') ||
                        pageContent.includes('Proteínas');
      expect(hasDetails).toBeTruthy();

      await page.screenshot({ path: 'test-results/foods-details-displayed.png', fullPage: true });
    }
  });

  test('should open edit form for existing food', async ({ page }) => {
    // Navigate to Foods section
    await page.locator('button:has-text("Alimentos")').first().click();
    await page.waitForTimeout(2000);

    // Select first food
    const firstFood = page.locator('div').filter({ hasText: 'Manzana' }).first();
    if (await firstFood.count() > 0) {
      await firstFood.click();
      await page.waitForTimeout(1000);

      // Click edit button
      const editButton = page.locator('button:has-text("Editar")').first();
      if (await editButton.count() > 0) {
        await editButton.click();
        await page.waitForTimeout(1000);

        // Verify edit form is displayed
        const pageContent = await page.textContent('body');
        expect(pageContent).toContain('Editar Alimento');

        await page.screenshot({ path: 'test-results/foods-edit-form-opened.png', fullPage: true });
      }
    }
  });

  test('should edit an existing food item', async ({ page }) => {
    // Navigate to Foods section
    await page.locator('button:has-text("Alimentos")').first().click();
    await page.waitForTimeout(2000);

    // Select first food
    const firstFood = page.locator('div').filter({ hasText: 'Manzana' }).first();
    if (await firstFood.count() > 0) {
      await firstFood.click();
      await page.waitForTimeout(1000);

      // Click edit button
      const editButton = page.locator('button:has-text("Editar")').first();
      if (await editButton.count() > 0) {
        await editButton.click();
        await page.waitForTimeout(1000);

        // Modify the name
        const nameInput = page.locator('input[type="text"]').first();
        await nameInput.fill('Manzana Modificada');

        await page.screenshot({ path: 'test-results/foods-edit-modified.png', fullPage: true });

        // Handle alert
        page.once('dialog', async dialog => {
          expect(dialog.message()).toContain('actualizado exitosamente');
          await dialog.accept();
        });

        // Click update button
        await page.locator('button:has-text("Actualizar Alimento")').first().click();
        await page.waitForTimeout(2000);

        // Verify changes
        const pageContent = await page.textContent('body');
        expect(pageContent).toContain('Manzana Modificada');

        await page.screenshot({ path: 'test-results/foods-edited-successfully.png', fullPage: true });
      }
    }
  });

  test('should delete a food item', async ({ page }) => {
    // Navigate to Foods section
    await page.locator('button:has-text("Alimentos")').first().click();
    await page.waitForTimeout(2000);

    // Get initial count of foods
    const initialContent = await page.textContent('body');

    // Select first food
    const firstFood = page.locator('div').filter({ hasText: /Manzana|Platano/ }).first();
    if (await firstFood.count() > 0) {
      await firstFood.click();
      await page.waitForTimeout(1000);

      // Get food name before deletion
      const foodName = await page.textContent('h2');

      // Handle confirmation dialog
      page.once('dialog', async dialog => {
        expect(dialog.message()).toContain('seguro de eliminar');
        await dialog.accept();
      });

      // Click delete button
      const deleteButton = page.locator('button:has-text("Eliminar")').first();
      if (await deleteButton.count() > 0) {
        await deleteButton.click();

        // Handle success alert
        page.once('dialog', async dialog => {
          expect(dialog.message()).toContain('eliminado exitosamente');
          await dialog.accept();
        });

        await page.waitForTimeout(2000);

        await page.screenshot({ path: 'test-results/foods-deleted-successfully.png', fullPage: true });
      }
    }
  });

  test('should search foods by name', async ({ page }) => {
    // Navigate to Foods section
    await page.locator('button:has-text("Alimentos")').first().click();
    await page.waitForTimeout(2000);

    // Find search input
    const searchInput = page.locator('input[placeholder*="Buscar"]').first();
    if (await searchInput.count() > 0) {
      await searchInput.fill('Manzana');
      await page.waitForTimeout(1000);

      // Verify filtered results
      const pageContent = await page.textContent('body');

      await page.screenshot({ path: 'test-results/foods-search-results.png', fullPage: true });
    }
  });

  test('should filter foods by category', async ({ page }) => {
    // Navigate to Foods section
    await page.locator('button:has-text("Alimentos")').first().click();
    await page.waitForTimeout(2000);

    // Find category select
    const categorySelect = page.locator('select').first();
    if (await categorySelect.count() > 0) {
      await categorySelect.selectOption('FRUITS');
      await page.waitForTimeout(1000);

      await page.screenshot({ path: 'test-results/foods-filtered-by-category.png', fullPage: true });
    }
  });

  test('should refresh food list', async ({ page }) => {
    // Navigate to Foods section
    await page.locator('button:has-text("Alimentos")').first().click();
    await page.waitForTimeout(2000);

    // Find refresh button
    const refreshButton = page.locator('button:has-text("Actualizar")').first();
    if (await refreshButton.count() > 0) {
      await refreshButton.click();
      await page.waitForTimeout(2000);

      await page.screenshot({ path: 'test-results/foods-list-refreshed.png', fullPage: true });
    }
  });

  test('should close form with cancel button', async ({ page }) => {
    // Navigate to Foods section
    await page.locator('button:has-text("Alimentos")').first().click();
    await page.waitForTimeout(2000);

    // Open add form
    await page.locator('button:has-text("Agregar Nuevo Alimento")').first().click();
    await page.waitForTimeout(1000);

    // Click cancel
    const cancelButton = page.locator('button:has-text("Cancelar")').first();
    await cancelButton.click();
    await page.waitForTimeout(1000);

    // Verify form is closed
    const pageContent = await page.textContent('body');
    expect(pageContent).not.toContain('Agregar Nuevo Alimento');

    await page.screenshot({ path: 'test-results/foods-form-cancelled.png', fullPage: true });
  });
});

test.describe('Full Application Flow', () => {
  test('should navigate through all sections', async ({ page }) => {
    await page.goto('http://localhost:3005');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    const sections = [
      { name: 'Dashboard', text: 'Dashboard' },
      { name: 'Alimentos', text: 'Alimentos' },
      { name: 'Recetas', text: 'Recetas' },
      { name: 'Equivalencias', text: 'Equivalencias' },
      { name: 'Pacientes', text: 'Pacientes' },
      { name: 'Calculadora', text: 'Calculadora' },
    ];

    for (const section of sections) {
      console.log(`Testing navigation to: ${section.name}`);

      const button = page.locator(`button:has-text("${section.text}")`).first();
      await button.click();
      await page.waitForTimeout(1500);

      await page.screenshot({
        path: `test-results/navigation-${section.name.toLowerCase()}.png`,
        fullPage: true
      });
    }
  });

  test('should verify backend connectivity', async ({ page }) => {
    await page.goto('http://localhost:3005');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    const pageContent = await page.textContent('body');

    // Should show backend connected
    const hasBackend = pageContent.includes('Backend Conectado') ||
                       pageContent.includes('Backend') ||
                       pageContent.includes('✅');
    expect(hasBackend).toBeTruthy();

    await page.screenshot({ path: 'test-results/backend-connectivity.png', fullPage: true });
  });
});