from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@given('Chrome tarayıcısı açık')
def step_impl(context):
    assert context.driver is not None

@when('Google.com adresine gidilir')
def step_impl(context):
    context.driver.get('https://www.google.com')

@when('Python.org adresine gidilir')
def step_impl(context):
    context.driver.get('https://www.python.org')