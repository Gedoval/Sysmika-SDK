from src.integrations.mercadolibre.inbound.run import run_app

# Gunicorn command to start the Flask app: gunicorn --bind 0.0.0.0:5000 'wsgi:run_app()'

# Gunicorn using gevent workers: gunicorn --bind 0.0.0.0:5000 'wsgi:run_app()' -k gevent --worker-connections 1000

if __name__ == "__main__":
    run_app()
