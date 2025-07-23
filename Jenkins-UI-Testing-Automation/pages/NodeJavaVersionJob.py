from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time

def node_java_job(driver, job_url, debug = True):
    wait = WebDriverWait(driver, 60)
    driver.get(job_url)
    if debug:
        print("Reached Node Java Version job page")
    
    time.sleep(4)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "task-link")))
    build_now_tab = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//a[span[@class="task-link-text" and text()="Build Now"]]')))
    build_now_tab.click()
    if debug:
        print("Clicked on Build Now")

    time.sleep(4)
    wait.until(EC.presence_of_element_located((By.ID, "buildHistory")))

    href_anchor_tag = driver.find_element(By.XPATH, '//*[@id="buildHistory"]/div[2]/table/tbody/tr[2]/td/div[1]/div[1]/a')
    href_value = href_anchor_tag.get_attribute("href")

    driver.get(href_value)
    if debug:
        print("Clicked mini console button successfully.")

    console_output_tab = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "task-link") and span[text()="Console Output"]]'))
    )
    ActionChains(driver).move_to_element(console_output_tab).perform()

    console_output_tab.click()

    try:
        time.sleep(4)
        wait.until(
            lambda d: "Finished:" in d.find_element(By.CLASS_NAME, "console-output").text
        )
        output = driver.find_element(By.CLASS_NAME, "console-output").text
        if "Finished: SUCCESS" in output:
            if debug:
                print("Node Java Version Job completed successfully!")
            print('Node Java Version Job URL : ',href_value)
            return True, href_value
        else:
            print('Node Java Version Job URL : ',href_value)
            return False, href_value
    except TimeoutException:
        print("Timeout: Build did not finish within 2 minutes.")
        return False, href_value

