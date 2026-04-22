# Dashboard Product Creation Test Script - Select Category (Meals -> Breakfast)

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys  # ✅ added
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

            dropdown_btn = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(@class,'dropdown-toggle') and contains(.,'Please select')]"
                ))
            )
            driver.execute_script("arguments[0].click();", dropdown_btn)

            meals_expand_icon = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//label[normalize-space()='Meals']/preceding-sibling::span"
                ))
            )
            driver.execute_script("arguments[0].click();", meals_expand_icon)

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

            image_path = r"C:\Users\Suchini\Desktop\Test Automation\test_images\croissant.jpg"

            file_input = wait.until(
                EC.presence_of_element_located((By.NAME, "inputFieldName"))
            )

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
            time.sleep(1)

            driver.execute_script("arguments[0].click();", create_button)

            take_screenshot(driver, "create_button_clicked")
            print("✅ SUCCESS: Create button clicked")

            with allure.step("Wait for product creation redirect"):
                wait.until(EC.url_contains("/supplier/products/"))
                take_screenshot(driver, "product_created_redirect")
                print("✅ SUCCESS: Redirected to product details page")

        # ---------------- FINALISE NOW ----------------
        with allure.step("Click Finalise Now after product creation"):

            finalise_now_link = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//a[normalize-space()='Finalise Now']"
                ))
            )

            driver.execute_script("arguments[0].scrollIntoView(true);", finalise_now_link)
            time.sleep(1)

            driver.execute_script("arguments[0].click();", finalise_now_link)

            take_screenshot(driver, "finalise_now_clicked")
            print("✅ SUCCESS: Finalise Now clicked")

        with allure.step("Set Quantity to 15"):

        # ✅ WAIT for spinner overlay to disappear (THIS is the fix)
            wait.until(
                EC.invisibility_of_element_located(
                    (By.CLASS_NAME, "spinner-wrapper")
                )
            )

            quantity_input = wait.until(
                EC.visibility_of_element_located((By.NAME, "qty"))
            )

            # Scroll into view (extra safety)
            driver.execute_script("arguments[0].scrollIntoView(true);", quantity_input)
            time.sleep(0.5)

            # Click using JS to avoid interception edge cases
            driver.execute_script("arguments[0].click();", quantity_input)

            # Clear properly
            quantity_input.send_keys(Keys.CONTROL + "a")
            quantity_input.send_keys(Keys.DELETE)

            # Enter value
            quantity_input.send_keys("15")

            # Trigger Angular update
            quantity_input.send_keys(Keys.TAB)

            take_screenshot(driver, "quantity_set_15")
            print("✅ SUCCESS: Quantity set to 15")

                # ---------------- FEATURED PRODUCT ----------------
        with allure.step("Select Featured Product checkbox"):

            # Wait again in case any small loader appears
            wait.until(
                EC.invisibility_of_element_located(
                    (By.CLASS_NAME, "spinner-wrapper")
                )
            )

            featured_checkbox = wait.until(
                EC.element_to_be_clickable((By.NAME, "isFeatured"))
            )

            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView(true);", featured_checkbox)
            time.sleep(0.5)

            # Click using JS (more reliable for Angular checkbox)
            driver.execute_script("arguments[0].click();", featured_checkbox)

            take_screenshot(driver, "featured_product_selected")
            print("✅ SUCCESS: Featured product checkbox selected")

                # ---------------- SAVE BUTTON ----------------
        with allure.step("Click Save button"):

            # Wait for any loader to disappear
            wait.until(
                EC.invisibility_of_element_located(
                    (By.CLASS_NAME, "spinner-wrapper")
                )
            )

            save_button = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[@type='submit' and normalize-space()='Save']"
                ))
            )

            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
            time.sleep(0.5)

            # Click using JS (consistent with your flow)
            driver.execute_script("arguments[0].click();", save_button)

            take_screenshot(driver, "save_button_clicked")
            print("✅ SUCCESS: Save button clicked")

        # ---------------- CLICK PRODUCTS MENU ----------------
        with allure.step("Click Products menu"):

            # Wait for page/navigation to stabilize after Save
            wait.until(EC.url_contains("/supplier"))

            # Wait for sidebar to be present
            products_menu = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//a[contains(@href,'/supplier/products')]"
                ))
            )

            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView(true);", products_menu)
            time.sleep(1)

            # Wait until clickable (extra safety)
            wait.until(EC.element_to_be_clickable((
                By.XPATH,
                "//a[contains(@href,'/supplier/products')]"
            )))

            # Click using JS (Angular safe)
            driver.execute_script("arguments[0].click();", products_menu)

            take_screenshot(driver, "products_menu_clicked")
            print("✅ SUCCESS: Products menu clicked")

            # Confirm navigation
            wait.until(EC.url_contains("/supplier/products"))

    finally:
        print("✅ Test finished. Browser remains open.")