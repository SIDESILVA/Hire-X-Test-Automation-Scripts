import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os

# -----------------------------
# Screenshot helper
# -----------------------------
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

# -----------------------------
# Pytest driver fixture (shared)
# -----------------------------
@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    # ✅ Selenium Manager auto-downloads ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    yield driver

    print("✅ Login test finished. Browser remains open.")

# -----------------------------
# Test: Login to GrandRest Tenant
# -----------------------------
@pytest.mark.smoke
@allure.parent_suite("Web Automation")
@allure.suite("Login")
@allure.sub_suite("GrandRest Tenant")
@allure.feature("Tenant Login")
@allure.title("TC01 - Login Test for GrandRest Tenant")
def test_login_grandrest(driver):

    wait = WebDriverWait(driver, 20)

    with allure.step("STEP 1: Open tenant select page"):
        driver.get(
            "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/webshopnotfound"
        )

    with allure.step("STEP 2: Enter tenant ID"):
        tenant_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
        )
        tenant_input.clear()
        tenant_input.send_keys("GrandRest")

    with allure.step("STEP 3: Click Set Tenant"):
        set_tenant_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Set Tenant')]"))
        )
        set_tenant_button.click()

    with allure.step("STEP 4: Wait for Home page"):
        wait.until(EC.url_contains("/home"))

    with allure.step("STEP 5: Click Sign In"):
        sign_in_button = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'sign')]"
            ))
        )
        sign_in_button.click()

    with allure.step("STEP 6: Wait for Login page"):
        wait.until(EC.url_contains("/login"))

    with allure.step("STEP 7: Enter login credentials"):
        email_input = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@type,'email')]"))
        )
        password_input = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@type,'password')]"))
        )
        email_input.send_keys("suchini@ateamsoftware.com")
        password_input.send_keys("Abc12345")

    with allure.step("STEP 8: Click Login"):
        login_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]"))
        )
        login_btn.click()

    with allure.step("STEP 9: Verify Dashboard loaded"):
        try:
            wait.until(EC.url_contains("/supplier/dashboard"))
            take_screenshot(driver, "dashboard_success")
            print("✅ Login successful")
        except:
            take_screenshot(driver, "dashboard_failed")
            pytest.fail("❌ Dashboard did not load after login")
