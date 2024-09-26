from requests import Session
from seeq import sdk, spy
import json
from requests.adapters import HTTPAdapter, Retry


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
        self.project_id = self.get_project_id(project_name)
        self.mount("http://", _http_adapter)
        self.mount("https://", _http_adapter)
        self.auth_header = None

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

    def get_project_id(self, project_name):
        if spy.utils.is_guid(project_name):
            projects_api = sdk.ProjectsApi(self.spy_session.client)
            response = projects_api.get_project(id=project_name)
            if response.id == project_name:
                return project_name
        items_api = sdk.ItemsApi(self.spy_session.client)
        response = items_api.search_items(
            filters=[f"name=={project_name}"], types=["Project"]
        )
        if len(response.items) == 0:
            raise Exception(f"Could not find a project with name {project_name}")
        if len(response.items) > 1:
            raise Exception(f"Multiple projects found with name {project_name}. Try using the project ID instead.")
        return response.items[0].id

    def dlf_request(self, method, notebook, endpoint, *args, **kwargs):
        joined_url = f"{self.base_url}/data-lab/{self.project_id}/functions/notebooks/{notebook}/endpoints/{endpoint}"
        return super().request(
            method,
            joined_url,
            *args,
            **kwargs,
        )

    def dlf_logs(self, method, log_file, *args, **kwargs):
        if log_file is None:
            log_file = ""
        else:
            log_file = f"/{log_file.strip("/")}"
        joined_url = f"{self.base_url}/data-lab/{self.project_id}/functions/logs{log_file}"
        return super().request(
            method,
            joined_url,
            *args,
            **kwargs,
        )


class AddOnManagerSession(DataLabFunctionSession):
    API_NOTEBOOK_NAME = "addonmanagerAPI"
    ADD_ON_MANAGER_PROJECT_NAME = "com.seeq.add-on-manager"

    def __init__(self, base_url, username, password):
        super().__init__(base_url, username, password, self.ADD_ON_MANAGER_PROJECT_NAME)

    def aom_request(self, method, endpoint, *args, **kwargs):
        return super().dlf_request(
            method,
            self.API_NOTEBOOK_NAME,
            endpoint,
            *args,
            **kwargs,
        )

    def aom_logs_request(self, method, log_file, *args, **kwargs):
        return super().dlf_logs(
            method,
            log_file,
            *args,
            **kwargs,
        )

    def get_add_on(self, add_on_identifier, hydrated=False):
        return self.aom_request(
            "GET",
            f"add-ons/add-on",
            params={"add_on_identifier": add_on_identifier, "hydrated": hydrated},
        )

    def uninstall_add_on(self, add_on_identifier, force=False):
        return self.aom_request(
            "POST",
            f"add-ons/uninstall",
            params={"add_on_identifier": add_on_identifier, "force": force},
        )

    def upload_add_on(self, filename, data):
        # temporarily unset the content-type header
        content_type = self.headers.pop("Content-Type")
        try:
            request = self.aom_request(
                "POST",
                "add-ons/upload-binary",
                data={"filename": filename, "data": data},
            )
            return request
        except Exception as e:
            raise e
        finally:
            self.headers.update({"Content-Type": content_type})

    def install_add_on(self, add_on_identifier, binary_filename, configuration):
        return self.aom_request(
            "POST",
            f"add-ons/install",
            data=json.dumps(
                {
                    "add_on_identifier": add_on_identifier,
                    "binary_filename": binary_filename,
                    "configuration": configuration,
                }
            ),
        )

    def update_add_on(self, add_on_identifier, binary_filename, configuration):
        return self.aom_request(
            "POST",
            f"add-ons/update",
            data=json.dumps(
                {
                    "add_on_identifier": add_on_identifier,
                    "binary_filename": binary_filename,
                    "configuration": configuration,
                }
            ),
        )

    def get_logs(self, log_file=None):
        return self.aom_logs_request(
            "GET",
            log_file
        )
