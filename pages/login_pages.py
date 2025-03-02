# pages/login_pages.py
import time
from locators.login_locators import LoginpageLocators
from appium.webdriver.common.appiumby import By
from common.base import Base


class LoginPage(Base):
    def __init__(self, driver):
        self.driver = driver
        self.locators = LoginpageLocators()
        self.base =Base


    def enter_username(self):
        time.sleep(10)
        self.click_element(By.XPATH, self.locators.KESFET_TEXT_XPATH)
        time.sleep(10)

    def enter_google(self):
        self.base.open_web_page()
        time.sleep(10)