import json


class MercadoLibreError(BaseException):
    def __init__(self):
        self.status = None
        self.message = None
        self.error = None
        self.cause = None

    def to_json(self):
        return json.dumps(self.__dict__)


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


class UserCreationError(MercadoLibreError):
    pass


class MissingQueryParameterError(MercadoLibreError):
    def __init__(self, message, status):
        self.status = status
        self.message = message


class PublicationError(MercadoLibreError):
    pass