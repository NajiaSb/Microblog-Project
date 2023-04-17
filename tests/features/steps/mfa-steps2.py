from behave import *
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

@given(u'the second mfa user is on the login page')
def open_browser(context):
    context.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    context.driver.implicitly_wait(5)
    context.driver.get("http://127.0.0.1:5000/auth/login")

@when('the second mfa user enters {username} in the username field')
def step_impl(context, username):
    title_field = context.driver.find_element(By.ID, "username")
    title_field.send_keys(username)

@when('the second mfa user enters {password} in the password field')
def step_impl(context, password):
    title_field = context.driver.find_element(By.ID, "password")
    title_field.send_keys(password)

@when('the second mfa user enters {token} in the token field')
def step_impl(context, token):
    title_field = context.driver.find_element(By.ID, "token")
    title_field.send_keys(token)

@when(u'the second mfa user clicks the "Sign in" button')
def step_impl(context):
    add_button = context.driver.find_element(By.ID, "submit")
    add_button.click()
    context.driver.implicitly_wait(5)

@then('the second mfa user gets an error message')
def step_impl(context):
    success_message = context.driver.find_element(By.ID, "message")
    expected_message = "Invalid username, password or token."
    assert success_message.text == expected_message, f"Expected message: '{expected_message}', but got '{success_message.text}'"

