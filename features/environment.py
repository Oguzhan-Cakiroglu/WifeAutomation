# features/environment.py
from appium import webdriver as appium_webdriver
from appium.options.android import UiAutomator2Options
from selenium import webdriver as selenium_webdriver

def before_all(context):
    # Runner'dan gelen platformu al
    platform = context.config.userdata.get('platform', 'android')  # Varsayılan olarak android

    if platform == 'safari':
        # Safari için Selenium WebDriver
        try:
            context.driver = selenium_webdriver.Safari()
            print("Safari driver başlatıldı.")
        except Exception as e:
            print(f"Safari driver başlatılamadı: {e}")
            raise
    elif platform == 'android':
        # Android için Appium driver
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
            context.driver = appium_webdriver.Remote(command_executor=appium_server_url, options=options)
            print("Appium driver Android için başlatıldı.")
        except Exception as e:
            print(f"Appium driver başlatılamadı: {e}")
            raise
    else:
        raise ValueError(f"Bilinmeyen platform: {platform}")

def after_all(context):
    if hasattr(context, 'driver'):
        context.driver.quit()
        print("Driver kapatıldı.")