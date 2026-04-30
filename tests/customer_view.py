import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random
import time

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
@allure.title("Tenant + Shuffled Featured Product Click")
def test_open_tenant_and_click_featured_product(driver):
    wait = WebDriverWait(driver, 25)

    # ---------------- OPEN TENANT PAGE ----------------
    driver.get(
        "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/webshopnotfound"
    )

    tenant_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
    )
    tenant_input.clear()
    tenant_input.send_keys("GrandRest")

    set_tenant_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Set Tenant')]"))
    )
    set_tenant_button.click()

    wait.until(EC.url_contains("/home"))
    print("✅ Tenant page loaded successfully!")

    # ---------------- WAIT FOR PAGE LOAD ----------------
    time.sleep(3)

    # ---------------- CLICK FEATURED PRODUCT (SHUFFLE) ----------------
    with allure.step("Click shuffled 'View' button from Featured Products"):

        view_buttons = wait.until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                "//button[contains(.,'View')]"
            ))
        )

        # Filter visible buttons
        visible_buttons = [btn for btn in view_buttons if btn.is_displayed()]

        print(f"🛒 Found {len(visible_buttons)} visible 'View' buttons")

        if not visible_buttons:
            raise Exception("❌ No visible View buttons found!")

        # Debug
        for btn in visible_buttons:
            print("👉 Button text:", btn.text)

        # 🔥 SHUFFLE instead of random.choice
        random.shuffle(visible_buttons)
        selected_button = visible_buttons[0]

        # Scroll
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            selected_button
        )

        time.sleep(1)

        # Click
        driver.execute_script("arguments[0].click();", selected_button)

        print("✅ Shuffled featured product clicked!")

    # ---------------- VALIDATION ----------------
    with allure.step("Validate navigation after click"):
        time.sleep(2)
        print("🌐 Current URL:", driver.current_url)