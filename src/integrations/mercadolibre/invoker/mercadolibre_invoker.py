import json
from src.api.restapiinvoker import RestApiInvoker
from src.integrations.mercadolibre.model.access_token import AccessToken
from src.integrations.mercadolibre.exceptions.mercadolibre_exceptions import *
from src.integrations.mercadolibre.model.api_response import ApiResponse
from src.integrations.mercadolibre.model.test_user import TestUser
from src.integrations.mercadolibre.model.inmboliaria_categories import InmobiliariaCategories
from src.utils.Utils import SysmikaUtils
import requests
import os
from src.integrations.mercadolibre.constants.constants import Constants as Consts


class MercadoLibreAPICaller(RestApiInvoker):
    def __init__(self, app_id=None, app_secret=None, app_token=None, cred_file=None):
        super().__init__(app_id=app_id, app_secret=app_secret, app_token=app_token)
        self.__set_credentials(cred_file)
        self.__set_categories_dict()

    current_dir = os.path.dirname(os.path.realpath(__file__))
    target_dir = os.path.sep.join(current_dir.split(os.path.sep)[:-1])

    def get_access_token(self, tg_code, request_url):
        headers = {"content-type": "application/x-www-form-urlencoded", "accept": "application/json"}
        client = self.make_post_request(
            Consts.API_HOST,
            Consts.TOKEN_URL,
            headers,
            None,
            self.create_token_request_body(tg_code, request_url)
        )
        response = requests.post(client.host + client.url, data=client.post_body, headers=client.header)
        if response.status_code is not 200:
            raise SysmikaUtils.json_parser(response.json(), AuthTokenGenerationError())
        else:
            access_token = SysmikaUtils.json_parser(response.json(), AccessToken())
        self.__set_access_token(access_token.access_token)
        return access_token

    def refresh_access_token(self, refresh_code):
        headers = {"content-type": "application/x-www-form-urlencoded", "accept": "application/json"}
        client = self.make_post_request(
            Consts.API_HOST,
            Consts.TOKEN_URL,
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
        headers = {"Authorization": "Bearer " + app_token, "Content-Type": "application/json"}
        site_body = '{"site_id":' + '"' + site + '"' + '}'
        client = self.make_post_request(
            Consts.API_HOST,
            Consts.TEST_USER_URL,
            headers,
            None,
            site_body
        )
        response = requests.post(client.host + client.url, data=client.post_body, headers=client.header)
        if response.status_code is not 201:
            raise SysmikaUtils.json_parser(response.json(), UserCreationError())
        else:
            test_user = SysmikaUtils.json_parser(response.json(), TestUser())
        return test_user

    def get_category_attributes(self, category_id):
        client = self.make_get_request(
            Consts.API_HOST,
            Consts.CATEGORIES + "/" + category_id + "/attributes",
            None,
            None
        )
        response = requests.get(client.host + client.url)
        if response.status_code is not 200:
            raise SysmikaUtils.json_parser(response.json(), MercadoLibreError())
        else:
            desc = json.dumps(response.json())
        return desc

    def get_categories(self):
        return self.categories

    """
    Publication Methods
    """

    def post_real_state_publication(self, body):
        headers = {"Authorization": "Bearer " + self.builder.get_app_token(), "Content-Type": "application/json"}
        self.__validate_sync_event_json(body)
        client = self.make_post_request(
            Consts.API_HOST,
            Consts.ITEMS,
            headers=headers,
            body=body.get("Payload")
        )
        response = requests.post(client.host + client.url, json=client.post_body, headers=client.header)
        if response.status_code == 400:
            raise SysmikaUtils.json_parser(response.json(), PublicationError())
        return SysmikaUtils.json_parser(response.json(), ApiResponse())

    def put_update_real_state_publication(self, body, item_id, status=None):
        headers = {"Authorization": "Bearer " + self.builder.get_app_token(),
                   "Content-Type": "application/json",
                   "Accept": "application/json"
                   }
        if status is not None:
            body = {"status": status}
        else:
            self.__validate_sync_event_json(body)
            body = body.get("Payload")

        client = self.make_put_request(
            Consts.API_HOST,
            Consts.ITEMS + "/" + item_id,
            body=body,
            headers=headers
        )
        response = requests.put(client.host + client.url, json=client.post_body)
        if response.status_code != 200:
            raise SysmikaUtils.json_parser(response.json(), PublicationError())
        return SysmikaUtils.json_parser(response.json(), ApiResponse())

    def delete_publication(self, item_id):
        headers = {"Authorization": "Bearer " + self.builder.get_app_token(),
                   "Content-Type": "application/json",
                   "Accept": "application/json"
                   }
        body = {"deleted": "true"}
        client = self.make_put_request(
            Consts.API_HOST,
            Consts.ITEMS + "/" + item_id,
            body=body,
            headers=headers
        )
        response = requests.put(client.host + client.url, json=client.post_body)
        if response.status_code != 200:
            raise SysmikaUtils.json_parser(response.json(), PublicationError())
        return SysmikaUtils.json_parser(response.json(), ApiResponse())

    """
    Location Endpoints
    """
    def get_argentina_locations_id(self):
        client = self.make_get_request(
            Consts.API_HOST,
            Consts.LOCATION_AR,
            None,
            None
        )
        response = requests.get(client.host + client.url)
        return response.json()

    def get_location_info(self, location, state_id):
        client = self.make_get_request(
            Consts.API_HOST,
            Consts.LOCATION_STATE_INFO + "/" + location + "/" + state_id,
            None,
            None
        )
        response = requests.get(client.host + client.url)
        return response.json()

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

    def __set_categories_dict(self):
        self.categories = InmobiliariaCategories().categories

    def __set_access_token(self, token):
        self.builder.set_app_token(token)

    def __validate_sync_event_json(self, data):
        if not (SysmikaUtils.validate_sync_event_schema(data)):
            raise PublicationError(status=400, message="The request body is not valid. Please check the JSON schema")





