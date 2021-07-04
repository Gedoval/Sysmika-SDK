import os
import json
from jsonschema import validate, ValidationError

class SysmikaUtils:

    current_dir = os.path.dirname(os.path.realpath(__file__))
    target_dir = os.path.sep.join(current_dir.split(os.path.sep)[:-1])
    schema_path = target_dir + "/integrations/mercadolibre/inbound/specs/schemas/sync_event.json"

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

    """
    Returns false if the json does not comply to the schema
    """
    @staticmethod
    def validate_sync_event_schema(data):
        remove = ("$id", "$schema", "description", "title")
        schema = json.load(open(SysmikaUtils.schema_path))
        for k in remove:
            schema.pop(k, None)
        try:
            validate(instance=data, schema=schema)
        except ValidationError:
            return False
        return True
