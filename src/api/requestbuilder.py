from src.api.requestclient import RequestClient
import urllib.parse
import yaml


class RequestBuilder:

    def __init__(self, app_id, app_secret, app_token):
        self.__app_id = app_id
        self.__app_secret = app_secret
        self.__app_token = app_token
        self.__params = dict()
        self.client = RequestClient()

    def build_get_request(self, host, url, headers, params):
        self.__init_client(host=host, headers=headers, params=params)
        self.client.method = "GET"
        self.__encode_params(url)
        return self.client

    def build_post_request(self, host, url, headers, params, body):
        self.__init_client(host=host, headers=headers, params=params, body=body)
        self.client.method = "POST"
        self.__encode_params(url)
        return self.client

    def build_put_request(self, host, url, body, headers):
        pass

    def build_patch_request(self, host, url, body, headers):
        pass

    def __init_client(self, **kwargs):
        self.client.host = kwargs["host"]
        if "headers" in kwargs is not None:
            self.client.header = kwargs["headers"]
        if "params" in kwargs is not None:
            self.client.params = kwargs["params"]
        if "body" in kwargs is not None:
            self.client.post_body = kwargs["body"]

    def __encode_params(self, url):
        if self.client.params is None:
            self.client.url = url
        else:
            self.client.url = url + "?" + urllib.parse.urlencode(self.client.params)

    def set_api_credentials_from_file(self, file):
        with open(file, "r") as stream:
            try:
                creds = yaml.safe_load(stream).get("credentials").get("api")
                self.__app_id = creds.get("app_id")
                self.__app_secret = creds.get("app_secret")
            except yaml.YAMLError as exc:
                print(exc)

    def get_app_id(self):
        return self.__app_id

    def get_app_secret(self):
        return self.__app_secret

    def get_app_token(self):
        return self.__app_token
