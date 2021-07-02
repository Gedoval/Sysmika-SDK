from flask import Flask, request
from ..instance import config
from src.integrations.mercadolibre.inbound.invoker_factory import MercadoLibreInvokerFactory
from src.integrations.mercadolibre.exceptions.mercadolibre_exceptions import *
from src.integrations.mercadolibre.constants.constants import Constants as Consts


def create_app(is_dev=True):
    app = Flask(__name__, instance_relative_config=True)
    if is_dev:
        app.config.from_object(config.DevConfig)
    else:
        app.config.from_object(config.ProdConfig)

    """
    Auth Endpoints section
    """

    @app.route(Consts.GET_ACCESS_TOKEN)
    def generate_access_token():
        if not all(key in request.headers for key in (
                Consts.TG_CODE, Consts.REDIRECT_URL, Consts.APP_ID, Consts.APP_SECRET
        )):
            return MissingHeadersError("Missing required headers", 400).to_json()
        invoker = MercadoLibreInvokerFactory.create_invoker(
            app_id=request.headers[Consts.APP_ID],
            app_secret=request.headers[Consts.APP_SECRET]
        )
        try:
            access_token = invoker.get_access_token(
                request.headers[Consts.TG_CODE],
                request.headers[Consts.REDIRECT_URL]
            )
        except AuthTokenGenerationError as e:
            return vars(e)
        return vars(access_token)

    @app.route(Consts.REFRESH_ACCESS_TOKEN)
    def refresh_access_token():
        if not all(key in request.headers for key in (
                Consts.REFRESH_TOKEN, Consts.APP_ID, Consts.APP_SECRET
        )):
            return MissingHeadersError("Missing required headers", 400).to_json()
        invoker = MercadoLibreInvokerFactory.create_invoker(
            app_id=request.headers[Consts.APP_ID],
            app_secret=request.headers[Consts.APP_SECRET]
        )
        try:
            access_token = invoker.refresh_access_token(
                request.headers[Consts.REFRESH_TOKEN]
            )
        except AuthTokenGenerationError as e:
            return vars(e)
        return vars(access_token)

    """
    User Endpoints section
    """

    @app.route(Consts.CREATE_TEST_USER)
    def create_test_user():
        if not all(key in request.headers for key in (
                Consts.APP_TOKEN, Consts.SITE
        )):
            return MissingHeadersError("Missing required headers", 400).to_json()
        invoker = MercadoLibreInvokerFactory.create_invoker()
        try:
            test_user = invoker.create_mercado_libre_test_user(
                request.headers[Consts.APP_TOKEN],
                request.headers[Consts.SITE]
            )
        except UserCreationError as e:
            return vars(e)
        return vars(test_user)

    """
    Categories Endpoints  section
    """

    @app.route(Consts.CATEGORIES)
    def get_inmobiliaria_categories_tree():
        invoker = MercadoLibreInvokerFactory.create_invoker()
        return invoker.get_categories()

    @app.route(Consts.CATEGORY_ATTRIBUTES)
    def get_inmobiliaria_category_description(category_id):
        invoker = MercadoLibreInvokerFactory().create_invoker()
        return invoker.get_category_attributes(category_id)

    """
    Publication Endpoints section
    """

    @app.route(Consts.CREATE_PUBLICATION, methods=['POST'])
    def post_real_state_publication():
        if Consts.APP_TOKEN not in request.headers:
            return MissingHeadersError("Missing required headers", 400).to_json()
        invoker = MercadoLibreInvokerFactory.create_invoker(
            app_token=request.headers[Consts.APP_TOKEN]
        )
        try:
            response = invoker.post_real_state_publication(request.json)
        except PublicationError as e:
            return vars(e)
        return vars(response)

    @app.route(Consts.UPDATE_PUBLICATION, methods=['PUT'])
    def put_update_real_state_publication():
        if not all(key in request.headers for key in (
            Consts.APP_TOKEN, Consts.ITEM_ID
        )):
            return MissingHeadersError("Missing required headers", 400).to_json()
        invoker = MercadoLibreInvokerFactory.create_invoker(
            app_token=request.headers[Consts.APP_TOKEN]
        )
        try:
            response = invoker.put_update_real_state_publication(request.json, request.headers[Consts.ITEM_ID])
        except PublicationError as e:
            return vars(e)
        return vars(response)

    @app.route(Consts.UPDATE_STATUS,  methods=['PUT'])
    def put_update_publication_status(status):
        if not all(key in request.headers for key in (
            Consts.APP_TOKEN, Consts.ITEM_ID
        )):
            return MissingHeadersError("Missing required headers", 400).to_json()
        if status not in ["paused", "active", "closed"]:
            return MissingQueryParameterError("The status sent is not allowed", 400).to_json()
        invoker = MercadoLibreInvokerFactory.create_invoker(
            app_token=request.headers[Consts.APP_TOKEN]
        )
        try:
            response = invoker.put_update_real_state_publication(request.json, request.headers[Consts.ITEM_ID], status)
        except PublicationError as e:
            return vars(e)
        return vars(response)

    @app.route(Consts.DELETE_PUBLICATION, methods=['DELETE'])
    def delete_real_state_publication():
        if not all(key in request.headers for key in (
                Consts.APP_TOKEN, Consts.ITEM_ID
        )):
            return MissingHeadersError("Missing required headers", 400).to_json()
        invoker = MercadoLibreInvokerFactory.create_invoker(
            app_token=request.headers[Consts.APP_TOKEN]
        )
        try:
            response = invoker.delete_publication(request.headers[Consts.ITEM_ID])
        except PublicationError as e:
            return vars(e)
        return vars(response)

    """
    Location Endpoints section
    """
    @app.route(Consts.LOCATION_GET_ARGENTINA)
    def get_argentina_locations_id():
        response = MercadoLibreInvokerFactory.create_invoker().get_argentina_locations_id()
        return response

    @app.route(Consts.LOCATION_INFO)
    def get_location_info(location, state_id):
        response = MercadoLibreInvokerFactory.create_invoker().get_location_info(location, state_id)
        return response

    return app
