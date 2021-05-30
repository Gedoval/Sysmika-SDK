from src.api.requestbuilder import RequestBuilder


class RestApiInvoker:
    def __init__(self, **kwargs):
        api_key = None
        api_secret = None
        if "api_key" in kwargs:
            api_key = kwargs["api_key"]
        if "api_secret" in kwargs:
            api_secret = kwargs["api_secret"]
        self.builder = RequestBuilder(api_key, api_secret)

    def make_get_request(self, host, url, headers=None, params=None):
        return self.builder.build_get_request(host, url, headers, params)

    def make_post_request(self, host, url, headers=None, params=None, body=None):
        return self.builder.build_post_request(host, url, headers, params, body)
