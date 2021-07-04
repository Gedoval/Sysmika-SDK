from src.utils.Utils import SysmikaUtils
import os
import json
from src.integrations.mercadolibre.exceptions.mercadolibre_exceptions import *


class TestSysmikaUtils:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    target_dir = os.path.sep.join(current_dir.split(os.path.sep)[:-2])  # Project root

    def test_json_parser(self):
        data = json.load(open(TestSysmikaUtils.target_dir + "/tests/resources/invalid_grant.json"))
        resp = SysmikaUtils.json_parser(data, AuthTokenGenerationError())
        assert resp is not None
        assert isinstance(resp, AuthTokenGenerationError)
        assert resp.message == "Error validating grant. Your authorization code or refresh token may be expired or it was already used"
        assert resp.status == 400

    def test_json_validator(self):
        data = json.load(open(os.path.sep.join(TestSysmikaUtils.current_dir.split(os.path.sep)[:-1]) + "/resources/sample_sync_event.json"))
        resp = SysmikaUtils.validate_sync_event_schema(data)
        assert resp is True

    def test_json_validator_on_error(self):
        data = {"something": "something"}
        resp = SysmikaUtils.validate_sync_event_schema(data)
        assert resp is False
