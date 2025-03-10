from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@given('Safari tarayıcısı açık')
def step_impl(context):
    assert context.driver is not None, "Safari WebDriver başlatılamadı!"
    context.driver.get("https://www.google.com")  # Safari'yi aç ve Google'a git

@when('web adresine gidilir')
def step_impl(context):
    context.driver.get("https://www.apple.com")
    WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))