import pytest
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Global variables to store command-line args

def pytest_addoption(parser):
    parser.addoption("--username", action="store", help="Jenkins username")
    parser.addoption("--password", action="store", help="Jenkins password")
    parser.addoption("--controller", action="store", help="Controller name passed from Jenkins (e.g. sandbox, dev1, dev2)")

@pytest.fixture(scope="session")
def jenkins_username(pytestconfig):
    return pytestconfig.getoption("username")

@pytest.fixture(scope="session")
def jenkins_password(pytestconfig):
    return pytestconfig.getoption("password")

@pytest.fixture(scope="session")
def controller_url(pytestconfig):
    name = pytestconfig.getoption("controller")
    controller_map = {
        "sandbox":  "https://jenkins-sandbox.devops.broadridge.net",
        "dev2":     "https://jenkins-edw-dev2.devops.broadridge.net",
        "dev3":     "https://jc-dev3.devops.bfsaws.net",
        "csg":      "https://jc-csg.devops.bfsaws.net",
        "jabe":     "https://jc-jabe.devops.bfsaws.net",
        "ipe":      "https://jc-ipe.devops.bfsaws.net",
        "gptm":     "https://jc-gptm.devops.bfsaws.net",
        "epm":      "https://jc-epm.devops.bfsaws.net",
        # "jenkinsha":"https://jenkins.jenkinsha.ssprd.bfsaws.net",
        # "edwprod":  "https://jenkins-edw-prod.devops.broadridge.net",
        "tstdev2":  "https://jenkins-tstdev2.devops.broadridge.net",
    }

    if name not in controller_map:
        raise ValueError(f"Unknown controller: '{name}' — please check the spelling.")
    
    return controller_map[name]


@pytest.fixture(scope="session")
def debug():
    return True

@pytest.fixture(scope="session")
def logged_in_driver(jenkins_username, jenkins_password, controller_url, debug):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920,1080")

    # # comment the below 4 chrome options if u wanna run in local machine, uncomment it for pipeline
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        if "tstdev2" in controller_url:
            JENKINS_LOGIN_URL = "https://jenkins-tstoc.devops.broadridge.net/login"
        else:
            JENKINS_LOGIN_URL = "https://jenkins-oc.devops.broadridge.net/login"
        
        if debug:
            print("Launching Jenkins login...")

        driver.get(JENKINS_LOGIN_URL)
        wait = WebDriverWait(driver, 20)

        username_input = wait.until(EC.presence_of_element_located((By.NAME, "j_username")))
        username_input.clear()
        username_input.send_keys(jenkins_username)

        driver.find_element(By.NAME, "j_password").send_keys(jenkins_password)
        driver.find_element(By.NAME, "Submit").click()

        yield driver

    except Exception as e:
        print(f"Error during login: {e}")
        driver.quit()
        raise

    finally:
        driver.quit()

# -------------------------------
# HTML Report Customization Hooks
# -------------------------------

def pytest_html_results_table_header(cells):
    cells.insert(2, '<th>Link</th>')

def pytest_html_results_table_row(report, cells):
    link = getattr(report, 'report_link', None)
    if link:
        cells.insert(2, f'<td>{link}</td>')
    else:
        cells.insert(2, '<td>-</td>')

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.report_link = getattr(item, "report_link", None)

