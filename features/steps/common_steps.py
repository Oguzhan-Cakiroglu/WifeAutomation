from behave import given, when, then
from appium import webdriver
from common.base import Base
from locators.common_locators import CommonLocators
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

@when('User click on "{text}" button')
def step_click_on_button_with_text(context, text):
    context.base = Base(context.driver)
    context.commonlocators = CommonLocators()
    context.base.click_element(AppiumBy.XPATH, context.commonlocators.TEXT_XPATH.format(text))
