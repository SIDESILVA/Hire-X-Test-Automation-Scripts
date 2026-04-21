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
import json

ROTATION_FILE = "task_type_index.json"

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
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    yield driver

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
        wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "spinner-wrapper"))
        )

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

        # ---------------- SELECT TASK TYPE (ROTATING ORDER FIXED) ----------------
        with allure.step("Select rotating task type from dropdown"):

            type_dropdown = wait.until(
                EC.element_to_be_clickable((By.NAME, "noteTypeId"))
            )
            type_dropdown.click()

            options = wait.until(
                EC.presence_of_all_elements_located((
                    By.XPATH,
                    "//select[@name='noteTypeId']/option"
                ))
            )

            types = [opt.text.strip() for opt in options if opt.text.strip()]
            print(f"📋 Available task types: {types}")

            # ---- load index ----
            if os.path.exists(ROTATION_FILE):
                with open(ROTATION_FILE, "r") as f:
                    index = json.load(f).get("index", 0)
            else:
                index = 0

            # ---- rotate sequentially ----
            selected_type = types[index % len(types)]

            # ---- save next index ----
            with open(ROTATION_FILE, "w") as f:
                json.dump({"index": index + 1}, f)

            print(f"🎯 Selected task type: {selected_type}")

            # ---- click selection ----
            for opt in options:
                if opt.text.strip() == selected_type:
                    opt.click()
                    break

            take_screenshot(driver, f"selected_task_type_{selected_type}")

        # ---------------- SELECT RESPONSIBLE USER ----------------
        with allure.step("Select rotating user from dropdown"):

            user_dropdown = wait.until(
                EC.element_to_be_clickable((By.NAME, "user"))
            )
            user_dropdown.click()

            options = wait.until(
                EC.presence_of_all_elements_located((
                    By.XPATH,
                    "//select[@name='user']/option"
                ))
            )

            users = [opt.text for opt in options if opt.text.strip()]

            print(f"👥 Available users: {users}")

            index = int(time.time()) % len(users)
            selected_user = users[index]

            print(f"🎯 Selected user: {selected_user}")

            for opt in options:
                if opt.text.strip() == selected_user:
                    opt.click()
                    break

            take_screenshot(driver, f"selected_user_{selected_user}")

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