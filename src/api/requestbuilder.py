from src.api.requestclient import RequestClient
import urllib.parse


class RequestBuilder:

    def __init__(self, api_key, api_secret):
        self.__api_key = api_key
        self.__api_secret = api_secret
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

    def get_api_key(self):
        return self.__api_key

    def get_api_secret(self):
        return self.__api_secret
