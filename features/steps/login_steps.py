# features/steps/login_steps.py
from behave import given
from pages.login_pages import LoginPage

@given('User open Divan app')
def login_username(context):
    login_page = LoginPage(context.driver)
    login_page.enter_username()
