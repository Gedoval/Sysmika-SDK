import json
import sys


class SysmikaUtils:

    @staticmethod
    def json_parser(json_data, obj):
        field_names = [a for a in dir(obj) if not a.startswith('__') and not callable(getattr(obj, a))]
        for field in field_names:
            try:
                setattr(obj, field, json_data[field])
            except (KeyError, ValueError) as e:
                pass
        return obj

    @staticmethod
    def flask_data_parser(data):
        return data.decode('UTF-8').replace('\n', '')

