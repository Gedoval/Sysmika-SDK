from src.api.restapiinvoker import RestApiInvoker
from tests.constants.testcontstants import TestConstants


class TestApi:

    def test_get_client_generator(self):
        headers = {"Content/Type": "application/json"}
        params = {"test": "123"}
        client = RestApiInvoker().make_get_request(
            TestConstants.MOCK_HOST,
            TestConstants.MOCK_URL,
            params=params,
            headers=headers
        )
        assert client is not None
        assert client.method is "GET"
        assert client.params is params
        assert client.header is headers
        assert TestConstants.MOCK_URL in client.url
        assert client.host is TestConstants.MOCK_HOST

    def test_post_client_generator(self):
        headers = {"Content/Type": "application/json"}
        body = "This is a body"
        client = RestApiInvoker().make_post_request(
            TestConstants.MOCK_HOST,
            TestConstants.MOCK_URL,
            headers=headers,
            body=body
        )
        assert client is not None
        assert client.method is "POST"
        assert client.header is headers
        assert TestConstants.MOCK_URL in client.url
        assert client.host is TestConstants.MOCK_HOST
