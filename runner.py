import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
import behave.__main__

capabilities = {
    'platformName': 'Android',
    'automationName': 'uiautomator2',
    'deviceName': 'Android',
    'appPackage': 'com.tokenflexapp.test',
    'appActivity': 'com.tokenflexapp.MainActivity',
}

appium_server_url = 'http://localhost:4723'

class RunDriver(unittest.TestCase):
    driver =None
    def setUp(self):
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
    def tearDown(self):
        if self.driver:
            self.driver.quit()
    def test_test_runner_divanApp(self):
        divan_tag = '@mainDivan'
        divan_features_path = "./features/"
        login_feature = "login.feature"
        options = f"--tags={divan_tag} {divan_features_path}{login_feature}"
        print('running divanApp')
        behave.__main__.main(options.split())

if __name__ == '__main__':
    unittest.main()
