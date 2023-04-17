from behave import *
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), "test-image3.pdf")

@given(u'the third user is signed into their account')
def open_browser(context):
    context.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    context.driver.implicitly_wait(5)
    context.driver.get("http://127.0.0.1:5000/auth/login")
    username_field = context.driver.find_element(By.ID, "username")
    username_field.send_keys("user2")
    pass_field = context.driver.find_element(By.ID, "password")
    pass_field.send_keys("Password1@")
    token_field = context.driver.find_element(By.ID, "token")
    token_field.send_keys("111111")
    add_button = context.driver.find_element(By.ID, "submit")
    add_button.click()
    context.driver.implicitly_wait(100)

@when(u'the third user is on the "Edit Profile" page')
def step_impl(context):
    expected_url = "http://127.0.0.1:5000/auth/index"
    wait = WebDriverWait(context.driver, 10)
    try:
        wait.until(lambda driver: driver.current_url == expected_url)
    except TimeoutException:
        assert False, f"Page was not redirected to {expected_url}"
    context.driver.get("http://127.0.0.1:5000/edit_profile")

@when(u'the third user chooses a PDF file from their local storage')
def step_impl(context):
    upload_element = context.driver.find_element(By.ID, "profile_picture")
    upload_element.send_keys(UPLOADS_PATH)

@when(u'the third user enters the "Submit" button')
def step_impl(context):
    add_button = context.driver.find_element(By.ID, "submit")
    add_button.click()
    context.driver.implicitly_wait(100)

@then(u'the third user will an error message')
def step_impl(context):
    success_message = context.driver.find_element(By.CLASS_NAME, "help-block")
    expected_message = "Images only!"
    assert success_message.text == expected_message, f"Expected message: '{expected_message}', but got '{success_message.text}'"