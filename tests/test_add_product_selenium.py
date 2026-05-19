from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:5500/frontend/pages"

USERNAME = "asd123"
PASSWORD = "Test1234"
ROLE = "admin"

CHROMEDRIVER_PATH = str(Path(__file__).resolve().parent.parent / "drivers" / "chromedriver.exe")


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")  # uncomment if needed

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def click_first(driver, wait, locators):
    for by, value in locators:
        try:
            return wait.until(EC.element_to_be_clickable((by, value)))
        except Exception:
            pass
    raise Exception(f"None of the locators worked: {locators}")


def fill_first(driver, locators, text):
    for by, value in locators:
        elements = driver.find_elements(by, value)
        if elements:
            elements[0].clear()
            elements[0].send_keys(text)
            return True
    raise Exception(f"Could not find input for locators: {locators}")


def test_login_dashboard_products_add_product(driver):
    wait = WebDriverWait(driver, 15)

    # 1) Open login page
    driver.get(f"{BASE_URL}/login.html")

    # 2) Select role
    if ROLE.lower() == "admin":
        wait.until(EC.element_to_be_clickable((By.ID, "roleAdmin"))).click()
    else:
        wait.until(EC.element_to_be_clickable((By.ID, "roleEmployee"))).click()

    # 3) Fill login
    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)

    # 4) Click login
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    # 5) Wait for dashboard redirect
    wait.until(lambda d: "dashboard" in d.current_url.lower() or "dashboard" in d.page_source.lower())

    # 6) Go to Products page
    driver.get(f"{BASE_URL}/products.html")

    # 7) Click Add Product button/link
    add_product_button = click_first(
        driver,
        wait,
        [
            (By.LINK_TEXT, "Add Product"),
            (By.PARTIAL_LINK_TEXT, "Add Product"),
            (By.XPATH, "//a[contains(., 'Add Product')]"),
            (By.XPATH, "//button[contains(., 'Add Product')]"),
        ],
    )
    add_product_button.click()

    # 8) Wait for add-product page
    wait.until(lambda d: "add-product" in d.current_url.lower() or "add product" in d.page_source.lower())

    # 9) Fill product form
    fill_first(driver, [(By.ID, "name"), (By.NAME, "name"), (By.ID, "productName"), (By.NAME, "productName")], "Test Product")
    fill_first(driver, [(By.ID, "category"), (By.NAME, "category")], "Electronics")
    fill_first(driver, [(By.ID, "quantity"), (By.NAME, "quantity")], "10")
    fill_first(driver, [(By.ID, "price"), (By.NAME, "price")], "99.99")
    fill_first(driver, [(By.ID, "supplier_id"), (By.NAME, "supplier_id"), (By.ID, "supplierId"), (By.NAME, "supplierId")], "1")

    # 10) Submit form
    submit_btn = click_first(
        driver,
        wait,
        [
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.XPATH, "//button[contains(., 'Save')]"),
            (By.XPATH, "//button[contains(., 'Add')]"),
            (By.XPATH, "//input[@type='submit']"),
        ],
    )
    submit_btn.click()

    # 11) Verify success
    wait.until(lambda d: "success" in d.page_source.lower() or "added" in d.page_source.lower() or "created" in d.page_source.lower())
    assert any(word in driver.page_source.lower() for word in ["success", "added", "created"])