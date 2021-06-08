import ast


class SysmikaUtils:

    @staticmethod
    def json_parser(json_data, obj):
        field_names = [a for a in dir(obj) if not a.startswith('__') and not callable(getattr(obj, a))]
        data = ast.literal_eval(json_data)
        for field in field_names:
            try:
                setattr(obj, field, data[field])
            except KeyError:
                continue
        return obj
