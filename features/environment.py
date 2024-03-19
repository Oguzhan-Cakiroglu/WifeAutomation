# features/environment.py
from appium import webdriver
from appium.options.android import UiAutomator2Options

def before_all(context):
    capabilities = {
        'platformName': 'Android',
        'automationName': 'uiautomator2',
        'deviceName': 'Android',
        'appPackage': 'com.divan.life.test',
        'appActivity': 'com.divan.life.test.MainActivity',
    }
    appium_server_url = 'http://localhost:4723'
    context.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

def after_all(context):
    context.driver.quit()
