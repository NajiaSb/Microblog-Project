from behave import *
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

@given(u'the third user is on the Registration page')
def open_browser(context):
    context.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    context.driver.implicitly_wait(5)
    context.driver.get("http://127.0.0.1:5001/auth/register")

@when('the third user enters "{username}" in the username field')
def step_impl(context, username):
    title_field = context.driver.find_element(By.ID, "username")
    title_field.send_keys(username)

@when('the third user enters "{email}" in the email field')
def step_impl(context, email):
    title_field = context.driver.find_element(By.ID, "email")
    title_field.send_keys(email)

@when('the third user enters "{password}" in the password field')
def step_impl(context, password):
    title_field = context.driver.find_element(By.ID, "password")
    title_field.send_keys(password)

@when('the third user enters "{password2}" in the repeat password field')
def step_impl(context, password2):
    title_field = context.driver.find_element(By.ID, "password2")
    title_field.send_keys(password2)

@when(u'the third user clicks the "Submit" button')
def step_impl(context):
    add_button = context.driver.find_element(By.ID, "submit")
    add_button.click()
    context.driver.implicitly_wait(5)

@then('the third user will get a message error stating criteria of password')
def step_impl(context):
    context.driver.implicitly_wait(5)
    status = context.driver.find_element(By.CLASS_NAME, "help-block").is_displayed()
    assert status is True


