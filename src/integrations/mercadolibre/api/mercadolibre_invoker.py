from src.api.restapiinvoker import RestApiInvoker
from src.integrations.mercadolibre.constants.constants import MercadoLibreConstants
from src.integrations.mercadolibre.model.access_token import AccessToken
from src.integrations.mercadolibre.exceptions.mercadolibre_exceptions import *
from src.integrations.mercadolibre.model.test_user import TestUser
from src.utils.Utils import SysmikaUtils
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
            raise SysmikaUtils.json_parser(response.json(), AuthTokenGenerationError())
        else:
            access_token = SysmikaUtils.json_parser(response.json(), AccessToken())
        return access_token

    def refresh_access_token(self, refresh_code):
        headers = {"content-type": "application/x-www-form-urlencoded", "accept": "application/json"}
        client = self.make_post_request(
            MercadoLibreConstants.API_HOST,
            MercadoLibreConstants.TOKEN_URL,
            headers,
            None,
            self.refresh_token_request_body(refresh_code)
        )
        response = requests.post(client.host + client.url, data=client.post_body, headers=client.header)
        if response.status_code is not 200:
            raise SysmikaUtils.json_parser(response.json(), AuthTokenGenerationError())
        else:
            access_token = SysmikaUtils.json_parser(response.json(), AccessToken())
        return access_token


    def create_mercado_libre_test_user(self, tg_code, request_url, site):
        access_token = self.get_access_token(tg_code, request_url).access_token
        headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json" }
        client = RestApiInvoker().make_post_request(
            MercadoLibreConstants.API_HOST,
            MercadoLibreConstants.TEST_USER_URL,
            headers,
            None,
            {"site_id": site}
        )
        response = requests.post(client.host + client.url, data=client.post_body, headers=client.header)
        test_user = SysmikaUtils.json_parser(response.json(), TestUser())
        return test_user

    def create_token_request_body(self, tg_code, redirect_url):
        return "grant_type=authorization_code&" \
               "client_id=" + self.builder.get_api_key() + "&" \
               "client_secret=" + self.builder.get_api_secret() + "&" \
                "code=" + tg_code + "&" \
                "redirect_uri=" + redirect_url

    def refresh_token_request_body(self, refresh_code):
        return "grant_type=refresh_token&" \
               "client_id=" + self.builder.get_api_key() + "&" \
                "client_secret=" + self.builder.get_api_secret() + "&" \
                "refresh_token=" + refresh_code
