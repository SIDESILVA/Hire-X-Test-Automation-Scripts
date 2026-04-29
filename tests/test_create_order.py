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

def change_hire_status(driver, wait):
    with allure.step("Change Hire Status (Next Status)"):

        # 🔹 Wait for UI to stabilize after product add
        time.sleep(2)

        # 🔹 Click status dropdown button (Recieved)
        status_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class,'dropdown-toggle') and contains(@class,'button-warning')]")
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", status_btn
        )
        driver.execute_script("arguments[0].click();", status_btn)

        # 🔹 Wait for dropdown menu
        options = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//ul[contains(@class,'dropdown-menu') and contains(@class,'show')]//a")
            )
        )

        valid_options = [opt for opt in options if opt.text.strip() != ""]

        if len(valid_options) == 0:
            raise Exception("No status options found")

        # 🔹 Click FIRST option (Requested)
        next_status = valid_options[0]
        status_name = next_status.text.strip()

        driver.execute_script("arguments[0].click();", next_status)

        print(f"✅ Status changed to: {status_name}")
        take_screenshot(driver, "status_changed")

# -------------------- CLOSE MODAL --------------------
def close_order_modal(driver, wait):
    with allure.step("Close Order Details Modal"):

        close_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@aria-label='Close']")
            )
        )

        close_btn.click()

        wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'modal')]")
            )
        )

        take_screenshot(driver, "modal_closed")


# -------------------- TEST CASE --------------------
@pytest.mark.smoke
@allure.parent_suite("Web Automation")
@allure.suite("Orders")
@allure.sub_suite("Create Order")
@allure.feature("Order Management")
@allure.title("TC02 - Create Order with Product + Status Change")
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

        # ---------------- SELECT CUSTOMER ----------------
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

            selected = random.choice(valid_options)
            selected.click()

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

        # ---------------- CHANGE STATUS AFTER PRODUCT ----------------
        change_hire_status(driver, wait)

        # ---------------- CLOSE MODAL ----------------
        close_order_modal(driver, wait)

        take_screenshot(driver, "test_completed")

    except Exception as e:
        take_screenshot(driver, "test_failed")
        pytest.fail(f"Test failed due to error: {str(e)}")