// tests/e2e/login-ui.spec.js
import { test, expect } from '@playwright/test';

test('Login page UI', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  
  await expect(page.getByText('Login to Social Circles')).toBeVisible();
  await expect(page.locator('#username')).toBeVisible();
  await expect(page.locator('#password')).toBeVisible();
  await expect(page.getByRole('button', { name: 'Login' })).toBeVisible();
  
  // Button state
  await expect(page.getByRole('button', { name: 'Login' })).toBeDisabled();
  
  await page.locator('#username').fill('test');
  await page.locator('#password').fill('test');
  
  await expect(page.getByRole('button', { name: 'Login' })).toBeEnabled();
});