class MercadoLibreError(Exception):
    pass


class AuthTokenGenerationError(MercadoLibreError):
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message
