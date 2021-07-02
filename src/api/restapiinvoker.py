from src.api.requestbuilder import RequestBuilder


class RestApiInvoker:
    def __init__(self, **kwargs):
        app_id = None
        app_secret = None
        app_token = None
        if "app_id" in kwargs:
            app_id = kwargs["app_id"]
        if "app_secret" in kwargs:
            app_secret = kwargs["app_secret"]
        if "app_token" in kwargs:
            app_token = kwargs["app_token"]
        self.builder = RequestBuilder(app_id, app_secret, app_token)

    def make_get_request(self, host, url, headers=None, params=None):
        return self.builder.build_get_request(host, url, headers, params)

    def make_post_request(self, host, url, headers=None, params=None, body=None):
        return self.builder.build_post_request(host, url, headers, params, body)

    def make_put_request(self, host, url, headers=None, params=None, body=None):
        return self.builder.build_put_request(host, url, headers, params, body)
