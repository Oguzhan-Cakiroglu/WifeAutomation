# features/steps/web_login.py
from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

@given('Web Safari Uygulaması baslatilir')
def step_web_safari_open(context):
    assert context.driver is not None, "Safari driver başlatılamadı!"
    context.wait = WebDriverWait(context.driver, 10)

@when('Safari Google.com adresine gidilir')
def safari_web_open(context):
    context.driver.get("https://www.google.com")
    assert "Google" in context.driver.title, "Google sayfası yüklenemedi!"
    time.sleep(3)  # 3 saniye bekle, böylece tarayıcı hemen kapanmaz