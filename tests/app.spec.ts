import { test, expect } from '@playwright/test';

test.describe('BaZingSe App - Full UI/UX Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to debug page with locale prefix (middleware redirects / to /en)
    await page.goto('http://localhost:4321/en/debug');
    await page.waitForTimeout(2000);
  });

  test('1. Page loads with header and logo', async ({ page }) => {
    const header = page.locator('header');
    await expect(header).toBeVisible();

    const logo = page.locator('img[alt="BaZingSe Logo"]');
    await expect(logo).toBeVisible();

    const title = page.locator('h1:has-text("BaZingSe")');
    await expect(title).toBeVisible();
  });

  test('2. Quick Test presets are visible and clickable', async ({ page }) => {
    const quickTestLabel = page.locator('text=Quick Test:');
    await expect(quickTestLabel).toBeVisible();

    const presetButtons = page.locator('button:has-text("1992-07-06")');
    await expect(presetButtons).toBeVisible();

    // Click a preset
    const malePreset = page.locator('button:has-text("1985-06-23")');
    await malePreset.click();
    await page.waitForTimeout(2000);

    // Verify the chart reloads (take screenshot to verify)
    await page.screenshot({ path: 'test-results/preset-click.png' });
  });

  test('3. Birth date inputs work correctly', async ({ page }) => {
    const dayInput = page.locator('input[placeholder="DD"]').first();
    await dayInput.fill('15');
    await page.waitForTimeout(1000);

    const monthInput = page.locator('input[placeholder="MM"]').first();
    await monthInput.fill('3');
    await page.waitForTimeout(1000);

    const yearInput = page.locator('input[placeholder="YYYY"]').first();
    await yearInput.fill('1990');
    await page.waitForTimeout(1500);

    await expect(dayInput).toHaveValue('15');
    await expect(monthInput).toHaveValue('3');
    await expect(yearInput).toHaveValue('1990');
  });

  test('4. Gender selection works', async ({ page }) => {
    const maleLabel = page.locator('label:has-text("♂")').first();
    await maleLabel.click();
    await page.waitForTimeout(1000);
    await page.screenshot({ path: 'test-results/gender-male.png' });
  });

  test('5. Unknown hour toggle works', async ({ page }) => {
    const unknownHourBtn = page.getByRole('button', { name: '?', exact: true });
    await unknownHourBtn.click();
    await page.waitForTimeout(1500);

    const timeInput = page.locator('input[value="?"]');
    await expect(timeInput).toBeVisible();

    await unknownHourBtn.click();
    await page.waitForTimeout(1000);
  });

  test('6. BaZi chart renders with 4 pillars', async ({ page }) => {
    await page.waitForTimeout(2000);
    // Check for stem Chinese characters in the chart
    const chart = page.locator('text=/[甲乙丙丁戊己庚辛壬癸]/');
    const count = await chart.count();
    expect(count).toBeGreaterThanOrEqual(4);
    await page.screenshot({ path: 'test-results/bazi-chart.png' });
  });

  test('7. Wu Xing Elements barchart renders', async ({ page }) => {
    await page.waitForTimeout(2000);
    // Title is now translated - look for "Day Master Analysis" heading
    const wuxingTitle = page.getByRole('heading', { name: /Day Master/ });
    await expect(wuxingTitle).toBeVisible();
    const dayMaster = page.locator('text=Day Master');
    await expect(dayMaster.first()).toBeVisible();
    // Check for favorable element text in either new narrative format or old format
    const favorable = page.getByText(/Favorable/).first();
    await expect(favorable).toBeVisible();
    await page.screenshot({ path: 'test-results/wuxing-elements.png' });
  });

  test('8. Time Travel mode can be enabled', async ({ page }) => {
    const timeTravelCheckbox = page.locator('text=🔮 Time Travel').locator('..').locator('input[type="checkbox"]');
    await timeTravelCheckbox.click();
    await page.waitForTimeout(2000);
    const annualLabel = page.locator('label:has-text("年運")').first();
    await expect(annualLabel).toBeVisible();
    await page.screenshot({ path: 'test-results/time-travel.png' });
  });

  test('9. Talisman section can be enabled', async ({ page }) => {
    // First ensure talisman is unchecked
    const talismanCheckbox = page.getByRole('checkbox', { name: /符/ });
    if (await talismanCheckbox.isChecked()) {
      await talismanCheckbox.click();
      await page.waitForTimeout(500);
    }
    // Now enable it
    await talismanCheckbox.click();
    await page.waitForTimeout(1500);
    // Check for talisman dropdown elements (Hour HS combobox)
    const talismanDropdown = page.getByRole('combobox').first();
    await expect(talismanDropdown).toBeVisible();
    await page.screenshot({ path: 'test-results/talisman.png' });
  });

  test('10. Location section can be enabled', async ({ page }) => {
    // The label is now translated as "地 Location" in English
    const locationCheckbox = page.getByRole('checkbox', { name: /地/ });
    await locationCheckbox.click();
    await page.waitForTimeout(1000);
    // Options are now translated but still contain Chinese chars
    const overseasRadio = page.getByText(/Overseas|海外/);
    await expect(overseasRadio.first()).toBeVisible();
    const birthplaceRadio = page.getByText(/Birthplace|故/);
    await expect(birthplaceRadio.first()).toBeVisible();
    await page.screenshot({ path: 'test-results/location.png' });
  });

  test('11. Different presets show different charts', async ({ page }) => {
    await page.locator('button:has-text("1969-07-04")').click();
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'test-results/preset-1969.png' });

    await page.locator('button:has-text("1988-02-02")').click();
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'test-results/preset-1988.png' });
  });

  test('12. Time travel with 10-Year Luck pillar', async ({ page }) => {
    const timeTravelCheckbox = page.locator('text=🔮 Time Travel').locator('..').locator('input[type="checkbox"]');
    await timeTravelCheckbox.click();
    await page.waitForTimeout(2000);
    // Look for 10-Year luck label (運 10Y or 10Y運)
    const luckLabel = page.getByText(/10Y|運/).first();
    await expect(luckLabel).toBeVisible();
    await page.screenshot({ path: 'test-results/luck-pillar.png' });
  });

  test('13. Monthly luck can be enabled after annual', async ({ page }) => {
    // Enable Date Comparison mode
    await page.getByText('🔮 Time Travel').click();
    await page.waitForTimeout(1500);

    // Find and click the annual luck label (年運 Annual)
    await page.getByText(/年運/).first().click();
    await page.waitForTimeout(1000);

    // After enabling annual, monthly slot should now have a checkbox
    // Verify the monthly label is visible (月運 Monthly)
    const monthlyActive = page.getByText(/月運/).first();
    await expect(monthlyActive).toBeVisible();
    await page.screenshot({ path: 'test-results/monthly-luck.png' });
  });

  test('14. Interaction badges render on pillars', async ({ page }) => {
    await page.locator('button:has-text("1992-07-06")').click();
    await page.waitForTimeout(2000);
    // Check for transformation badge
    const transformBadge = page.locator('text=化');
    const badgeCount = await transformBadge.count();
    console.log(`Found ${badgeCount} potential badge elements`);
    await page.screenshot({ path: 'test-results/interaction-badges.png' });
  });

  test('15. Hidden stems display in branch cards', async ({ page }) => {
    await page.waitForTimeout(2000);
    // Check for 10 gods display (7K, DO, etc.)
    const tenGods = page.locator('text=/^(7K|DO|DW|IW|F|HO|EG|RW|DR|IR)$/');
    const count = await tenGods.count();
    console.log(`Found ${count} hidden stem elements`);
    await page.screenshot({ path: 'test-results/hidden-stems.png' });
  });

  test('16. Full app screenshot', async ({ page }) => {
    await page.screenshot({ path: 'test-results/full-app.png', fullPage: true });
  });

  // New tests for additional coverage

  test('17. Daily luck cascading works', async ({ page }) => {
    // Enable Date Comparison mode
    await page.getByText('🔮 Time Travel').click();
    await page.waitForTimeout(1500);

    // Enable annual luck by clicking the label
    await page.getByText(/年運/).first().click();
    await page.waitForTimeout(500);

    // Enable monthly luck by clicking the label
    await page.getByText(/月運/).first().click();
    await page.waitForTimeout(500);

    // Fill in month value
    const monthInputLuck = page.locator('input[placeholder="MM"]').last();
    await monthInputLuck.fill('6');
    await page.waitForTimeout(1000);

    // Daily slot should now be active (not just gray placeholder)
    const dailyLabel = page.getByText(/日運/).first();
    await expect(dailyLabel).toBeVisible();
    await page.screenshot({ path: 'test-results/daily-luck.png' });
  });

  test('18. Hourly luck cascading works', async ({ page }) => {
    // Enable Date Comparison mode
    await page.getByText('🔮 Time Travel').click();
    await page.waitForTimeout(1000);

    // Enable annual luck by clicking the label
    await page.getByText(/年運/).first().click();
    await page.waitForTimeout(500);

    // Enable monthly luck by clicking the label
    await page.getByText(/月運/).first().click();
    await page.waitForTimeout(500);
    await page.locator('input[placeholder="MM"]').last().fill('6');
    await page.waitForTimeout(500);

    // Enable daily luck by clicking the label
    await page.getByText(/日運/).first().click();
    await page.waitForTimeout(500);
    await page.locator('input[placeholder="DD"]').last().fill('15');
    await page.waitForTimeout(1000);

    // Hourly slot should now be active (not just gray placeholder)
    const hourlyLabel = page.getByText(/時運/).first();
    await expect(hourlyLabel).toBeVisible();
    await page.screenshot({ path: 'test-results/hourly-luck.png' });
  });

  test('19. Talisman invalid Jia-Zi warning', async ({ page }) => {
    // First ensure talisman is enabled
    const talismanCheckbox = page.getByRole('checkbox', { name: /符/ });
    if (!await talismanCheckbox.isChecked()) {
      await talismanCheckbox.click();
      await page.waitForTimeout(1000);
    }

    const hourHSSelect = page.getByRole('combobox').first();
    await hourHSSelect.selectOption('甲 Jia (Yang Wood)');
    await page.waitForTimeout(500);

    const hourEBSelect = page.getByRole('combobox').nth(1);
    await hourEBSelect.selectOption('丑 Chou (Ox)');
    await page.waitForTimeout(1000);

    // The warning shows "Invalid pairs" or "Invalid Jia-Zi pair"
    const warning = page.getByText(/Invalid/);
    await expect(warning.first()).toBeVisible();
    await page.screenshot({ path: 'test-results/invalid-jiazi.png' });
  });

  test('20. Location overseas adds pillars', async ({ page }) => {
    const locationCheckbox = page.getByRole('checkbox', { name: /地/ });
    await locationCheckbox.click();
    await page.waitForTimeout(1000);

    // Radio button text is now translated
    const overseasRadio = page.getByText(/Overseas|海外/).first();
    await overseasRadio.click();
    await page.waitForTimeout(1500);

    // Chart should still render
    const chart = page.locator('text=/[甲乙丙丁戊己庚辛壬癸]/');
    expect(await chart.count()).toBeGreaterThan(0);
    await page.screenshot({ path: 'test-results/location-overseas.png' });
  });

  test('21. Location birthplace adds pillars', async ({ page }) => {
    const locationCheckbox = page.getByRole('checkbox', { name: /地/ });
    await locationCheckbox.click();
    await page.waitForTimeout(1000);

    // Radio button text is now translated
    const birthplaceRadio = page.getByText(/Birthplace|故/).first();
    await birthplaceRadio.click();
    await page.waitForTimeout(1500);

    // Chart should still render
    const chart = page.locator('text=/[甲乙丙丁戊己庚辛壬癸]/');
    expect(await chart.count()).toBeGreaterThan(0);
    await page.screenshot({ path: 'test-results/location-birthplace.png' });
  });

  test('22. localStorage persists on refresh', async ({ page }) => {
    // First clear any existing storage
    await page.evaluate(() => localStorage.clear());
    await page.reload();
    await page.waitForTimeout(2000);

    // Change year input
    const yearInput = page.locator('input[placeholder="YYYY"]').first();
    await yearInput.fill('1985');
    await page.waitForTimeout(1500);

    // Enable time travel
    const timeTravelCheckbox = page.locator('text=🔮 Time Travel').locator('..').locator('input[type="checkbox"]');
    await timeTravelCheckbox.click();
    await page.waitForTimeout(1000);

    // Reload without clearing storage
    await page.reload();
    await page.waitForTimeout(2000);

    // Verify data persisted
    const yearInputAfter = page.locator('input[placeholder="YYYY"]').first();
    await expect(yearInputAfter).toHaveValue('1985');

    const timeTravelCheckboxAfter = page.locator('text=🔮 Time Travel').locator('..').locator('input[type="checkbox"]');
    await expect(timeTravelCheckboxAfter).toBeChecked();
    await page.screenshot({ path: 'test-results/localstorage-persist.png' });
  });

  test('23. API error shows banner', async ({ page }) => {
    await page.route('**/api/analyze_bazi**', route => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Test API Error' })
      });
    });

    const dayInput = page.locator('input[placeholder="DD"]').first();
    await dayInput.fill('15');
    await page.waitForTimeout(2000);

    const errorBanner = page.locator('.bg-red-50');
    await expect(errorBanner).toBeVisible();
    await page.screenshot({ path: 'test-results/api-error.png' });
  });
});
