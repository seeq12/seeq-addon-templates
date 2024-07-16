from requests import Session
from seeq import sdk, spy
import json
from requests.adapters import HTTPAdapter, Retry
from ..session import get_project_id_from_name


class DataLabFunctionSession(Session):
    def __init__(self, base_url, username, password, project_name):
        max_request_retries = 5
        request_retry_status_list = [502, 503, 504]
        _http_adapter = HTTPAdapter(
            max_retries=Retry(
                total=max_request_retries,
                backoff_factor=0.5,
                status_forcelist=request_retry_status_list,
            )
        )
        super().__init__()
        self.base_url = base_url
        self.spy_session = spy.Session()
        self.authenticate(username, password)
        self.project_id = get_project_id_from_name(project_name, self.spy_session)
        self.mount("http://", _http_adapter)
        self.mount("https://", _http_adapter)

    def authenticate(self, username, password):
        spy.login(
            username=username,
            password=password,
            url=self.base_url,
            quiet=True,
            session=self.spy_session,
        )
        auth_header = {
            "sq-auth": self.spy_session.client.auth_token,
            "Content-Type": "application/json",
        }
        self.auth_header = auth_header
        self.headers.update(auth_header)
        self.cookies.update(auth_header)

    # def get_project_id(self, project_name):
    #     items_api = sdk.ItemsApi(self.spy_session.client)
    #     response = items_api.search_items(
    #         filters=[f"name=={project_name}"], types=["Project"]
    #     )
    #     if len(response.items) == 0:
    #         raise Exception(f"Could not find a project with name {project_name}")
    #     self.project_id = response.items[0].id

    def request(self, method, notebook, endpoint, *args, **kwargs):
        joined_url = f"{self.base_url}/data-lab/{self.project_id}/functions/notebooks/{notebook}/endpoints/{endpoint}"

        return super().request(
            method,
            joined_url,
            *args,
            **kwargs,
        )
