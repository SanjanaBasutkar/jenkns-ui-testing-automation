import pytest
from selenium.webdriver.common.by import By
import time

@pytest.mark.all
def test_plugin_manager_failed_to_load(logged_in_driver, request, controller_url, debug=True):
    plugin_url = f"{controller_url}/pluginManager/installed"
    logged_in_driver.get(plugin_url)

    if debug:
        print(f"Checking plugin manager page for 'Failed to load' errors on: {plugin_url}")

    time.sleep(5)
    error_found = False
    alerts = logged_in_driver.find_elements(By.CLASS_NAME, "alert-danger")

    for alert in alerts:
        alert_text = alert.text.strip()

        if "Failed to load" in alert_text:
            error_found = True

            # Extract and print everything after "Failed to load:"
            parts = alert_text.split("Failed to load", 1)
            if len(parts) > 1:
                message = parts[1].strip(":").strip()
                print(f"Plugin Load Error Detected: {message}")
            else:
                print("Plugin Load Error Detected.")


    # Add Plugin Manager page link to HTML report
    request.node.report_link = f'<a href="{plugin_url}" target="_blank">Plugin Manager Page</a>'
    
    if error_found == False:
        print(f"Installed plugins are loading successfully.")

    assert not error_found, f"'Failed to load' error found in Plugin Manager at: {plugin_url}"

