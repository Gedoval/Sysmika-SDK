from .app import create_app


def run_app(dev=True):

    if dev:
        app = create_app(cred_file="credentials.example.yml")
    else:
        app = create_app(cred_file="credentials.yml")

    @app.route("/")
    def im_alive():
        return "ElPsyKongroo"

    return app
