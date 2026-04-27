import pytest
import allure
import os
import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# -------------------- SCREENSHOT HELPER --------------------
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


# -------------------- ADD PRODUCT FUNCTION --------------------
def add_product(driver, wait, product_name, quantity):
    with allure.step(f"Add Product - {product_name} (Qty {quantity})"):

        product_input = wait.until(
            EC.element_to_be_clickable((By.NAME, "productLookup"))
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", product_input
        )

        product_input.clear()
        product_input.send_keys(product_name)

        # Wait for suggestions
        first_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//typeahead-container//button[1]")
            )
        )
        driver.execute_script("arguments[0].click();", first_option)

        qty_input = wait.until(
            EC.visibility_of_element_located((By.NAME, "quantity"))
        )
        qty_input.clear()
        qty_input.send_keys(str(quantity))

        take_screenshot(driver, "product_selected_qty")

        add_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Add']")
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", add_btn
        )

        try:
            add_btn.click()
        except:
            driver.execute_script("arguments[0].click();", add_btn)

        take_screenshot(driver, "product_added_success")

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//*[contains(text(),'{product_name}')]")
            )
        )


# -------------------- NEW: CHANGE HIRE STATUS FUNCTION --------------------
def change_hire_status(driver, wait):
    with allure.step("Change Hire Status (Next Status)"):

        # Locate dropdown button (Hire Status)
        status_dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'btn-group')]//button")
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", status_dropdown
        )

        # Open dropdown
        status_dropdown.click()

        # Wait for dropdown options
        options = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[contains(@class,'dropdown-menu')]//button | //div[contains(@class,'dropdown-menu')]//a")
            )
        )

        valid_options = [opt for opt in options if opt.text.strip() != ""]

        if len(valid_options) < 2:
            raise Exception("Not enough status options to change")

        next_status = valid_options[1]
        status_name = next_status.text

        try:
            next_status.click()
        except:
            driver.execute_script("arguments[0].click();", next_status)

        print(f"✅ Status changed to: {status_name}")
        take_screenshot(driver, "status_changed")


# -------------------- TEST CASE --------------------
@pytest.mark.smoke
@allure.parent_suite("Web Automation")
@allure.suite("Orders")
@allure.sub_suite("Create Order")
@allure.feature("Order Management")
@allure.title("TC02 - Create Order with Product (Auto Customer Selection)")
def test_login_and_create_order(driver):

    wait = WebDriverWait(driver, 30)

    try:
        # ---------------- LOGIN ----------------
        with allure.step("Open Tenant Select Page"):
            driver.get(
                "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/webshopnotfound"
            )

        with allure.step("Enter Tenant ID"):
            tenant = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
            )
            tenant.clear()
            tenant.send_keys("GrandRest")

        with allure.step("Set Tenant"):
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Set Tenant')]"))
            ).click()

        with allure.step("Navigate to Login"):
            wait.until(EC.url_contains("/home"))

            wait.until(
                EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class,'spinner')]"))
            )

            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'sign')]")
                )
            ).click()

        with allure.step("Login with credentials"):
            wait.until(EC.url_contains("/login"))
            driver.find_element(By.XPATH, "//input[contains(@type,'email')]") \
                .send_keys("suchini@ateamsoftware.com")
            driver.find_element(By.XPATH, "//input[contains(@type,'password')]") \
                .send_keys("Abc12345")
            driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()

        with allure.step("Verify Dashboard"):
            wait.until(EC.url_contains("/supplier/dashboard"))
            take_screenshot(driver, "dashboard_loaded")

        # ---------------- CREATE ORDER ----------------
        with allure.step("Open Orders Page"):
            driver.get(
                "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/orders"
            )
            wait.until(EC.url_contains("/supplier/orders"))
            take_screenshot(driver, "orders_page")

        with allure.step("Click New Order"):
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'New')]"))
            ).click()

        with allure.step("Verify Create Order Form"):
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Create Order')]"))
            )
            take_screenshot(driver, "create_order_form")

        # ---------------- SELECT CUSTOMER (AUTO) ----------------
        with allure.step("Select Random Customer"):

            dropdown = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//ng-select"))
            )
            dropdown.click()

            options = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[contains(@class,'ng-option')]")
                )
            )

            valid_options = [opt for opt in options if opt.text.strip() != ""]

            if not valid_options:
                raise Exception("No customers available in dropdown")

            selected = random.choice(valid_options)
            customer_name = selected.text
            selected.click()

            print(f"Selected Customer: {customer_name}")

        # ---------------- CLICK CREATE ----------------
        with allure.step("Click Create Button"):

            create_btn = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[@type='submit' and normalize-space()='Create']")
                )
            )

            wait.until(lambda d: create_btn.is_enabled())

            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", create_btn
            )

            time.sleep(0.5)

            try:
                create_btn.click()
            except:
                driver.execute_script("arguments[0].click();", create_btn)

            take_screenshot(driver, "create_clicked")

        # ---------------- ADD PRODUCT ----------------
        add_product(driver, wait, "Set", 2)

        # ---------------- NEW: CHANGE STATUS ----------------
        change_hire_status(driver, wait)

        take_screenshot(driver, "test_completed_without_save")
        print("✅ Product added successfully (Auto customer used)")

    except Exception as e:
        take_screenshot(driver, "test_failed")
        pytest.fail(f"Test failed due to error: {str(e)}")