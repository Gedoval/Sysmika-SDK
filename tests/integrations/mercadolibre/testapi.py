import pytest
from src.integrations.mercadolibre.constants.constants import MercadoLibreConstants
from src.integrations.mercadolibre.exceptions.mercadolibre_exceptions import *
from src.integrations.mercadolibre.api.app import create_app as app
from src.utils.Utils import SysmikaUtils
from src.integrations.mercadolibre.model.test_user import TestUser
import requests_mock
import os
import json
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
                url=MercadoLibreConstants.API_HOST + MercadoLibreConstants.TOKEN_URL,
                json=open(TestMercadoLibreApi.target_dir + "/resources/auth_token.json").read()
            )
            m.post(
                url=MercadoLibreConstants.API_HOST + MercadoLibreConstants.TEST_USER_URL,
                json=open(TestMercadoLibreApi.target_dir + "/resources/test_user.json").read()
            )
            headers = {
                "app_token": "asdadasd",
                "site_id": "MLA"
            }

            response = client.get("/user/test", headers=headers)
            assert response is not None
            assert response.status_code is 200
            data = response.data.decode('UTF-8').strip('\n')
            test_user = SysmikaUtils.json_parser(data, TestUser())
            assert test_user is not None and isinstance(test_user, TestUser)


