import time
from pages.PromoteArtifactPage import promote_artifact
import os
import pytest

@pytest.mark.sandbox
def test_promote_artifact(logged_in_driver, request, jenkins_username, jenkins_password):
    time.sleep(3)
    PROMOTE_ARTIFACT_JOB_URL = "https://jenkins-sandbox.devops.broadridge.net/job/PROMOTION/job/Promote_Artifact/"
    result = promote_artifact(logged_in_driver, jenkins_username, jenkins_password, PROMOTE_ARTIFACT_JOB_URL, debug=True)

    job_link = str(result.get("Job Link", "#"))
    # Inject job link in report
    request.node.report_link = f'<a href="{job_link}" target="_blank">Promote Artifact Job</a>'

    assert result["status"] == "success", f"Promote artifact job failed: {result}"
