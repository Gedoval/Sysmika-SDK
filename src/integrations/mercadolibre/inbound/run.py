from .app import create_app


def run_app(dev=True):

    if dev:
        app = create_app()
    else:
        app = create_app(is_dev=False)

    @app.route("/")
    def im_alive():
        return "ElPsyKongroo"

    return app
