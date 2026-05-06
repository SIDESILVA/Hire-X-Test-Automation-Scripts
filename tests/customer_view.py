import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
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


# -------------------- HELPER --------------------
def set_input(driver, element, value):
    driver.execute_script("""
        arguments[0].focus();
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
    """, element, value)


# -------------------- ADDRESS HELPER (FINAL FIXED) --------------------
def fill_address_block(driver, address_block, wait, prefix="Test"):
    inputs = address_block.find_elements(By.XPATH, ".//input")
    selects = address_block.find_elements(By.XPATH, ".//select")

    visible_inputs = [i for i in inputs if i.is_displayed()]
    visible_selects = [s for s in selects if s.is_displayed()]

    # -------- AUTOCOMPLETE (optional but useful) --------
    try:
        visible_inputs[0].send_keys("Colombo")
        time.sleep(1)
        visible_inputs[0].send_keys(Keys.ARROW_DOWN, Keys.ENTER)
    except:
        pass

    # -------- TEXT INPUTS --------
    if len(visible_inputs) > 1:
        set_input(driver, visible_inputs[1], f"{prefix} Street")

    if len(visible_inputs) > 2:
        set_input(driver, visible_inputs[2], f"{prefix} Line 2")

    if len(visible_inputs) > 3:
        set_input(driver, visible_inputs[3], "Colombo")

    if len(visible_inputs) > 4:
        set_input(driver, visible_inputs[4], "10000")

    # -------- IDENTIFY DROPDOWNS --------
    country_select = None
    state_select = None

    for s in visible_selects:
        attr = (s.get_attribute("autocomplete") or "").lower()

        if "country" in attr:
            country_select = s
        else:
            state_select = s

    # -------- STEP 1: SELECT COUNTRY --------
    if country_select:
        try:
            select = Select(country_select)
            select.select_by_value("AU")
            print("🌍 Country selected")
        except:
            pass

    # -------- WAIT FOR STATE TO LOAD --------
    time.sleep(1)

    # -------- STEP 2: SELECT STATE --------
    if state_select:
        try:
            select = Select(state_select)

            wait.until(lambda d: len(select.options) > 1)

            select.select_by_index(1)
            print("📍 State selected")
        except:
            pass


