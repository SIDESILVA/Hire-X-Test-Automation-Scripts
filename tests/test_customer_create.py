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
import random

# -------------------- REALISTIC NAME DATA --------------------
first_names = ["John", "Clara", "David", "Emma", "Michael", "Sophia", "Daniel", "Olivia"]
last_names = ["Smith", "Brown", "Taylor", "Wilson", "Lee", "Walker", "Hall", "Allen"]

def generate_name():
    # clean meaningful naming: test_John_Smith
    first = random.choice(first_names)
    last = random.choice(last_names)

    first_name = f"test_{first}"
    last_name = last
    return first_name, last_name


def random_phone():
    return "07" + ''.join(random.choices("0123456789", k=8))


def random_email():
    # keep email unique WITHOUT using name randomness in text
    return f"testuser{int(time.time())}@test.com"


def random_address():
    streets = ["Main Road", "High Street", "Lake Road", "Station Road"]
    return f"No.{random.randint(1,200)}/A, {random.choice(streets)}"


def random_suburb():
    suburbs = ["Colombo", "Kaduwela", "Malabe", "Nugegoda", "Dehiwala"]
    return random.choice(suburbs)


def random_postcode():
    return str(random.randint(10000, 99999))


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

        # ---------------- CLICK NEW CUSTOMER ----------------
        new_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='New']"))
        )
        driver.execute_script("arguments[0].click();", new_button)

        # ---------------- GENERATE DATA ----------------
        first_name, last_name = generate_name()
        email = random_email()
        phone = random_phone()
        address1 = random_address()
        suburb = random_suburb()
        postcode = random_postcode()

        print(f"Generated → {first_name} {last_name}")

        # ---------------- NAME ----------------
        first_name_input = wait.until(
            EC.visibility_of_element_located((By.NAME, "firstName"))
        )
        first_name_input.clear()
        first_name_input.send_keys(first_name)

        last_name_input = wait.until(
            EC.visibility_of_element_located((By.NAME, "lastName"))
        )
        last_name_input.clear()
        last_name_input.send_keys(last_name)

        take_screenshot(driver, "name_entered")

        # ---------------- EMAIL ----------------
        email_input = wait.until(
            EC.visibility_of_element_located((By.NAME, "emailAddress"))
        )
        email_input.clear()
        email_input.send_keys(email)

        # ---------------- PHONE ----------------
        phone_input = wait.until(
            EC.visibility_of_element_located((By.NAME, "phoneNumber"))
        )
        phone_input.clear()
        phone_input.send_keys(phone)

        # ---------------- ADDRESS ----------------
        address1_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[autocomplete='address-line1']"))
        )
        address1_input.clear()
        address1_input.send_keys(address1)

        suburb_input = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//label[normalize-space()='Suburb']/following::input[1]"))
        )
        suburb_input.clear()
        suburb_input.send_keys(suburb)

        # ---------------- STATE ----------------
        state_dropdown = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='State']/following::select[1]"))
        )
        state_dropdown.click()

        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//option[@value='VIC']"))
        ).click()

        # ---------------- POSTCODE ----------------
        postcode_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[autocomplete='postal-code']"))
        )
        postcode_input.clear()
        postcode_input.send_keys(postcode)

        # ---------------- CREATE ----------------
        create_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Create']"))
        )
        driver.execute_script("arguments[0].click();", create_button)

        take_screenshot(driver, "customer_created")

        print("✅ SUCCESS: Customer created with clean meaningful test names")

    finally:
        print("✅ Test finished. Browser remains open.")