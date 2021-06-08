from src.integrations.mercadolibre.api.mercadolibre_invoker import MercadoLibreAPICaller
from src.integrations.mercadolibre.constants.constants import MercadoLibreConstants
from src.integrations.mercadolibre.model.access_token import AccessToken
from src.integrations.mercadolibre.exceptions.mercadolibre_exceptions import *
import requests_mock
import os


class TestMercadoLibreInvoker:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    target_dir = os.path.sep.join(current_dir.split(os.path.sep)[:-2])

    def test_get_tg_code(self):
        with requests_mock.Mocker() as m:
            m.post(
                url=MercadoLibreConstants.API_HOST + MercadoLibreConstants.TOKEN_URL,
                json=open(TestMercadoLibreInvoker.target_dir + "/resources/auth_token.json").read()
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
            m.post(
                url=MercadoLibreConstants.API_HOST + MercadoLibreConstants.TOKEN_URL,
                json=open(TestMercadoLibreInvoker.target_dir + "/resources/invalid_grant.json").read(),
                status_code=400
            )
            try:
                MercadoLibreAPICaller(
                    api_key="gggggg",
                    api_secret="0000000"
                    ).get_access_token(
                    "TG-60b306c54e5c030007cf0e61-52073370",
                    "https://google.com"
                )
            except AuthTokenGenerationError as err:
                assert str(err.status) in str(400)
                assert err.message in open(TestMercadoLibreInvoker.target_dir + "/resources/invalid_grant.json").read()

    def test_generate_refresh_token(self):
        with requests_mock.Mocker() as m:
            m.post(
                url=MercadoLibreConstants.API_HOST + MercadoLibreConstants.TOKEN_URL,
                json=open(TestMercadoLibreInvoker.target_dir + "/resources/refresh_token_success.json").read(),
                status_code=200
            )
            refresh_token = MercadoLibreAPICaller(
                api_key="0000000",
                api_secret="ffffff"
                ).refresh_access_token(
                "TG-60b306c54e5c030007cf0e61-52073370"
            )
            assert refresh_token is not None
            assert refresh_token.access_token is not None
            assert refresh_token.access_token in open(TestMercadoLibreInvoker.target_dir + "/resources/refresh_token_success.json").read()

    def test_parse_grant_error_response(self):
        with requests_mock.Mocker() as m:
            m.post(
                url=MercadoLibreConstants.API_HOST + MercadoLibreConstants.TOKEN_URL,
                json=open(TestMercadoLibreInvoker.target_dir + "/resources/invalid_grant.json").read(),
                status_code=400
            )
            try:
                MercadoLibreAPICaller(
                    api_key="gggggg",
                    api_secret="0000000"
                    ).refresh_access_token(
                    "TG-60b306c54e5c030007cf0e61-52073370"
                )
            except AuthTokenGenerationError as err:
                assert str(err.status) in str(400)
                assert err.message in open(TestMercadoLibreInvoker.target_dir + "/resources/invalid_grant.json").read()



