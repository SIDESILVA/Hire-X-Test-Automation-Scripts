# tests/test_list_create.py

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time
from datetime import datetime


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
    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    print("✅ Browser kept open for inspection")


# -------------------- Test Case --------------------
@allure.title("Supplier Dashboard - Navigate to List Section and Click New")
def test_navigate_to_list_section(driver):
    wait = WebDriverWait(driver, 30)

    # -------- Tenant Page --------
    driver.get(
        "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/webshopnotfound"
    )

    tenant_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
    )
    tenant_input.clear()
    tenant_input.send_keys("GrandRest")

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Set Tenant')]"))
    ).click()

    wait.until(EC.url_contains("/home"))
    take_screenshot(driver, "tenant_set")

    # -------- Login --------
    wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'sign')]"
        ))
    ).click()

    wait.until(EC.url_contains("/login"))

    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@type='email']"))
    ).send_keys("suchini@ateamsoftware.com")

    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))
    ).send_keys("Abc12345")

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]"))
    ).click()

    # -------- Dashboard --------
    wait.until(EC.url_contains("/supplier/dashboard"))
    take_screenshot(driver, "dashboard_loaded")

    # -------- Navigate to List Section --------
    driver.get(
        "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/lists"
    )

    wait.until(EC.url_contains("/supplier/lists"))
    take_screenshot(driver, "list_page_loaded")
    print("✅ SUCCESS: Navigated to List section")

    # -------- Click New List Button --------
    with allure.step("Click New List button"):

        new_button = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[@type='button' and normalize-space()='New']"
            ))
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            new_button
        )
        time.sleep(0.5)

        driver.execute_script("arguments[0].click();", new_button)

        take_screenshot(driver, "new_list_button_clicked")
        print("✅ SUCCESS: New List button clicked")

        # -------- Enter List Name --------
    with allure.step("Enter List Name"):

        list_name_input = wait.until(
            EC.visibility_of_element_located((By.NAME, "listName"))
        )

        list_name_input.clear()
        unique_name = "Test_" + datetime.now().strftime("%Y%m%d%H%M%S")
        list_name_input.send_keys(unique_name)
        print(f"✅ Using unique list name: {unique_name}")

        take_screenshot(driver, "list_name_entered")
        print("✅ SUCCESS: List name entered as 'Customer'")

    # -------- Click Create Button --------
    with allure.step("Click Create button"):

        create_button = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[@type='submit' and normalize-space()='Create']"
            ))
        )

        create_button.click()

        take_screenshot(driver, "create_button_clicked")
        print("✅ SUCCESS: Create button clicked")