import pytest

from os import environ
from unittest import TestCase

from flask import Flask, request
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

    def test_get_geoip_data_for_custom_addr(self):
        with self.app.test_request_context():
            simple_geoip = SimpleGeoIP(self.app)
            data = simple_geoip.get_geoip_data('8.8.8.8')
            self.assertIsInstance(data, dict)
            self.assertEqual(data['ip'], '8.8.8.8')

    def test_get_geoip_data_for_x_forwarded_for(self):
        with self.app.test_request_context(environ_base={'HTTP_X_FORWARDED_FOR': '1.2.3.4'}):
            simple_geoip = SimpleGeoIP(self.app)
            data = simple_geoip.get_geoip_data()
            self.assertIsInstance(data, dict)
            self.assertEqual(data['ip'], '1.2.3.4')

    def test_get_geoip_data_with_multiple_proxies(self):
        with self.app.test_request_context(environ_base={'HTTP_X_FORWARDED_FOR': '1.2.3.4, 1.2.3.5, 1.2.3.6, 1.2.3.7'}):
            simple_geoip = SimpleGeoIP(self.app)
            data = simple_geoip.get_geoip_data()
            self.assertIsInstance(data, dict)
            self.assertEqual(data['ip'], '1.2.3.4')

    def test_get_geoip_data_with_malformed_x_forwarded_for(self):
        environ_base = {
            'REMOTE_ADDR': '127.0.0.1',
            'HTTP_X_FORWARDED_FOR': '<script> alert(1) </script'
        }

        with self.app.test_request_context(environ_base=environ_base):
            simple_geoip = SimpleGeoIP(self.app)
            data = simple_geoip.get_geoip_data()
            self.assertIsInstance(data, dict)
            self.assertEqual(data['ip'], request.remote_addr)
