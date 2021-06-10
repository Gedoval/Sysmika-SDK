from src.api.restapiinvoker import RestApiInvoker
from src.integrations.mercadolibre.constants.constants import MercadoLibreConstants
from src.integrations.mercadolibre.model.access_token import AccessToken
from src.integrations.mercadolibre.exceptions.mercadolibre_exceptions import *
from src.integrations.mercadolibre.model.test_user import TestUser
from src.utils.Utils import SysmikaUtils
import requests
import os
from src.integrations.mercadolibre.constants.constants import MercadoLibreConstants as Consts


class MercadoLibreAPICaller(RestApiInvoker):
    def __init__(self, app_id=None, app_secret=None, app_token=None, cred_file=None):
        super().__init__(app_id=app_id, app_secret=app_secret, app_token=app_token)
        self.__set_credentials(cred_file)

    current_dir = os.path.dirname(os.path.realpath(__file__))
    target_dir = os.path.sep.join(current_dir.split(os.path.sep)[:-1])

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

    def create_mercado_libre_test_user(self, app_token, site):
        headers = {"Authorization": "Bearer " + app_token, "Content-Type": "application/json" }
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
               "client_id=" + self.builder.get_app_id() + "&" \
               "client_secret=" + self.builder.get_app_secret() + "&" \
                "code=" + tg_code + "&" \
                "redirect_uri=" + redirect_url

    def refresh_token_request_body(self, refresh_code):
        return "grant_type=refresh_token&" \
               "client_id=" + self.builder.get_app_id() + "&" \
                "client_secret=" + self.builder.get_app_secret() + "&" \
                "refresh_token=" + refresh_code

    def __set_credentials(self, cred_file):
        if cred_file is None:
            return
        self.builder.set_api_credentials_from_file(self.target_dir + "/credentials/" + cred_file)