# -------------------- Test Case --------------------
@allure.title("Tenant + Full Booking Flow with Correct Address Handling")
def test_open_tenant_and_click_featured_product(driver):
    wait = WebDriverWait(driver, 25)

    # ---------------- OPEN TENANT PAGE ----------------
    driver.get("https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/webshopnotfound")

    tenant_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
    tenant_input.clear()
    tenant_input.send_keys("GrandRest")

    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Set Tenant')]"))).click()
    wait.until(EC.url_contains("/home"))

    print("✅ Tenant page loaded successfully!")
    time.sleep(2)

    # ---------------- CLICK PRODUCT ----------------
    buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(.,'View')]")))
    visible = [b for b in buttons if b.is_displayed()]
    random.shuffle(visible)

    driver.execute_script("arguments[0].click();", visible[0])
    print("✅ Product clicked")

    time.sleep(2)

    # ---------------- SET DATE ----------------
    end_date = wait.until(EC.element_to_be_clickable((By.NAME, "hireEndDate")))
    tomorrow = datetime.now() + timedelta(days=1)
    set_input(driver, end_date, tomorrow.strftime("%d/%m/%Y"))

    driver.find_element(By.TAG_NAME, "body").click()

    # ---------------- QUANTITY ----------------
    qty = wait.until(EC.element_to_be_clickable((By.NAME, "Quantity")))
    qty.clear()
    qty.send_keys("3")

    # ---------------- REQUEST ----------------
    request_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Request to Book')]")))
    driver.execute_script("arguments[0].click();", request_btn)

    # ---------------- DELIVERY METHOD ----------------
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "spinner-wrapper")))

    dropdown = wait.until(EC.element_to_be_clickable((By.NAME, "shippingMethod")))
    select = Select(dropdown)

    option = random.choice(select.options[1:])
    select.select_by_visible_text(option.text)

    print("🚚 Selected:", option.text)

    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "spinner-wrapper")))
    time.sleep(2)

    # ---------------- CUSTOMER DETAILS ----------------
    email = f"test_{datetime.now().strftime('%Y%m%d%H%M%S')}@mail.com"
    phone = f"077{random.randint(1000000,9999999)}"

    set_input(driver, next(i for i in driver.find_elements(By.NAME, "emailAddress") if i.is_displayed()), email)
    set_input(driver, next(i for i in driver.find_elements(By.NAME, "phoneNumber") if i.is_displayed()), phone)
    set_input(driver, next(i for i in driver.find_elements(By.NAME, "firstName") if i.is_displayed()), "Test")
    set_input(driver, next(i for i in driver.find_elements(By.NAME, "lastName") if i.is_displayed()), "User")

    print("✅ Customer details filled")

    # ---------------- ADDRESS HANDLING ----------------
    with allure.step("Fill addresses correctly"):

        blocks = driver.find_elements(By.XPATH, "//address-input")
        visible_blocks = [b for b in blocks if b.is_displayed()]

        print(f"📦 Address blocks: {len(visible_blocks)}")

        # Pickup
        if len(visible_blocks) == 1:
            fill_address_block(driver, visible_blocks[0], wait, "Pickup")

        # Delivery
        elif len(visible_blocks) >= 2:
            try:
                checkbox = driver.find_element(By.NAME, "hasCustomerAndDeliveryAddressSame")
                if checkbox.is_selected():
                    driver.execute_script("arguments[0].click();", checkbox)
                    time.sleep(1)
            except:
                pass

            fill_address_block(driver, visible_blocks[0], wait, "Customer")
            fill_address_block(driver, visible_blocks[1], wait, "Delivery")

        else:
            print("⚠️ No address blocks found")
    
    # ---------------- CLICK NEXT BUTTON ----------------
    with allure.step("Click Next button"):

        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next')]"))
        )

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", next_button)
        time.sleep(1)

        driver.execute_script("arguments[0].click();", next_button)

        print("➡️ Clicked Next button")

        # Wait for next step (Order Summary page)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//h5[contains(text(),'Order Summary')]"))
        )

        print("✅ Navigated to Order Summary")
    
    # ---------------- ACCEPT TERMS CHECKBOX ----------------
    with allure.step("Accept Terms and Conditions"):

        checkbox = wait.until(
            EC.presence_of_element_located((By.NAME, "hasAgreedTermsAndConditions"))
        )

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", checkbox)
        time.sleep(1)

        # Click only if not already selected
        if not checkbox.is_selected():
            driver.execute_script("arguments[0].click();", checkbox)

        print("✅ Terms & Conditions accepted")

    # ---------------- FINAL REQUEST BOOKING ----------------
    with allure.step("Click Final Request Booking"):

        # Wait until button appears in summary step
        buttons = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(.,'Request Booking')]"))
        )

        # Get ONLY visible button (important)
        final_button = next(btn for btn in buttons if btn.is_displayed())

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            final_button
        )

        time.sleep(1)

        driver.execute_script("arguments[0].click();", final_button)

        print("✅ Final 'Request Booking' clicked!")

    # ---------------- CLOSE MODAL ----------------
    with allure.step("Close confirmation modal"):

        # Wait for modal to appear
        wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "modal-footer"))
        )

        # Get all Close buttons
        close_buttons = driver.find_elements(
            By.XPATH, "//div[contains(@class,'modal-footer')]//button[contains(.,'Close')]"
        )

        # Pick visible one
        close_button = next(btn for btn in close_buttons if btn.is_displayed())

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            close_button
        )

        time.sleep(1)

        driver.execute_script("arguments[0].click();", close_button)

        print("✅ Modal closed successfully!")

    # ---------------- FINAL ----------------
    print("🌐 Current URL:", driver.current_url)