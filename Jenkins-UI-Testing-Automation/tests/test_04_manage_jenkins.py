import pytest
from selenium.webdriver.common.by import By
import time

@pytest.mark.all
def test_manage_page_alert_check(logged_in_driver, request, controller_url, debug = True):
    manage_url = f"{controller_url}/manage"
    logged_in_driver.get(manage_url)

    if debug:
        print(f"Checking manage page for alert-danger blocks on: {manage_url}")

    time.sleep(5)

    found_unexpected_alert = False
    alerts = logged_in_driver.find_elements(By.CLASS_NAME, "alert-danger")

    for alert in alerts:
        try:
            if alert.get_attribute("id") != "redirect-error":
                found_unexpected_alert = True
                if debug:
                    print(f"Some plugins could not be loaded due to unsatisfied dependencies. Fix these issues and restart Jenkins to re-enable these plugins.")
                break
        except Exception:
            continue

    # Add the /manage page link to the HTML report
    request.node.report_link = f'<a href="{manage_url}" target="_blank">Manage Page</a>'

    if found_unexpected_alert == False:
        print(f"There is no alert in manage jenkins page, everything is fine here.")

    assert not found_unexpected_alert, f"Unexpected alert-danger block found on {manage_url}"

