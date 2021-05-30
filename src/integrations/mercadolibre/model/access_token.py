import ast


class AccessToken:
    def __init__(self):
        self.access_token = None
        self.token_type = None
        self.expires_in = 0
        self.scope = None
        self.user_id = None
        self.refresh_token = None

    @staticmethod
    def json_parser(json_data):
        result = AccessToken()
        field_names = [a for a in dir(result) if not a.startswith('__') and not callable(getattr(result, a))]
        data = ast.literal_eval(json_data)

        for field in field_names:
            setattr(result, field, data[field])
        return result
