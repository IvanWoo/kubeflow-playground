import json
import kfp

from kubeflow_playground.auth import get_istio_auth_session

KUBEFLOW_ENDPOINT = "http://localhost:8080"
KUBEFLOW_USERNAME = "user@example.com"
KUBEFLOW_PASSWORD = "12341234"

auth_session = get_istio_auth_session(
    url=KUBEFLOW_ENDPOINT, username=KUBEFLOW_USERNAME, password=KUBEFLOW_PASSWORD
)

client = kfp.Client(
    host=f"{KUBEFLOW_ENDPOINT}/pipeline", cookies=auth_session["session_cookie"]
)
pipelines = client.list_pipelines()
out = json.dumps(pipelines.to_dict()["pipelines"], indent=4, default=str)
print(out)
