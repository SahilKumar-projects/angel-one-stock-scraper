
from selenium import webdriver


def create_driver():

    driver = webdriver.Chrome()

    driver.maximize_window()

    return driver