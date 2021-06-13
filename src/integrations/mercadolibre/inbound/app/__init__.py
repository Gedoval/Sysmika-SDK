import sys

from flask import Flask, request
from ..instance import config
from src.integrations.mercadolibre.invoker.mercadolibre_invoker import MercadoLibreAPICaller
from src.integrations.mercadolibre.exceptions.mercadolibre_exceptions import *
from src.integrations.mercadolibre.constants.constants import Constants as Consts


def create_app(cred_file=None, is_dev=True):
    app = Flask(__name__, instance_relative_config=True)
    if is_dev:
        app.config.from_object(config.DevConfig)
    else:
        app.config.from_object(config.ProdConfig)

    if cred_file is not None:
        invoker = MercadoLibreAPICaller(cred_file=cred_file)
    else:
        invoker = MercadoLibreAPICaller()

    """
    Endpoints section
    """

    @app.route(Consts.CREATE_TEST_USER)
    def create_test_user():
        if not (Consts.APP_TOKEN or Consts.SITE) in request.headers:
            raise MissingHeadersError("Missing required headers", 500)
        test_user = invoker.create_mercado_libre_test_user(
            request.headers[Consts.APP_TOKEN],
            request.headers[Consts.SITE]
        )
        return vars(test_user)

    @app.route(Consts.GET_ACCESS_TOKEN)
    def generate_access_token():
        if not (Consts.TG_CODE or Consts.REDIRECT_URL) in request.headers:
            raise MissingHeadersError("Missing required headers", 500)
        access_token = invoker.get_access_token(
            request.headers[Consts.TG_CODE],
            request.headers[Consts.REDIRECT_URL]
        )
        return vars(access_token)

    @app.route(Consts.REFRESH_ACCESS_TOKEN)
    def refresh_access_token():
        if Consts.REFRESH_TOKEN not in request.headers:
            raise MissingHeadersError("Missing required header", 500)
        access_token = invoker.refresh_access_token(
            request.headers[Consts.REFRESH_TOKEN]
        )
        return vars(access_token)

    return app
