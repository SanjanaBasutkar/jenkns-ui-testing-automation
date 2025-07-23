from pages.LoginPage import login
import pytest

@pytest.mark.all
def test_login(logged_in_driver, debug, jenkins_username, request):
    current_url = logged_in_driver.current_url

    if "loginError" in current_url:
        if debug:
            print("Login failed.")
    else:
        if debug:
            print(f"Login successful for user: {jenkins_username}")

    # Inject username in "Link" column of HTML report
    request.node.report_link = f"User: {jenkins_username}"

    assert "loginError" not in current_url, "Login failed"
