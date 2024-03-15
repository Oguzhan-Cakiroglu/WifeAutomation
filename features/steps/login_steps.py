import time

from pages.login_pages import LoginPage
from behave import given
from runner import RunDriver
from pages.login_pages import LoginPage



class LoginSteps:
    def __init__(self):
        self.runner = RunDriver()
        self.driver = self.runner.driver
        self.loginpage =LoginPage()
    @given('enter username')
    def login_username(self):
        self.loginpage = LoginPage()
        self.loginpage.enter_username()




