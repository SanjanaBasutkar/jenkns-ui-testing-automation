import time
from pages.PluginTestJobPage import plugin_test_job
import pytest

@pytest.mark.all
def test_plugin_test_job(logged_in_driver, debug, request, controller_url):
    time.sleep(3)

    # for all controllers except csg, sandbox ( coz they have diff file structure ) and prod controllers
    PLUGIN_TEST_JOB_URL = f"{controller_url}/job/DEVOPS/job/ADMIN/job/Plugin_Test/"
    # PLUGIN_TEST_JOB_URL = "https://jenkins-sandbox.devops.broadridge.net/job/ADMIN/job/Plugin_Test/"

    # for sandbox 
    if controller_url == "https://jenkins-sandbox.devops.broadridge.net":
        PLUGIN_TEST_JOB_URL = "https://jenkins-sandbox.devops.broadridge.net/job/ADMIN/job/Plugin_Test/"

    # for csg controller
    if controller_url == "https://jc-csg.devops.bfsaws.net":
        PLUGIN_TEST_JOB_URL = "https://jc-csg.devops.bfsaws.net/job/internal/job/Plugin_Test/"

    success, downstream_output, href_value, downstream_url = plugin_test_job(logged_in_driver, PLUGIN_TEST_JOB_URL, debug)

    # Inject both job links into report
    request.node.report_link = f'<a href="{href_value}" target="_blank">Main Job</a> | <a href="{downstream_url}" target="_blank">Downstream Job</a>'

    assert success, f"Plugin test job failed. Downstream output: {downstream_output}. URL: {href_value}"

