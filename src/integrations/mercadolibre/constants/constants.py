class HeaderConstants:
    TG_CODE = "tg-code"
    REDIRECT_URL = "redirect-url"
    SITE = "site-id"
    APP_ID = "app-id"
    APP_SECRET = "app-secret"
    APP_TOKEN = "app-token"
    REFRESH_TOKEN = "refresh-token"
    ITEM_ID = "item-id"


# Endpoints exposed by the MercadoLibre site
class EndpointsConstants(HeaderConstants):
    TOKEN_URL = "/oauth/token"
    TEST_USER_URL = "/users/test_user"
    CATEGORIES = "/categories"
    ATTRIBUTES = "/attributes"
    ITEMS = "/items"
    LOCATION_AR = "/classified_locations/countries/AR"
    LOCATION_STATE_INFO = "/classified_locations/"


# Endpoints for the API exposed by the Sysmika-SDK
class ServiceEndpointsConstants(EndpointsConstants):
    CREATE_TEST_USER = "/user/test"
    GET_ACCESS_TOKEN = "/auth/access_token"
    REFRESH_ACCESS_TOKEN = "/auth/refresh_token"
    CATEGORIES = "/categories"
    CATEGORY_ATTRIBUTES = "/categories/<category_id>"
    CREATE_PUBLICATION = "/publish/create"
    UPDATE_PUBLICATION = "/publish/update"
    DELETE_PUBLICATION = "/publish/delete"
    UPDATE_STATUS = "/publish/update/<status>"
    LOCATION_GET_ARGENTINA = "/location/ar"
    LOCATION_INFO = "/location/<location>/<state_id>"


class UrlConstants(ServiceEndpointsConstants):
    API_HOST = "https://api.mercadolibre.com"


class Constants(UrlConstants):
    # Placeholder, extends the last class added to this file
    pass
