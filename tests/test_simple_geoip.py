import pytest

from os import environ
from unittest import TestCase

from flask import Flask, jsonify
from flask_simple_geoip import SimpleGeoIP


class TestSimpleGeoIP(TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_init_fails_with_no_config(self):
        with self.assertRaises(Exception):
            SimpleGeoIP(app)

    def test_init_works_with_environment_variable_config(self):
        environ["GEOIPIFY_API_KEY"] = "test"
        SimpleGeoIP(self.app)
        del environ["GEOIPIFY_API_KEY"]

    def test_init_works_with_environment_variable_config(self):
        self.app.config["GEOIPIFY_API_KEY"] = "test"
        SimpleGeoIP(self.app)

