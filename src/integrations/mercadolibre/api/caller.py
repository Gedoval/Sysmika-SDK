from src.api.restapiinvoker import RestApiInvoker
from src.integrations.mercadolibre.constants.constants import MercadoLibreConstants
from src.integrations.mercadolibre.model.access_token import AccessToken
from src.integrations.mercadolibre.exceptions.mercadolibre_exceptions import *
import requests


class MercadoLibreAPICaller(RestApiInvoker):
    def __init__(self, **kwargs):
        super().__init__(api_key=kwargs["api_key"], api_secret=kwargs["api_secret"])

    def get_access_token(self, tg_code, request_url):
        headers = {"content-type": "application/x-www-form-urlencoded", "accept": "application/json"}
        client = self.make_post_request(
            MercadoLibreConstants.API_HOST,
            MercadoLibreConstants.TOKEN_URL,
            headers,
            None,
            self.create_token_request_body(tg_code, request_url)
        )
        response = requests.post(client.host + client.url, data=client.post_body, headers=client.header)
        if response.status_code is not 200:
            raise AuthTokenGenerationError(response.status_code, response.json())
        else:
            access_token = AccessToken.json_parser(response.json())
        return access_token

    def create_token_request_body(self, tg_code, redirect_url):
        return "grant_type=authorization_code&" \
               "client_id=" + self.builder.get_api_key() + "&"  \
               "client_secret=" + self.builder.get_api_secret() + "&"\
               "code=" + tg_code + "&" \
               "redirect_uri=" + redirect_url
