from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def login(driver, login_url, username, password):
    driver.get(login_url)
    driver.find_element(By.NAME, "j_username").send_keys(username)
    driver.find_element(By.NAME, "j_password").send_keys(password)
    driver.find_element(By.NAME, "Submit").click()

    time.sleep(3)

    return driver.current_url
