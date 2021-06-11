from .app import create_app


def run_app():
    app = create_app(
        cred_file="credentials.example.yml"
    )
    @app.route("/hello")
    def hello():
        return "jello"

    return app
