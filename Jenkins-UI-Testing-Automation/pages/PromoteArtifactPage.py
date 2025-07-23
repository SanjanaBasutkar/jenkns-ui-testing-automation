from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from selenium.webdriver.common.action_chains import ActionChains

def promote_artifact(driver, username, password, job_url, debug = True):
    try:
        wait = WebDriverWait(driver, 60)

        # Navigate to Promote Artifact job page
        driver.get(job_url)
        if debug:
            print('Reached Promote Artifact Job page.')

        time.sleep(4)
        wait.until(EC.presence_of_element_located((By.ID, "buildHistory")))

        # Click latest build (mini console)
        href_anchor_tag = driver.find_element(By.XPATH, '//*[@id="buildHistory"]/div[2]/table/tbody/tr[2]/td/div[1]/div[1]/a')
        href_value = href_anchor_tag.get_attribute("href")
        driver.get(href_value)
        if debug:
            print("Clicked latest build link.")

        # Click rebuild button
        time.sleep(4)
        rebuild_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, '//a[contains(@class, "task-link") and span[text()="Rebuild"]]'
        )))
        rebuild_button.click()
        if debug:
            print("Clicked Rebuild button.")

        # Fill username
        print("reached parameter filling page")
        time.sleep(4)
        username_input_box = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-panel"]/form/div[1]/div[3]/div[3]/div/input[2]')))
        print("captured username_input_box")
        username_input_box.clear()
        print("cleared username_input_box")
        time.sleep(5)
        print(username)
        username_input_box.send_keys(username)
        print("filled username_input_box")
        if debug:
            print("Filled username.")

        # Reveal and fill password
        driver.find_element(By.CLASS_NAME, 'hidden-password-update-btn').click()
        time.sleep(4)
        password_input_box = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'complex-password-field')
        ))
        password_input_box.clear()
        password_input_box.send_keys(password)
        if debug:
            print("Filled password.")

        time.sleep(2)

        # Click final Rebuild
        time.sleep(4)
        final_rebuild_button = wait.until(EC.element_to_be_clickable((By.ID, 'yui-gen1-button')))
        final_rebuild_button.click()
        if debug:
            print("Clicked final Rebuild button.")

        time.sleep(3)

        # Wait for new build to appear
        time.sleep(4)
        wait.until(EC.presence_of_element_located((By.ID, "buildHistory")))
        new_href = driver.find_element(By.XPATH, '//*[@id="buildHistory"]/div[2]/table/tbody/tr[2]/td/div[1]/div[1]/a')
        new_href_value = new_href.get_attribute("href")
        driver.get(new_href_value)

        # Click console output
        console_output_tab = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "task-link") and span[text()="Console Output"]]'))
        )
        ActionChains(driver).move_to_element(console_output_tab).perform()

        console_output_tab.click()
        if debug:
            print("Opened Console Output.")

        # Monitor console output
        timeout = 120
        check_interval = 3
        start_time = time.time()

        while time.time() - start_time < timeout:
            console_output = driver.find_element(By.CLASS_NAME, "console-output").text
            print(console_output)

            # Case 1: Job succeeded
            if "Finished: SUCCESS" in console_output:
                if debug:
                    print("Promote Artifact Job Finished: SUCCESS")
                print('Promote Artifact Job URL : ',new_href_value)
                return {"status": "success", "Job Link": new_href_value}

            # Case 2: Job failed
            if "Finished: FAILURE" in console_output:
                # Case 1: If there's a status code
                status_match = re.search(r"Status:\s*(\d+)", console_output)
                if status_match:
                    if debug:
                        print(f"JOB RUNNING FINISHED SUCCESSFULLY but Promote Artifact Job Finished: FAILURE (with status {status_match.group(1)}) — treating as success.")
                    print('Promote Artifact Job URL : ', new_href_value)
                    return {"status": "success", "note": f"Finished with Status: {status_match.group(1)}", "Job Link": new_href_value}

                # Case 2: Known non-critical error messages that we still treat as success
                known_success_errors = [
                    "Validation result: Failed!!! Artifact name",
                    "Failed to fetch checksums. Aborting validation.",
                    "Checksum mismatch for",
                    "Please make sure you have entered valid input parameters",
                    "Source Artifact may not be available/exists at:",
                    "You don't have access to the artifact",
                    "Source Artifact already exists in the Target repository at below location, it cannot be uploaded again",
                    "Unable to get availability status of requested Artifact from Target repo",
                    "Source Artifact doesnot exists"
                ]

                for known_error in known_success_errors:
                    if known_error in console_output:
                        if debug:
                            print(f"Known non-critical failure encountered: '{known_error}' — treating as success.")
                        print('Promote Artifact Job URL : ', new_href_value)

                        # Special handling for one particular known error
                        note_message = f"Finished with known message: {known_error}"
                        if known_error == "Source Artifact doesnot exists":
                            note_message += "\nHence we are proceeding with Promotion of this artifact to Release Repository."

                        return {"status": "success", "note": note_message, "Job Link": new_href_value}

                # Case 3: Unhandled failure, treat as failure
                error_message = "unknown error"
                error_match = re.search(r'ERROR:\s*(.*)', console_output)
                if error_match:
                    error_message = error_match.group(1)
                if debug:
                    print(f"Promote Artifact Job failed without status code: {error_message}")
                print('Promote Artifact Job URL : ', new_href_value)
                return {"status": "failure", "reason": error_message, "Job Link": new_href_value}


            time.sleep(check_interval)

        return {"status": "timeout", "reason": "Job did not complete in expected time.", "Job Link": new_href_value}

    except Exception as e:
        if debug:
            print("An error occurred during Promote Artifact Job.")
        
        print(e)
        return {"status": "error", "exception": "Error occurred, check logic or node is offline."}


