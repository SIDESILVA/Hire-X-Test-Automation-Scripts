import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random
import time
from datetime import datetime, timedelta


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
@allure.title("Tenant + Shuffled Featured Product Click + Full Flow")
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

    time.sleep(3)

    # ---------------- CLICK FEATURED PRODUCT ----------------
    with allure.step("Click shuffled 'View' button from Featured Products"):

        view_buttons = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(.,'View')]"))
        )

        visible_buttons = [btn for btn in view_buttons if btn.is_displayed()]

        print(f"🛒 Found {len(visible_buttons)} visible 'View' buttons")

        if not visible_buttons:
            raise Exception("❌ No visible View buttons found!")

        random.shuffle(visible_buttons)
        selected_button = visible_buttons[0]

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            selected_button
        )

        time.sleep(1)

        driver.execute_script("arguments[0].click();", selected_button)

        print("✅ Shuffled featured product clicked!")

    time.sleep(3)

    # ---------------- SET END DATE ----------------
    with allure.step("Set End Date to tomorrow"):

        end_date_input = wait.until(
            EC.element_to_be_clickable((By.NAME, "hireEndDate"))
        )

        tomorrow = datetime.now() + timedelta(days=1)
        formatted_date = tomorrow.strftime("%d/%m/%Y")

        print("📅 Setting End Date:", formatted_date)

        end_date_input.click()
        time.sleep(1)

        driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, end_date_input, formatted_date)

        driver.find_element(By.TAG_NAME, "body").click()

        print("✅ End Date set successfully!")

    # ---------------- SET QUANTITY ----------------
    with allure.step("Set Quantity to 3"):

        quantity_input = wait.until(
            EC.element_to_be_clickable((By.NAME, "Quantity"))
        )

        quantity_input.clear()
        quantity_input.send_keys("3")

        print("🔢 Quantity set to 3")

    # ---------------- REQUEST TO BOOK ----------------
    with allure.step("Click 'Request to Book' button"):

        request_button = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[@type='submit' and contains(.,'Request to Book')]"
            ))
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            request_button
        )

        time.sleep(1)

        driver.execute_script("arguments[0].click();", request_button)

        print("✅ 'Request to Book' button clicked!")

    # ---------------- DELIVERY METHOD ----------------
    with allure.step("Select random delivery method"):

        wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "spinner-wrapper"))
        )

        delivery_dropdown = wait.until(
            EC.element_to_be_clickable((By.NAME, "shippingMethod"))
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            delivery_dropdown
        )

        time.sleep(1)

        select = Select(delivery_dropdown)
        options = select.options[1:]

        print(f"🚚 Available delivery methods: {[opt.text for opt in options]}")

        if not options:
            raise Exception("❌ No delivery options available!")

        random_option = random.choice(options)

        print(f"🎯 Selected delivery method: {random_option.text}")

        select.select_by_visible_text(random_option.text)

        print("✅ Delivery method selected!")

    # ---------------- EMAIL (FIXED - NO CLICK ISSUE) ----------------
    if "Request a quote for delivery" in random_option.text:

        with allure.step("Fill email for quote delivery"):

            unique_email = f"testuser_{datetime.now().strftime('%Y%m%d%H%M%S%f')}@example.com"
            print("📧 Generated Email:", unique_email)

            # 🔥 IMPORTANT: wait until spinner disappears
            wait.until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "spinner-wrapper"))
            )

            email_input = wait.until(
                EC.visibility_of_element_located((By.NAME, "emailAddress"))
            )

            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                email_input
            )

            time.sleep(0.5)

            # Safe click (JS avoids overlay issue)
            driver.execute_script("arguments[0].click();", email_input)

            # Clear + set value properly for Angular
            driver.execute_script("""
                arguments[0].value = '';
            """, email_input)

            driver.execute_script("""
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
            """, email_input, unique_email)

            print("✅ Email entered successfully!")

    # ---------------- FINAL ----------------
    with allure.step("Final validation"):
        time.sleep(2)
        print("🌐 Current URL:", driver.current_url)