# features/environment.py
from appium import webdriver
from appium.options.android import UiAutomator2Options

def before_all(context):
    capabilities = {
        'platformName': 'Android',
        'automationName': 'UiAutomator2',
        'deviceName': 'Pixel_6_API_33',
        'appPackage': 'com.android.chrome',
        'appActivity': 'com.google.android.apps.chrome.Main',
        'noReset': True
    }
    
    options = UiAutomator2Options()
    options.load_capabilities(capabilities)
    
    # Appium 2.0 için doğru URL formatı
    appium_server_url = 'http://localhost:4723'
    context.driver = webdriver.Remote(command_executor=appium_server_url, options=options)

def after_all(context):
    if hasattr(context, 'driver'):
        context.driver.quit()
