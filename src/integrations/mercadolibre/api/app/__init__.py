import os
import json
from flask import Flask, request
from src.integrations.mercadolibre.api.mercadolibre_invoker import MercadoLibreAPICaller
from src.integrations.mercadolibre.exceptions.mercadolibre_exceptions import *
from src.integrations.mercadolibre.constants.constants import MercadoLibreConstants as Consts


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr-sqlite"),
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/user/test")
    def create_test_user():
        if not (Consts.TG_CODE or Consts.REDIRECT_URL or Consts.SITE) in request.headers:
            raise MissingHeaders("Missing required headers", 500)
        test_user = MercadoLibreAPICaller(
            api_key="gggggg",
            api_secret="0000000"
        ).create_mercado_libre_test_user(
            request.headers[Consts.TG_CODE],
            request.headers[Consts.REDIRECT_URL],
            request.headers[Consts.SITE]
        )
        return vars(test_user)


    @app.route("/")
    def hello():
        return "ElPsyKongroo"

    return app
