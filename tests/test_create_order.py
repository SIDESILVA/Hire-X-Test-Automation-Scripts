import pytest
import allure
import os
import time

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

        # Wait for product lookup input
        product_input = wait.until(
            EC.element_to_be_clickable((By.NAME, "productLookup"))
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", product_input
        )
        time.sleep(0.5)

        product_input.clear()
        product_input.send_keys(product_name)
        time.sleep(1)

        # Select first suggestion
        first_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//typeahead-container//button[1]")
            )
        )
        driver.execute_script("arguments[0].click();", first_option)

        # Quantity
        qty_input = wait.until(
            EC.visibility_of_element_located((By.NAME, "quantity"))
        )
        qty_input.clear()
        qty_input.send_keys(str(quantity))

        take_screenshot(driver, "product_selected_qty")

        # Add button
        add_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Add']")
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", add_btn
        )
        time.sleep(0.5)

        try:
            add_btn.click()
        except:
            driver.execute_script("arguments[0].click();", add_btn)

        take_screenshot(driver, "product_added_success")

        # Verify product added
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//*[contains(text(),'{product_name}')]")
            )
        )


# -------------------- TEST CASE --------------------
@pytest.mark.smoke
@allure.parent_suite("Web Automation")
@allure.suite("Orders")
@allure.sub_suite("Create Order")
@allure.feature("Order Management")
@allure.title("TC02 - Create Order with Product (No Save)")
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

        # ---------------- SELECT CUSTOMER ----------------
        with allure.step("Select Customer - Amantha Nirmal"):
            dropdown = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//ng-select"))
            )
            dropdown.click()
            time.sleep(1)

            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class,'ng-option') and contains(., 'Amantha Nirmal')]")
                )
            ).click()

            take_screenshot(driver, "customer_selected")

        # ---------------- CLICK CREATE ----------------
        with allure.step("Click Create Button"):
            create_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@type='submit' and contains(normalize-space(),'Create')]")
                )
            )
            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", create_btn
            )
            time.sleep(0.5)
            create_btn.click()

            take_screenshot(driver, "create_clicked")

        with allure.step("Wait for Order Details Page"):
            wait.until(EC.url_contains("/supplier/orders/"))
            take_screenshot(driver, "order_details_page")

        # ---------------- ADD PRODUCT ONLY ----------------
        add_product(driver, wait, "Set", 2)

        # ✅ Test intentionally ends here
        take_screenshot(driver, "test_completed_without_save")
        print("✅ Product added successfully (Save step skipped)")

    except Exception as e:
        take_screenshot(driver, "test_failed")
        pytest.fail(f"Test failed due to error: {str(e)}")
