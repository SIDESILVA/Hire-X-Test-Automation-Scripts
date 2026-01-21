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
@allure.suite("Orders")
@allure.sub_suite("Create Order")
@allure.feature("Order Management")
@allure.title("TC02 - Create Order with Product and Save")
def test_login_and_create_order(driver):

    wait = WebDriverWait(driver, 25)

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

        driver.find_element(By.XPATH, "//input[contains(@type,'email')]").send_keys(
            "suchini@ateamsoftware.com"
        )
        driver.find_element(By.XPATH, "//input[contains(@type,'password')]").send_keys(
            "Abc12345"
        )
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
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Create Order')]"))
        )
        take_screenshot(driver, "create_order_form")

    # ---------------- SELECT CUSTOMER ----------------
    with allure.step("Select Customer - Amantha Nirmal"):
        dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//ng-select")))
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
            EC.presence_of_element_located(
                (By.XPATH, "//button[@type='submit' and contains(normalize-space(),'Create')]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", create_btn)
        wait.until(lambda d: create_btn.is_enabled())
        driver.execute_script("arguments[0].click();", create_btn)
        take_screenshot(driver, "create_clicked")

    with allure.step("Wait for Order Details Page"):
        wait.until(EC.url_contains("/supplier/orders/"))
        take_screenshot(driver, "order_details_page")

    # ---------------- ADD PRODUCT ----------------
    with allure.step("Add Product - Set Menu (Qty 2)"):
        product = wait.until(EC.element_to_be_clickable((By.NAME, "productLookup")))
        product.send_keys("Set")
        time.sleep(1)

        option = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//typeahead-container//button[1]"))
        )
        driver.execute_script("arguments[0].click();", option)

        qty = wait.until(EC.visibility_of_element_located((By.NAME, "quantity")))
        qty.clear()
        qty.send_keys("2")

        add_btn = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@type='submit' and normalize-space()='Add']")
            )
        )
        wait.until(lambda d: add_btn.is_enabled())
        driver.execute_script("arguments[0].click();", add_btn)

        take_screenshot(driver, "product_added")

    # ---------------- SAVE ORDER ----------------
    with allure.step("Save Order"):
        save_btn = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@type='submit' and normalize-space()='Save']")
            )
        )

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_btn)
        wait.until(lambda d: save_btn.is_enabled())
        time.sleep(0.5)

        driver.execute_script("arguments[0].click();", save_btn)
        take_screenshot(driver, "order_saved")

    print("✅ TEST PASSED — Order created and saved successfully")
