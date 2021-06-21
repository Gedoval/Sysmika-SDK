import pytest
from src.integrations.mercadolibre.inbound.app import create_app as app
from src.integrations.mercadolibre.model.access_token import AccessToken
import requests_mock
import os, json
from src.integrations.mercadolibre.constants.constants import Constants as Consts
from src.utils.Utils import SysmikaUtils
from src.integrations.mercadolibre.model.test_user import TestUser


class TestMercadoLibreApi:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    target_dir = os.path.sep.join(current_dir.split(os.path.sep)[:-2])

    @pytest.fixture
    def client(self):
        with app().test_client() as client:
            yield client

    def test_create_test_user(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                url=Consts.API_HOST + Consts.TOKEN_URL,
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/auth_token.json"))
            )
            m.post(
                url=Consts.API_HOST + Consts.TEST_USER_URL,
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/test_user.json"))
            )
            headers = {
                Consts.APP_TOKEN: "asdadasd",
                Consts.SITE: "MLA"
            }

            response = client.get(Consts.CREATE_TEST_USER, headers=headers)
            assert response is not None
            assert response.status_code is 200
            data = SysmikaUtils.flask_data_parser(response.data)
            test_user = SysmikaUtils.json_parser(json.loads(data), TestUser())
            assert test_user is not None and isinstance(test_user, TestUser)

    def test_get_access_token(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                url=Consts.API_HOST + Consts.TOKEN_URL,
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/auth_token.json"))
            )
            headers = {
                Consts.TG_CODE: "TG-1234",
                Consts.REDIRECT_URL: "http://asd.com",
                Consts.APP_ID: "APP-ID",
                Consts.APP_SECRET: "APP-Secret"
            }

            response = client.get(Consts.GET_ACCESS_TOKEN, headers=headers)
            assert response is not None
            assert response.status_code is 200
            data = SysmikaUtils.flask_data_parser(response.data)
            access_token = SysmikaUtils.json_parser(json.loads(data), AccessToken())
            assert access_token is not None and isinstance(access_token, AccessToken)
            assert access_token.access_token is not None

    def test_refresh_token(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                url=Consts.API_HOST + Consts.TOKEN_URL,
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/auth_token.json"))
            )
            headers = {
                Consts.REFRESH_TOKEN: "TG-1234",
                Consts.APP_ID: "APP-ID",
                Consts.APP_SECRET: "APP-Secret"
            }

            response = client.get(Consts.REFRESH_ACCESS_TOKEN, headers=headers)
            assert response is not None
            assert response.status_code is 200
            data = SysmikaUtils.flask_data_parser(response.data)
            access_token = SysmikaUtils.json_parser(json.loads(data), AccessToken())
            assert access_token is not None and isinstance(access_token, AccessToken)
            assert access_token.access_token is not None
            assert access_token.refresh_token is not None
