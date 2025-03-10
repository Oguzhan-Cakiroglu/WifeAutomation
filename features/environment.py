# features/environment.py
from appium import webdriver as appium_webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selenium import webdriver as selenium_webdriver

def before_all(context):
    """ Runner'dan gelen platformları al ve uygun driver'ı başlat. """
    platform = context.config.userdata.get('platform', 'android')  # Varsayılan Android
    context.drivers = {}  # Birden fazla driver'ı desteklemek için
    context.driver = None  # Varsayılan olarak driver None

    if 'safari' in platform:
        try:
            safari_driver = selenium_webdriver.Safari()
            context.drivers['safari'] = safari_driver
            context.driver = safari_driver  # Tüm testlerde kullanılabilecek driver
            print("✅ Safari WebDriver başlatıldı.")
        except Exception as e:
            print(f"❌ Safari WebDriver başlatılamadı: {e}")
            raise

    if 'android' in platform:
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

        appium_server_url = 'http://localhost:4723'
        try:
            android_driver = appium_webdriver.Remote(command_executor=appium_server_url, options=options)
            context.drivers['android'] = android_driver
            if context.driver is None:
                context.driver = android_driver
            print("✅ Appium Android driver başlatıldı.")
        except Exception as e:
            print(f"❌ Android driver başlatılamadı: {e}")
            raise

    if 'ios' in platform:
        capabilities = {
    'platformName': 'iOS',
    'automationName': 'XCUITest',
    'deviceName': 'iPhone 16 Pro',  # Cihaz modelinizin adı
    'platformVersion': '18.2',  # iOS versiyonunuz
    'udid': 'A6DC6B16-68CA-433A-80F0-8E5C62D65253',  # Cihazınızın UDID'si
    'browserName': 'Safari',
    'noReset': True
        }

        options = XCUITestOptions()
        options.load_capabilities(capabilities)

        appium_server_url = 'http://localhost:4724'
        try:
            ios_driver = appium_webdriver.Remote(command_executor=appium_server_url, options=options)
            context.drivers['ios'] = ios_driver
            if context.driver is None:
                context.driver = ios_driver
            print("✅ Appium iOS driver başlatıldı.")
        except Exception as e:
            print(f"❌ iOS driver başlatılamadı: {e}")
            raise

    if not context.drivers:
        raise ValueError(f"❌ Bilinmeyen platform: {platform}")

def after_all(context):
    """ Testler bitince tüm driver'ları kapat. """
    for platform, driver in context.drivers.items():
        if driver:
            driver.quit()
            print(f"🚪 {platform.upper()} driver kapatıldı.")