from src.integrations.mercadolibre.invoker.mercadolibre_invoker import MercadoLibreAPICaller


class MercadoLibreInvokerFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_invoker(app_id=None, app_secret=None):
        return MercadoLibreAPICaller(app_id=app_id, app_secret=app_secret)
