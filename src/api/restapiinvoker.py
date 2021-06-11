from src.api.requestbuilder import RequestBuilder
from src.integrations.mercadolibre.constants.constants import MercadoLibreConstants as Consts


class RestApiInvoker:
    def __init__(self, **kwargs):
        app_id = None
        app_secret = None
        app_token = None
        if Consts.APP_ID in kwargs:
            app_id = kwargs[Consts.APP_ID]
        if Consts.APP_SECRET in kwargs:
            app_secret = kwargs[Consts.APP_SECRET]
        if Consts.APP_TOKEN in kwargs:
            app_token = kwargs[Consts.APP_TOKEN]
        self.builder = RequestBuilder(app_id, app_secret, app_token)

    def make_get_request(self, host, url, headers=None, params=None):
        return self.builder.build_get_request(host, url, headers, params)

    def make_post_request(self, host, url, headers=None, params=None, body=None):
        return self.builder.build_post_request(host, url, headers, params, body)
