from os import environ

from simple_geoip import GeoIP
from flask import request


CONFIG_KEY = "GEOIPIFY_API_KEY"


class SimpleGeoIP(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        api_key = app.config.get(CONFIG_KEY) or environ.get(CONFIG_KEY)
        if not api_key:
            raise Exception("No API key was supplied for performing GeoIP lookups. Please set a value for GEOIPIFY_API_KEY.")

        self.geoip_client = GeoIP(api_key)

    def get_geoip_data(self):
        """
        Performs a geoip lookup based on the requester's public IP address.

        NOTE: This method will *always* return and never raise an exception --
        it does this strategically because performing a geoip lookup should
        never be a tier 1 stop-the-world exception.

        :rtype: dict or None
        :returns: A dictionary containing the user's geolocation data, or None
            if there was a problem.
        """
        try:
            data = self.geoip_client.lookup(request.remote_addr)

        # Don't do anything if an exception arises -- since geolocation data isn't
        # critical to a request being processed, we can always skip it in the worst
        # case scenario.
        #
        # By default, the underlying `simple_geoip` library will handle retry logic
        # for us ;)
        except:
            data = None

        return data
