import requests
from src.api.restapiinvoker import RestApiInvoker
from src.integrations.mercadolibre.constants.constants import MercadoLibreConstants
from src.utils.Utils import SysmikaUtils
from src.integrations.mercadolibre.model.test_user import TestUser


class TestUtils:
    @staticmethod
    def create_mercado_libre_test_user(self, access_token, site):
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
