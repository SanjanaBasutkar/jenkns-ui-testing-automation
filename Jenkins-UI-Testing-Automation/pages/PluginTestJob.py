from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time

def plugin_test_job(driver, job_url, debug = True):
    wait = WebDriverWait(driver, 120)
    driver.get(job_url)
    if debug:
        print("Reached plugin test job page")

    time.sleep(4)
    build_with_param_tab = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//a[span[@class="task-link-text" and text()="Build with Parameters"]]')))
    build_with_param_tab.click()
    if debug:
        print("Reached plugin test job build with parameters page")

    time.sleep(4)
    input_box = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jenkins-input")))
    input_box.clear()
    input_box.send_keys("dev")
    if debug:
        print("Filled 'dev' in environment box")

    checkbox = driver.find_element(By.CLASS_NAME, 'jenkins-checkbox')
    checkbox.click()
    if debug:
        print('Checkbox ticked')

    time.sleep(4)
    build_button = wait.until(EC.element_to_be_clickable((By.ID, "yui-gen1-button")))
    build_button.click()
    if debug:
        print("Build started")

    time.sleep(10)
    wait.until(EC.presence_of_element_located((By.ID, "buildHistory")))

    href_anchor_tag = driver.find_element(
        By.XPATH, '//*[@id="buildHistory"]/div[2]/table/tbody/tr[2]/td/div[1]/div[1]/a')
    href_value = href_anchor_tag.get_attribute("href")

    driver.get(href_value)
    if debug:
        print("Clicked build number successfully.")

    plugin_console_url = driver.current_url
    print('plugin console url : ',plugin_console_url)

    # console_output_tab = wait.until(EC.element_to_be_clickable(
    #     (By.XPATH, '//a[contains(@class, "task-link") and span[text()="Console Output"]]')))

    # console_output_tab = WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "task-link") and span[text()="Console Output"]]'))
    # )
    # ActionChains(driver).move_to_element(console_output_tab).perform()

    # Wait for tab to be present
    time.sleep(10)
    # print(driver.page_source)
    # driver.save_screenshot("before_click_console_output.png")
    
    console_output_tab = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "task-link") and span[text()="Console Output"]]'))
    )

    # Scroll into view (fix for headless mode)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", console_output_tab)

    # Hover over tab (some buttons require mouseover to activate)
    ActionChains(driver).move_to_element(console_output_tab).perform()

    # Wait for it to become clickable
    console_output_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "task-link") and span[text()="Console Output"]]'))
    )

    console_output_tab.click()
    print("clicked console output tab")

    try:
        WebDriverWait(driver, 300).until(
            lambda driver: "Finished:" in driver.find_element(By.CLASS_NAME, "console-output").text)
        if debug:
            print("Build finished detected in plugin console output.")
    except TimeoutException:
        print("Timeout: Plugin test job did not finish within expected time.")
        return False, "", href_value, ""

    try:
        starting_building_link = driver.find_element(
            By.XPATH, '//text()[contains(., "Starting building")]/following-sibling::a')
        downstream_url = starting_building_link.get_attribute("href")
        if debug:
            print("Captured downstream job URL:", downstream_url)

        driver.get(downstream_url)
        time.sleep(4)
        downstream_console_tab = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//a[contains(@class, "task-link") and span[text()="Console Output"]]')))
        downstream_console_tab.click()

        try:
            WebDriverWait(driver, 300).until(
                lambda driver: "Finished:" in driver.find_element(By.CLASS_NAME, "console-output").text)
            if debug:
                print("Downstream build finished detected in console output.")
        except TimeoutException:
            print("Timeout: Downstream job did not finish within expected time.")
            return False, "", href_value, downstream_url

        downstream_output = driver.find_element(By.CLASS_NAME, "console-output").text
        if debug:
            if "Finished: SUCCESS" in downstream_output:
                print("Downstream Job: SUCCESS")
            else:
                print("Downstream Job: FAILURE")

        driver.get(plugin_console_url)
        # console_output_tab = WebDriverWait(driver, 20).until(
        #     EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "task-link") and span[text()="Console Output"]]'))
        # )
        # ActionChains(driver).move_to_element(console_output_tab).perform()

        # Wait for tab to be present
        console_output_tab = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "task-link") and span[text()="Console Output"]]'))
        )

        # Scroll into view (fix for headless mode)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", console_output_tab)

        # Hover over tab (some buttons require mouseover to activate)
        ActionChains(driver).move_to_element(console_output_tab).perform()

        # Wait for it to become clickable
        console_output_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "task-link") and span[text()="Console Output"]]'))
        )

        console_output_tab.click()
        
        if debug:
            print("Returned to plugin test job console output page.")

    except Exception as e:
        print(f"Exception occurred while fetching downstream job link: {e}")
        return False, "", href_value, ""

    try:
        time.sleep(4)
        wait.until(lambda d: "Finished:" in d.find_element(By.CLASS_NAME, "console-output").text)
        output = driver.find_element(By.CLASS_NAME, "console-output").text
    except TimeoutException:
        print("Timeout: Plugin job console output not available after returning.")
        return False, "", href_value, downstream_url

    if "Finished: SUCCESS" in output:
        if debug:
            print("Plugin Test Job: SUCCESS")
        print('Plugin test Job URL : ',href_value)
        print('Downstream Job URL : ',downstream_url)
        return True, downstream_output, href_value, downstream_url
    else:
        if debug:
            print("Plugin Test Job: FAILURE")
        print('Plugin test Job URL : ',href_value)
        print('Downstream Job URL : ',downstream_url)
        return False, downstream_output, href_value, downstream_url

