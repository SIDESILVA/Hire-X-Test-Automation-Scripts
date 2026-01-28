# Dashboard Customer Creation Test Script - Open New Customer Form and Fill Name

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    yield driver
    print("✅ Test finished. Browser remains open for inspection.")

# -------------------- Test Case --------------------
@allure.title("Supplier Dashboard - Open New Customer Form and Fill Name")
def test_open_new_customer_form_fill_name(driver):
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

        # ---------------- CUSTOMERS PAGE ----------------
        driver.get(
            "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/customers"
        )
        wait.until(EC.url_contains("/supplier/customers"))

        take_screenshot(driver, "customer_page_opened")
        print("✅ SUCCESS: Navigated to Customers section")

        # ---------------- CLICK NEW CUSTOMER ----------------
        with allure.step("Click New Customer Button"):
            new_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='New']"))
            )
            driver.execute_script("arguments[0].click();", new_button)
            take_screenshot(driver, "new_customer_clicked")
            print("✅ SUCCESS: New Customer button clicked - Form opened")

        # ---------------- ENTER FIRST NAME AND LAST NAME ----------------
        with allure.step("Enter Customer First Name and Last Name"):
            # First Name
            first_name_input = wait.until(
                EC.visibility_of_element_located((By.NAME, "firstName"))
            )
            first_name_input.clear()
            first_name_input.send_keys("Niseni")

            # Last Name
            last_name_input = wait.until(
                EC.visibility_of_element_located((By.NAME, "lastName"))
            )
            last_name_input.clear()
            last_name_input.send_keys("Senanayaka")

            take_screenshot(driver, "customer_name_entered")
            print("✅ SUCCESS: First Name and Last Name entered")

                # ---------------- ENTER EMAIL AND PHONE NUMBER ----------------
        with allure.step("Enter Customer Email and Phone Number"):

            # Email Address
            email_input = wait.until(
                EC.visibility_of_element_located((By.NAME, "emailAddress"))
            )
            email_input.clear()
            email_input.send_keys("niseni@gmail.com")

            # Phone Number
            phone_input = wait.until(
                EC.visibility_of_element_located((By.NAME, "phoneNumber"))
            )
            phone_input.clear()
            phone_input.send_keys("0752569852")

            take_screenshot(driver, "customer_email_phone_entered")
            print("✅ SUCCESS: Email and Phone Number entered")

                    # ---------------- ENTER CUSTOMER ADDRESS ----------------
        with allure.step("Enter Customer Address Details"):

            # Address Line 1
            address1_input = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "input[autocomplete='address-line1']")
                )
            )
            address1_input.clear()
            address1_input.send_keys("No.23/A, Main Rd,")

            # Address Line 2
            address2_input = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "input[autocomplete='address-line2']")
                )
            )
            address2_input.clear()
            address2_input.send_keys("Malabe")

            # Suburb
            suburb_input = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//label[normalize-space()='Suburb']/following::input[1]")
                )
            )
            suburb_input.clear()
            suburb_input.send_keys("Kaduwela")

            take_screenshot(driver, "customer_address_entered")
            print("✅ SUCCESS: Customer address entered")

                # ---------------- SELECT CUSTOMER STATE ----------------
        with allure.step("Select Customer State"):

            # Locate the State dropdown based on the label
            state_dropdown = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//label[normalize-space()='State']/following::select[1]")
                )
            )

            # Scroll into view (optional but stable)
            driver.execute_script("arguments[0].scrollIntoView(true);", state_dropdown)
            time.sleep(0.5)

            # Click to open dropdown
            state_dropdown.click()
            time.sleep(0.5)

            # Select the option Victoria
            victoria_option = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//label[normalize-space()='State']/following::select[1]/option[@value='VIC']")
                )
            )
            victoria_option.click()

            take_screenshot(driver, "customer_state_selected")
            print("✅ SUCCESS: Customer State selected as Victoria")

        # ---------------- ENTER CUSTOMER POSTCODE ----------------
        with allure.step("Enter Customer Postcode"):

            postcode_input = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "input[autocomplete='postal-code']")
                )
            )

            driver.execute_script("arguments[0].scrollIntoView(true);", postcode_input)
            time.sleep(0.5)

            postcode_input.clear()
            postcode_input.send_keys("34/B")

            take_screenshot(driver, "customer_postcode_entered")
            print("✅ SUCCESS: Customer Postcode entered as 34/B")

        # ---------------- CLICK CREATE CUSTOMER ----------------
        with allure.step("Click Create Customer Button"):

            create_button = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//div[contains(@class,'modal-footer')]//button[@type='submit' and normalize-space()='Create']"
                ))
            )

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", create_button)
            time.sleep(0.5)

            driver.execute_script("arguments[0].click();", create_button)

            take_screenshot(driver, "create_customer_clicked")
            print("✅ SUCCESS: Create button clicked")

    finally:
        print("✅ Test finished. Browser remains open.")
