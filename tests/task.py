# Dashboard Task Page Test Script

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time

# -------------------- Screenshot Helper --------------------
def take_screenshot(driver, step_name):
    if not os.path.exists("reports"):
        os.makedirs("reports")
    path = f"reports/{step_name}.png"
    driver.save_screenshot(path)
    allure.attach.file(
        path,
        name=step_name,
        attachment_type=allure.attachment_type.PNG
    )

# -------------------- Pytest Fixture --------------------
@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  # Keep browser open

    # Automatically download & manage ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    yield driver

    # Browser stays open because of detach=True
    print("✅ Test finished. Browser remains open for inspection.")

# -------------------- Test Case --------------------
@allure.title("Supplier Dashboard - Open Tasks Page")
def test_open_tasks_page(driver):
    wait = WebDriverWait(driver, 20)

    try:
        # ---------------- OPEN TENANT PAGE ----------------
        driver.get(
            "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/webshopnotfound"
        )
        tenant_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
        )
        tenant_input.clear()
        tenant_input.send_keys("GrandRest")

        set_tenant_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Set Tenant')]"))
        )
        set_tenant_button.click()

        wait.until(EC.url_contains("/home"))
        print("✅ Tenant page loaded")

        # ---------------- SIGN IN ----------------
        sign_in_button = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'sign')]"
            ))
        )
        sign_in_button.click()

        wait.until(EC.url_contains("/login"))

        email_input = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[contains(@type,'email') or contains(@formcontrolname,'email')]")
            )
        )
        password_input = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[contains(@type,'password') or contains(@formcontrolname,'password')]")
            )
        )

        email_input.send_keys("suchini@ateamsoftware.com")
        password_input.send_keys("Abc12345")

        login_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]"))
        )
        login_btn.click()

        # ---------------- DASHBOARD ----------------
        wait.until(EC.url_contains("/supplier/dashboard"))
        take_screenshot(driver, "dashboard_loaded")
        print("✅ Dashboard loaded successfully!")

        # ---------------- GO TO TASKS PAGE ----------------
        with allure.step("Navigate to Tasks page"):
            driver.get(
                "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/tasks"
            )
            wait.until(EC.url_contains("/supplier/tasks"))
            take_screenshot(driver, "tasks_page_loaded")
            print("✅ Tasks page opened successfully!")

        # ---------------- VALIDATE TASKS PAGE ----------------
        with allure.step("Validate Tasks page load (URL only)"):
            assert "/supplier/tasks" in driver.current_url
            take_screenshot(driver, "tasks_page_loaded_verified")
            print("✅ Tasks page loaded and URL validated")

        # ---------------- CLICK "NEW" BUTTON ----------------
        with allure.step("Click 'NEW' button to create a task"):
            new_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='New']"))
            )
            new_button.click()
            take_screenshot(driver, "clicked_new_button")
            print("✅ 'NEW' button clicked successfully!")

        # ---------------- SELECT TASK TYPE ----------------
        with allure.step("Select 'Checkout Items' from Type dropdown"):
            type_dropdown = wait.until(
                EC.element_to_be_clickable((By.NAME, "noteTypeId"))
            )
            select = Select(type_dropdown)
            select.select_by_visible_text("Checkout Items")
            take_screenshot(driver, "selected_task_type")
            print("✅ 'Checkout Items' selected in Type dropdown")

        # ---------------- SELECT RESPONSIBLE USER ----------------
        with allure.step("Select responsible user 'Ishanka Silva'"):
            user_dropdown = wait.until(
                EC.element_to_be_clickable((By.NAME, "user"))
            )
            user_dropdown.click()
            ishanka_option = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH, "//select[@name='user']/option[contains(normalize-space(.),'Ishanka')]"
                ))
            )
            ishanka_option.click()
            take_screenshot(driver, "selected_user_ishanka_silva")
            print("✅ User 'Ishanka Silva' selected successfully!")

        # ---------------- CLICK "CREATE" BUTTON ----------------
        with allure.step("Click 'Create' button to submit the task"):
            create_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Create']"))
            )
            create_button.click()
            take_screenshot(driver, "clicked_create_button")
            print("✅ 'Create' button clicked successfully!")

    finally:
        print("✅ Test finished. You can now manually close the browser.")
