import pytest

from os import environ
from unittest import TestCase

from flask import Flask
from flask_simple_geoip import SimpleGeoIP


class TestSimpleGeoIP(TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_init_fails_with_no_config(self):
        api_key = environ.get("GEOIPIFY_API_KEY")
        if api_key:
            del environ["GEOIPIFY_API_KEY"]

        with self.assertRaises(Exception):
            SimpleGeoIP(app)

        if api_key:
            environ["GEOIPIFY_API_KEY"] = api_key

    def test_init_works_with_environment_variable_config(self):
        environ["GEOIPIFY_API_KEY"] = "test"
        SimpleGeoIP(self.app)
        del environ["GEOIPIFY_API_KEY"]

    def test_init_works_with_environment_variable_config(self):
        self.app.config["GEOIPIFY_API_KEY"] = "test"
        SimpleGeoIP(self.app)

        del self.app.config["GEOIPIFY_API_KEY"]

    def test_get_geoip_data(self):
        with self.app.test_request_context():
            simple_geoip = SimpleGeoIP(self.app)
            data = simple_geoip.get_geoip_data()
            self.assertIsInstance(data, dict)
