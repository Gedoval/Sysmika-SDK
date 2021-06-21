import json

from src.integrations.mercadolibre.invoker.mercadolibre_invoker import MercadoLibreAPICaller
from src.integrations.mercadolibre.constants.constants import Constants as Consts
from src.integrations.mercadolibre.model.access_token import AccessToken
from src.integrations.mercadolibre.model.inmboliaria_categories import InmobiliariaCategories
from src.integrations.mercadolibre.exceptions.mercadolibre_exceptions import *
import requests_mock
import os
import yaml


class TestMercadoLibreInvoker:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    target_dir = os.path.sep.join(current_dir.split(os.path.sep)[:-2])

    def test_get_access_token(self):
        with requests_mock.Mocker() as m:
            m.post(
                url=Consts.API_HOST + Consts.TOKEN_URL,
                json=json.load(open(TestMercadoLibreInvoker.target_dir + "/resources/auth_token.json"))
            )
            invoker = MercadoLibreAPICaller(app_id="gggggg", app_secret="0000000")
            access_token = invoker.get_access_token(
                "TG-60b306c54e5c030007cf0e61-52073370",
                "https://google.com"
            )
            assert access_token is not None
            assert type(access_token) is AccessToken
            assert invoker.builder.get_app_token() is not None

    def test_get_access_code_exception(self):
        with requests_mock.Mocker() as m:
            m.post(
                url=Consts.API_HOST + Consts.TOKEN_URL,
                json=json.load(open(TestMercadoLibreInvoker.target_dir + "/resources/invalid_grant.json")),
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
                url=Consts.API_HOST + Consts.TOKEN_URL,
                json=json.load(open(TestMercadoLibreInvoker.target_dir + "/resources/refresh_token_success.json")),
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

    def test_parse_grant_error_response_on_token_creation(self):
        with requests_mock.Mocker() as m:
            m.post(
                url=Consts.API_HOST + Consts.TOKEN_URL,
                json=json.load(open(TestMercadoLibreInvoker.target_dir + "/resources/invalid_grant.json")),
                status_code=400
            )
            try:
                MercadoLibreAPICaller(
                    app_id="gggggg",
                    app_secret="0000000"
                ).get_access_token(
                    "TG-60b306c54e5c030007cf0e61-52073370",
                    "google.com"
                )
            except AuthTokenGenerationError as err:
                assert str(err.status) in str(400.0)

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

    def test_create_user_test_error(self):
        with requests_mock.Mocker() as m:
            m.post(
                url=Consts.API_HOST + Consts.TEST_USER_URL,
                json=json.load(open(TestMercadoLibreInvoker.target_dir + "/resources/user_creation_error.json")),
                status_code=400
            )
            try:
                MercadoLibreAPICaller().create_mercado_libre_test_user(
                    "TG-1231",
                    "MLA"
                )
            except UserCreationError as e:
                assert isinstance(e, UserCreationError)

    def test_get_category_description(self):
        with requests_mock.Mocker() as m:
            m.get(
                url=Consts.API_HOST + Consts.CATEGORIES + "/MLA1234/attributes",
                json=json.load(open(TestMercadoLibreInvoker.target_dir + "/resources/department_description.json")),
                status_code=200
            )
            resp = MercadoLibreAPICaller().get_category_attributes("MLA1234")
            assert resp is not None

    def test_get_categories_ids(self):
        resp = MercadoLibreAPICaller().get_categories()
        assert resp is not None

    def test_post_publish(self):
        with requests_mock.Mocker() as m:
            m.post(
                url=Consts.API_HOST + Consts.ITEMS,
                json=json.load(open(TestMercadoLibreInvoker.target_dir + "/resources/publication_response.json")),
                status_code=200
            )
            invoker = MercadoLibreAPICaller()
            invoker.builder.set_app_token("AG-12341")
            body = open(TestMercadoLibreInvoker.target_dir + "/resources/sample_publication.json").read()
            resp = invoker.post_real_state_publication(body)
            assert resp is not None
