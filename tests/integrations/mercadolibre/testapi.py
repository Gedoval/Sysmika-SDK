from src.integrations.mercadolibre.api.caller import MercadoLibreAPICaller
from src.integrations.mercadolibre.constants.constants import MercadoLibreConstants
from src.integrations.mercadolibre.model.access_token import AccessToken
from src.integrations.mercadolibre.exceptions.mercadolibre_exceptions import *
import requests_mock
import os


class TestMercadoLibreApi:

    def test_get_tg_code(self):
        with requests_mock.Mocker() as m:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            target_dir = os.path.sep.join(current_dir.split(os.path.sep)[:-2])
            m.post(
                url=MercadoLibreConstants.API_HOST + MercadoLibreConstants.TOKEN_URL,
                json=open(target_dir + "/resources/auth_token.json").read()
            )
            access_token = MercadoLibreAPICaller(
                api_key="0000000",
                api_secret="ffffff"
                ).get_access_token(
                "TG-60b306c54e5c030007cf0e61-52073370",
                "https://google.com"
            )
            assert access_token is not None
            assert type(access_token) is AccessToken

    def test_get_tg_code_on_exception(self):
        with requests_mock.Mocker() as m:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            target_dir = os.path.sep.join(current_dir.split(os.path.sep)[:-2])
            m.post(
                url=MercadoLibreConstants.API_HOST + MercadoLibreConstants.TOKEN_URL,
                json=open(target_dir + "/resources/auth_token_exception.json").read(),
                status_code=400
            )
            try:
                access_token = MercadoLibreAPICaller(
                    api_key="gggggg",
                    api_secret="0000000"
                    ).get_access_token(
                    "TG-60b306c54e5c030007cf0e61-52073370",
                    "https://google.com"
                )
            except AuthTokenGenerationError as err:
                assert err.error_code is 400
                assert err.message in open(target_dir + "/resources/auth_token_exception.json").read()



