from src.integrations.mercadolibre.api.mercadolibre_invoker import MercadoLibreAPICaller
from src.integrations.mercadolibre.constants.constants import MercadoLibreConstants
from src.integrations.mercadolibre.model.access_token import AccessToken
from src.integrations.mercadolibre.exceptions.mercadolibre_exceptions import *
import requests_mock
import os
import yaml


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
                app_id="gggggg",
                app_secret="0000000"
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
                    app_id="gggggg",
                    app_secret="0000000"
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
                app_id="gggggg",
                app_secret="0000000"
            ).refresh_access_token(
                "TG-60b306c54e5c030007cf0e61-52073370"
            )
            assert refresh_token is not None
            assert refresh_token.access_token is not None
            assert refresh_token.access_token in open(
                TestMercadoLibreInvoker.target_dir + "/resources/refresh_token_success.json").read()

    def test_parse_grant_error_response(self):
        with requests_mock.Mocker() as m:
            m.post(
                url=MercadoLibreConstants.API_HOST + MercadoLibreConstants.TOKEN_URL,
                json=open(TestMercadoLibreInvoker.target_dir + "/resources/invalid_grant.json").read(),
                status_code=400
            )
            try:
                MercadoLibreAPICaller(
                    app_id="gggggg",
                    app_secret="0000000"
                ).refresh_access_token(
                    "TG-60b306c54e5c030007cf0e61-52073370"
                )
            except AuthTokenGenerationError as err:
                assert str(err.status) in str(400)
                assert err.message in open(TestMercadoLibreInvoker.target_dir + "/resources/invalid_grant.json").read()

    def test_set_credentials_from_file(self):
        mer = MercadoLibreAPICaller(cred_file="credentials.example.yml")
        creds = yaml.safe_load(open(TestMercadoLibreInvoker.target_dir + "/resources/mock_credentials.yml")).get(
            "credentials").get("api")
        assert mer is not None
        assert creds is not None
        assert creds.get("app_id")
        assert creds.get("app_secret")
        assert mer.builder.get_app_id() is not None
        assert mer.builder.get_app_secret() is not None
        assert mer.builder.get_app_secret() in creds.get("app_secret")
        assert mer.builder.get_app_id() == creds.get("app_id")
