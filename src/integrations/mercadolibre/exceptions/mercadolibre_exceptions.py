class MercadoLibreError(Exception):
    pass


class AuthTokenGenerationError(MercadoLibreError):
    def __init__(self):
        self.status = None
        self.message = None
        self.error = None
        self.cause = None


class MissingHeadersError(MercadoLibreError):
    def __init__(self, message, status):
        self.status = status
        self.message = message
