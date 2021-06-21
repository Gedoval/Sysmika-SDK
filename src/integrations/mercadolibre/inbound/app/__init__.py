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
        if not (Consts.TG_CODE or Consts.REDIRECT_URL or Consts.APP_ID or Consts.APP_SECRET) in request.headers:
            raise MissingHeadersError("Missing required headers", 400)
        invoker = MercadoLibreInvokerFactory.create_invoker(
            app_id=request.headers[Consts.APP_ID],
            app_secret=request.headers[Consts.APP_SECRET]
        )
        access_token = invoker.get_access_token(
            request.headers[Consts.TG_CODE],
            request.headers[Consts.REDIRECT_URL]
        )
        return vars(access_token)

    @app.route(Consts.REFRESH_ACCESS_TOKEN)
    def refresh_access_token():
        if (Consts.REFRESH_TOKEN or Consts.APP_ID or Consts.APP_SECRET) not in request.headers:
            raise MissingHeadersError("Missing required header", 400)
        invoker = MercadoLibreInvokerFactory.create_invoker(
            app_id=request.headers[Consts.APP_ID],
            app_secret=request.headers[Consts.APP_SECRET]
        )
        access_token = invoker.refresh_access_token(
            request.headers[Consts.REFRESH_TOKEN]
        )
        return vars(access_token)

    """
    User Endpoints section
    """

    @app.route(Consts.CREATE_TEST_USER)
    def create_test_user():
        invoker = MercadoLibreInvokerFactory.create_invoker()
        if not (Consts.APP_TOKEN or Consts.SITE) in request.headers:
            raise MissingHeadersError("Missing required headers", 400)
        test_user = invoker.create_mercado_libre_test_user(
            request.headers[Consts.APP_TOKEN],
            request.headers[Consts.SITE]
        )
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

    @app.route(Consts.PUBLISH, methods=['POST'])
    def post_real_state_publication():
        invoker = MercadoLibreInvokerFactory.create_invoker()
        if Consts.APP_TOKEN not in request.headers:
            raise MissingHeadersError("Missing required headers: App Token", 400)
        return invoker.post_real_state_publication()

    return app
