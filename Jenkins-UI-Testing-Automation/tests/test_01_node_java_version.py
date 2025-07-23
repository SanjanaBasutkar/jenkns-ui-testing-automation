import time
from pages.NodeJavaVersionJobPage import node_java_job
import pytest

@pytest.mark.all
def test_node_java_version(logged_in_driver, debug, request, controller_url):
    time.sleep(3)
    NODE_JAVA_VERSION_JOB_URL = f"{controller_url}/job/DEVOPS/job/ADMIN/job/Node_Java_version/"
    # NODE_JAVA_VERSION_JOB_URL = "https://jenkins-sandbox.devops.broadridge.net/job/DEVOPS/job/ADMIN/job/Node_Java_version/"
    result, href_value = node_java_job(logged_in_driver, NODE_JAVA_VERSION_JOB_URL, debug)

     # Inject job link in report
    request.node.report_link = f'<a href="{href_value}" target="_blank">Node Java version Job</a>'

    assert result, f"Node Java version job failed. Job link: {href_value}"

