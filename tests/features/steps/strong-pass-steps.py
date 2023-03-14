from behave import *
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

@given(u'the first user is on the Registration page')
def open_browser(context):
    context.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    context.driver.implicitly_wait(5)
    context.driver.get("http://127.0.0.1:5000/auth/register")

@when('the first user enters "{username}" in the username field')
def step_impl(context, username):
    title_field = context.driver.find_element(By.ID, "username")
    title_field.send_keys(username)

@when('the first user enters "{email}" in the email field')
def step_impl(context, email):
    title_field = context.driver.find_element(By.ID, "email")
    title_field.send_keys(email)

@when('the first user enters "{password}" in the password field')
def step_impl(context, password):
    title_field = context.driver.find_element(By.ID, "password")
    title_field.send_keys(password)

@when('the first user enters "{password2}" in the repeat password field')
def step_impl(context, password2):
    title_field = context.driver.find_element(By.ID, "password2")
    title_field.send_keys(password2)

@when(u'the first user clicks the "Submit" button')
def step_impl(context):
    add_button = context.driver.find_element(By.ID, "submit")
    add_button.click()
    context.driver.implicitly_wait(5)


@then('the first user is redirected to mfa page')
def step_impl(context):
    expected_url = "http://127.0.0.1:5000/auth/twofactor"
    wait = WebDriverWait(context.driver, 10)
    try:
        wait.until(lambda driver: driver.current_url == expected_url)
    except TimeoutException:
        assert False, f"Page was not redirected to {expected_url}"


