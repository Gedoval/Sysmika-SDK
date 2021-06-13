class HeaderConstants:

    TG_CODE = "tg_code"
    REDIRECT_URL = "redirect_url"
    SITE = "site_id"
    APP_ID = "app_id"
    APP_SECRET = "app_secret"
    APP_TOKEN = "app_token"
    REFRESH_TOKEN = "refresh_token"


# Endpoints exposed by the MercadoLibre site
class EndpointsConstants(HeaderConstants):

    TOKEN_URL = "/oauth/token"
    TEST_USER_URL = "/users/test_user"


# Endpoints for the API exposed by the Sysmika-SDK

class ServiceEndpointsConstants(EndpointsConstants):
    CREATE_TEST_USER = "/user/test"
    GET_ACCESS_TOKEN = "/auth/access_token"
    REFRESH_ACCESS_TOKEN = "/auth/refresh_token"


class UrlConstants(ServiceEndpointsConstants):

    API_HOST = "https://api.mercadolibre.com"


class Constants(UrlConstants):
    # Placeholder, extends the last class added to this file
    pass
