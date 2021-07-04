import pytest

from src.integrations.mercadolibre.exceptions.mercadolibre_exceptions import MissingHeadersError, PublicationError
from src.integrations.mercadolibre.inbound.app import create_app as app
from src.integrations.mercadolibre.model.access_token import AccessToken
import requests_mock
import os, json
from src.integrations.mercadolibre.constants.constants import Constants as Consts
from src.integrations.mercadolibre.model.api_response import ApiResponse
from src.utils.Utils import SysmikaUtils
from src.integrations.mercadolibre.model.test_user import TestUser

"""
Unit tests for the Flask API. Each tests calls a Flask endpoint, which in turn will call the MercadoLibre API. 
We mock the response from MercadoLibre only.
All tests names must begin with 'test_' so Pytest can pick them up
"""


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

    def test_get_categories(self, client):
        with requests_mock.Mocker() as m:
            m.get(
                url=Consts.API_HOST + Consts.CATEGORIES + "/MLA1234/attributes",
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/department_description.json"))
            )
            response = client.get(Consts.CATEGORIES + "/MLA1234")
            assert response is not None
            data = json.loads(SysmikaUtils.flask_data_parser(response.data))
            assert data is not None

    def test_get_auth_token_with_missing_required_headers(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                url=Consts.API_HOST + Consts.TOKEN_URL,
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/auth_token.json"))
            )
            headers = {
                Consts.TG_CODE: "TG-1234",
                Consts.REDIRECT_URL: "http://asd.com"
            }
            response = client.get(Consts.GET_ACCESS_TOKEN, headers=headers)
            assert response is not None
            assert "Missing required headers" in SysmikaUtils.flask_data_parser(response.data)

    def test_refresh_token_with_missing_headers(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                url=Consts.API_HOST + Consts.TOKEN_URL,
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/auth_token.json"))
            )
            headers = {
                Consts.TG_CODE: "TG-1234",
                Consts.REDIRECT_URL: "http://asd.com"
            }
            response = client.get(Consts.REFRESH_ACCESS_TOKEN, headers=headers)
            assert response is not None
            assert "Missing required headers" in SysmikaUtils.flask_data_parser(response.data)

    def test_create_test_user_with_missing_headers(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                url=Consts.API_HOST + Consts.TOKEN_URL,
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/auth_token.json"))
            )
            headers = {}
            response = client.get(Consts.CREATE_TEST_USER, headers=headers)
            assert response is not None
            assert "Missing required headers" in SysmikaUtils.flask_data_parser(response.data)

    def test_publish_post_endpoint(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                url=Consts.API_HOST + Consts.ITEMS,
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/publication_response.json"))
            )
            headers = {
                Consts.APP_TOKEN: "AG-1234857"
            }
            body = open(TestMercadoLibreApi.target_dir + "/resources/sample_publication.json").read()
            response = client.post(Consts.CREATE_PUBLICATION, headers=headers, json=body)
            assert response is not None
            data = SysmikaUtils.flask_data_parser(response.data)
            api_response = SysmikaUtils.json_parser(json.loads(data), ApiResponse())
            assert api_response is not None

    def test_publish_put_endpoint(self, client):
        with requests_mock.Mocker() as m:
            m.put(
                url=Consts.API_HOST + Consts.ITEMS + "/MLA11234",
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/publication_update_response.json")),
                status_code=200
            )
            headers = {
                Consts.APP_TOKEN: "AG-1234857",
                Consts.ITEM_ID: "MLA11234"
            }
            body = json.load(open(TestMercadoLibreApi.target_dir + "/resources/sample_sync_event.json"))
            response = client.put(Consts.UPDATE_PUBLICATION, headers=headers, json=body)
            assert response is not None
            data = SysmikaUtils.flask_data_parser(response.data)
            api_response = SysmikaUtils.json_parser(json.loads(data), ApiResponse())
            assert api_response is not None

    def test_put_update_publication_status(self, client):
        with requests_mock.Mocker() as m:
            m.put(
                url=Consts.API_HOST + Consts.ITEMS + "/MLA11234",
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/publication_update_response.json")),
                status_code=200
            )
            headers = {
                Consts.APP_TOKEN: "AG-1234857",
                Consts.ITEM_ID: "MLA11234"
            }
            body = json.load(open(TestMercadoLibreApi.target_dir + "/resources/sample_sync_event.json"))
            response = client.put(Consts.UPDATE_PUBLICATION + "/paused", headers=headers, json=body)
            assert response is not None
            assert response.status_code is 200
            data = SysmikaUtils.flask_data_parser(response.data)
            api_response = SysmikaUtils.json_parser(json.loads(data), ApiResponse())
            assert api_response is not None

    def test_put_update_publication_status_with_bad_query_param(self,client):
        with requests_mock.Mocker() as m:
            m.put(
                url=Consts.API_HOST + Consts.ITEMS + "/MLA11234",
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/publication_update_response.json")),
                status_code=200
            )
            headers = {
                Consts.APP_TOKEN: "AG-1234857",
                Consts.ITEM_ID: "MLA11234"
            }
            body = json.load(open(TestMercadoLibreApi.target_dir + "/resources/sample_sync_event.json"))
            response = client.put(Consts.UPDATE_PUBLICATION + "/sarasa", headers=headers, json=body)
            assert response is not None
            assert response.status_code is 200
            data = SysmikaUtils.flask_data_parser(response.data)
            assert data is not None
            assert "The status sent is not allowed" in data

    def test_publish_post_endpoint_on_error(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                url=Consts.API_HOST + Consts.ITEMS,
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/bad_publication_response.json")),
                status_code=400
            )
            headers = {
                Consts.APP_TOKEN: "AG-21249"
            }
            response = client.post(Consts.CREATE_PUBLICATION, headers=headers)
            assert response is not None
            data = json.loads(SysmikaUtils.flask_data_parser(response.data))
            assert data is not None
            api_response = SysmikaUtils.json_parser(data, PublicationError())
            assert api_response is not None
            assert isinstance(api_response, PublicationError)
            assert api_response.status == 400

    def test_publish_post_endpoint_on_missing_headers(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                url=Consts.API_HOST + Consts.ITEMS,
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/bad_publication_response.json")),
            )
            headers = {}
            response = client.post(Consts.CREATE_PUBLICATION, headers=headers)
            assert response is not None
            assert "Missing required headers" in SysmikaUtils.flask_data_parser(response.data)

    def test_publish_put_endpoint_on_error(self, client):
        with requests_mock.Mocker() as m:
            m.put(
                url=Consts.API_HOST + Consts.ITEMS + "/MLA11234",
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/bad_publication_response.json")),
                status_code=400
            )
            headers = {
                Consts.APP_TOKEN: "AG-1234857",
                Consts.ITEM_ID: "MLA11234"
            }
            response = client.put(Consts.UPDATE_PUBLICATION, headers=headers)
            assert response is not None
            data = json.loads(SysmikaUtils.flask_data_parser(response.data))
            assert data is not None
            api_response = SysmikaUtils.json_parser(data, PublicationError())
            assert api_response is not None
            assert isinstance(api_response, PublicationError)
            assert api_response.status == 400

    def test_delete_publication(self, client):
        with requests_mock.Mocker() as m:
            m.put(
                url=Consts.API_HOST + Consts.ITEMS + "/MLA11234",
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/publication_update_response.json")),
                status_code=400
            )
            headers = {
                Consts.APP_TOKEN: "AG-1234857",
                Consts.ITEM_ID: "MLA11234"
            }
            response = client.delete(Consts.DELETE_PUBLICATION, headers=headers)
            assert response is not None

    def test_delete_publication_with_missing_headers(self, client):
        with requests_mock.Mocker() as m:
            m.post(
                url=Consts.API_HOST + Consts.ITEMS,
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/bad_publication_response.json")),
            )
            headers = {}
            response = client.delete(Consts.DELETE_PUBLICATION, headers=headers)
            assert response is not None
            assert "Missing required headers" in SysmikaUtils.flask_data_parser(response.data)

    def test_get_argentina_location_ids(self, client):
        with requests_mock.Mocker() as m:
            m.get(
                url=Consts.API_HOST + Consts.LOCATION_AR,
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/argentina_locations.json"))
            )
            response = client.get(Consts.LOCATION_GET_ARGENTINA)
            assert response is not None
            data = json.loads(SysmikaUtils.flask_data_parser(response.data))
            assert data is not None
            assert data.get("states") is not None

    def test_get_location_info(self, client):
        with requests_mock.Mocker() as m:
            m.get(
                url=Consts.API_HOST + Consts.LOCATION_STATE_INFO + "/states/TUxBQ0NBUGZlZG1sYQ",
                json=json.load(open(TestMercadoLibreApi.target_dir + "/resources/salta_location_info.json"))
            )
            response = client.get("/location/states/TUxBQ0NBUGZlZG1sYQ")
            assert response is not None
            data = json.loads(SysmikaUtils.flask_data_parser(response.data))
            assert data is not None
            assert data.get("cities") is not None

