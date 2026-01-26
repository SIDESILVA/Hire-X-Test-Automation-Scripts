# Dashboard Product Creation Test Script - Select Category (Meals -> Breakfast)

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time

chrome_driver_path = r"C:\Users\Suchini\Desktop\Test Automation\chromedriver.exe"


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

    # Selenium Manager will auto-download ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    yield driver

    print("✅ Test finished. Browser remains open for inspection.")



# -------------------- Test Case --------------------
@allure.title("Supplier Dashboard - Select Category Meals → Breakfast")
def test_open_product_form_select_category(driver):
    wait = WebDriverWait(driver, 30)

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

        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Set Tenant')]"))
        ).click()

        wait.until(EC.url_contains("/home"))

        # ---------------- LOGIN ----------------
        wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'sign')]"
            ))
        ).click()

        wait.until(EC.url_contains("/login"))

        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@type,'email')]"))
        ).send_keys("suchini@ateamsoftware.com")

        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@type,'password')]"))
        ).send_keys("Abc12345")

        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]"))
        ).click()

        # ---------------- DASHBOARD ----------------
        wait.until(EC.url_contains("/supplier/dashboard"))

        # ---------------- PRODUCTS PAGE ----------------
        driver.get(
            "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/products"
        )
        wait.until(EC.url_contains("/supplier/products"))

        # ---------------- CLICK NEW ----------------
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='New']"))
        ).click()

        # ---------------- CATEGORY SELECTION ----------------
        with allure.step("Select Category: Meals → Breakfast"):

            # Open category dropdown
            dropdown_btn = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(@class,'dropdown-toggle') and contains(.,'Please select')]"
                ))
            )
            driver.execute_script("arguments[0].click();", dropdown_btn)

            # ---------------- EXPAND MEALS (CLICK CARET) ----------------
            meals_expand_icon = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//label[normalize-space()='Meals']/preceding-sibling::span"
                ))
            )
            driver.execute_script("arguments[0].click();", meals_expand_icon)

            # ---------------- SELECT BREAKFAST ----------------
            breakfast_option = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//label[normalize-space()='Breakfast']"
                ))
            )
            driver.execute_script("arguments[0].click();", breakfast_option)

            take_screenshot(driver, "meals_breakfast_selected")
            print("✅ SUCCESS: Meals → Breakfast selected")

        with allure.step("Enter Product Name"):

            product_name_input = wait.until(
                EC.visibility_of_element_located((By.NAME, "name"))
            )
            product_name_input.clear()
            product_name_input.send_keys("Croissant")

            take_screenshot(driver, "product_name_entered")
            print("✅ SUCCESS: Product name entered as 'Croissant'")

        with allure.step("Enter Product Summary"):

            summary_text = (
                "A freshly baked, flaky butter croissant with a golden crust, "
                "perfect for a light and satisfying breakfast."
            )

            summary_input = wait.until(
                EC.visibility_of_element_located((By.NAME, "shortDescription"))
            )
            summary_input.clear()
            summary_input.send_keys(summary_text)

            take_screenshot(driver, "product_summary_entered")
            print("✅ SUCCESS: Product summary entered")
        
        with allure.step("Enter Additional Price Information"):

            price_note_input = wait.until(
                EC.visibility_of_element_located((By.NAME, "priceNote"))
            )
            price_note_input.clear()
            price_note_input.send_keys("Day Rental")

            take_screenshot(driver, "additional_price_info_entered")
            print("✅ SUCCESS: Additional Price Information entered")

        with allure.step("Enter Base Price"):

            base_price_input = wait.until(
                EC.visibility_of_element_located((By.NAME, "basePrice"))
            )
            base_price_input.clear()
            base_price_input.send_keys("5")

            take_screenshot(driver, "base_price_entered")
            print("✅ SUCCESS: Base Price entered as 5")


        with allure.step("Enter Security Deposit"):

            security_deposit_input = wait.until(
                EC.visibility_of_element_located((By.NAME, "bond"))
            )
            security_deposit_input.clear()
            security_deposit_input.send_keys("2")

            take_screenshot(driver, "security_deposit_entered")
            print("✅ SUCCESS: Security Deposit entered as 2")

        with allure.step("Upload Product Image"):

            # Absolute path of your test image
            image_path = r"C:\Users\Suchini\Desktop\Test Automation\test_images\croissant.jpg"

            # Locate the hidden file input
            file_input = wait.until(
                EC.presence_of_element_located((By.NAME, "inputFieldName"))
            )

            # Upload the image
            file_input.send_keys(image_path)

            take_screenshot(driver, "product_image_uploaded")
            print("✅ SUCCESS: Product image uploaded")

        with allure.step("Wait for image upload to complete"):
            wait.until(
                EC.invisibility_of_element_located(
                    (By.CLASS_NAME, "spinner-border")
                )
            )

        with allure.step("Click Create Button"):

            create_button = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[@type='submit' and normalize-space()='Create']"
                ))
            )

            driver.execute_script("arguments[0].scrollIntoView(true);", create_button)
            time.sleep(1)  # small pause for stability

            driver.execute_script("arguments[0].click();", create_button)

            take_screenshot(driver, "create_button_clicked")
            print("✅ SUCCESS: Create button clicked")

            with allure.step("Wait for product creation redirect"):
                wait.until(EC.url_contains("/supplier/products/"))
                take_screenshot(driver, "product_created_redirect")
                print("✅ SUCCESS: Redirected to product details page")


    finally:
        print("✅ Test finished. Browser remains open.")
