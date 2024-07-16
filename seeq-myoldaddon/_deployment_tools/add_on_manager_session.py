class AddOnManagerSession(DataLabFunctionSession):
    API_NOTEBOOK_NAME = "addonmanagerAPI"
    ADD_ON_MANAGER_PROJECT_NAME = "com.seeq.add-on-manager"

    def __init__(self, base_url, username, password):
        super().__init__(base_url, username, password, self.ADD_ON_MANAGER_PROJECT_NAME)

    def aom_request(self, method, endpoint, *args, **kwargs):
        return super().request(
            method,
            self.API_NOTEBOOK_NAME,
            endpoint,
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
