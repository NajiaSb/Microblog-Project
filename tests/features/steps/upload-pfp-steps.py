from behave import *
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), "samplePic.jpg")

@given(u'the user is signed into their account')
def open_browser(context):
    context.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    context.driver.implicitly_wait(5)
    context.driver.get("http://127.0.0.1:5000/auth/login")
    title_field = context.driver.find_element(By.ID, "username")
    title_field.send_keys("testPfp")
    title_field = context.driver.find_element(By.ID, "password")
    title_field.send_keys("Password1@")
    add_button = context.driver.find_element(By.ID, "submit")
    add_button.click()
    context.driver.implicitly_wait(100)

@when(u'the user is on the "Edit Profile" page')
def step_impl(context):
    expected_url = "http://127.0.0.1:5000/index"
    wait = WebDriverWait(context.driver, 10)
    try:
        wait.until(lambda driver: driver.current_url == expected_url)
    except TimeoutException:
        assert False, f"Page was not redirected to {expected_url}"
    context.driver.get("http://127.0.0.1:5000/edit_profile")

@when(u'the user chooses a picture from their local storage')
def step_impl(context):
    upload_element = context.driver.find_element(By.ID, "profile_picture")
    upload_element.send_keys(UPLOADS_PATH)

@when(u'the user enters the "Submit" button')
def step_impl(context):
    add_button = context.driver.find_element(By.ID, "submit")
    add_button.click()
    context.driver.implicitly_wait(100)

@then(u'the user will get a sucess message')
def step_impl(context):
    success_message = context.driver.find_element(By.ID, "message")
    expected_message = "Your changes have been saved."
    assert success_message.text == expected_message, f"Expected message: '{expected_message}', but got '{success_message.text}'"