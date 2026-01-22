import pytest
import allure
import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


# -------------------- TEST CASE --------------------
@pytest.mark.smoke
@allure.parent_suite("Web Automation")
@allure.suite("Products")
@allure.sub_suite("Create Product")
@allure.feature("Product Management")
@allure.title("TC03 - Create Product with Category Meals → Breakfast")
def test_create_product_meals_breakfast(driver):

    wait = WebDriverWait(driver, 30)

    # ---------------- OPEN TENANT PAGE ----------------
    with allure.step("Open Tenant Select Page"):
        driver.get(
            "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/webshopnotfound"
        )

    with allure.step("Enter Tenant ID"):
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
    with allure.step("Login as Supplier"):
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

        wait.until(EC.url_contains("/supplier/dashboard"))

    # ---------------- PRODUCTS PAGE ----------------
    with allure.step("Open Products Page"):
        driver.get(
            "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/products"
        )
        wait.until(EC.url_contains("/supplier/products"))
        take_screenshot(driver, "products_page")

    # ---------------- CLICK NEW ----------------
    with allure.step("Click New Product"):
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='New']"))
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

        take_screenshot(driver, "category_meals_breakfast_selected")

    # ---------------- PRODUCT DETAILS ----------------
    with allure.step("Enter Product Name"):
        name_input = wait.until(
            EC.visibility_of_element_located((By.NAME, "name"))
        )
        name_input.clear()
        name_input.send_keys("Croissant")
        take_screenshot(driver, "product_name_entered")

    with allure.step("Enter Product Summary"):
        summary_input = wait.until(
            EC.visibility_of_element_located((By.NAME, "shortDescription"))
        )
        summary_input.clear()
        summary_input.send_keys(
            "A freshly baked, flaky butter croissant with a golden crust, "
            "perfect for a light and satisfying breakfast."
        )
        take_screenshot(driver, "product_summary_entered")

    with allure.step("Enter Price Note"):
        price_note = wait.until(
            EC.visibility_of_element_located((By.NAME, "priceNote"))
        )
        price_note.clear()
        price_note.send_keys("Day Rental")
        take_screenshot(driver, "price_note_entered")

    with allure.step("Enter Base Price"):
        base_price = wait.until(
            EC.visibility_of_element_located((By.NAME, "basePrice"))
        )
        base_price.clear()
        base_price.send_keys("5")
        take_screenshot(driver, "base_price_entered")

    with allure.step("Enter Security Deposit"):
        bond_input = wait.until(
            EC.visibility_of_element_located((By.NAME, "bond"))
        )
        bond_input.clear()
        bond_input.send_keys("2")
        take_screenshot(driver, "bond_entered")

    # ---------------- IMAGE UPLOAD ----------------
    with allure.step("Upload Product Image"):
        image_path = r"C:\Users\Suchini\Desktop\Test Automation\test_images\croissant.jpg"

        file_input = wait.until(
            EC.presence_of_element_located((By.NAME, "inputFieldName"))
        )
        file_input.send_keys(image_path)

        take_screenshot(driver, "image_uploaded")

        wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "spinner-border"))
        )

    # ---------------- CREATE PRODUCT ----------------
    with allure.step("Click Create Button"):
        create_btn = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[@type='submit' and normalize-space()='Create']"
            ))
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", create_btn
        )
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", create_btn)

        take_screenshot(driver, "product_created")

    with allure.step("Verify Product Details Tab"):
        details_tab = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//a[contains(@class,'nav-link') and .//span[normalize-space()='Details']]"
            ))
        )
        driver.execute_script("arguments[0].click();", details_tab)

    print("✅ TEST PASSED — Product created successfully")
