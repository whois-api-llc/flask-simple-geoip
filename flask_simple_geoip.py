from os import environ

from simple_geoip import GeoIP
from flask import request

CONFIG_KEY = "GEOIPIFY_API_KEY"
import ipaddress


class SimpleGeoIP(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        api_key = app.config.get(CONFIG_KEY) or environ.get(CONFIG_KEY)
        if not api_key:
            raise Exception(
                "No API key was supplied for performing GeoIP lookups. Please set a value for GEOIPIFY_API_KEY.")

        self.geoip_client = GeoIP(api_key)

    def get_geoip_data(self, remote_addr=None):
        """
        Performs a geoip lookup based on the requester's public IP address.

        NOTE: This method will *always* return and never raise an exception --
        it does this strategically because performing a geoip lookup should
        never be a tier 1 stop-the-world exception.

        :param remote_addr:  IPv4 or IPv6 to search location by.
                             If None, it defaults to the request's public IP address
            :type remote_addr: str or None

        :rtype: dict or None
        :returns: A dictionary containing the user's geolocation data, or None
            if there was a problem.
        """

        remote_addr = remote_addr if remote_addr else self.__resolve_remote_addr()

        try:
            data = self.geoip_client.lookup(remote_addr)

        # Don't do anything if an exception arises -- since geolocation data isn't
        # critical to a request being processed, we can always skip it in the worst
        # case scenario.
        #
        # By default, the underlying `simple_geoip` library will handle retry logic
        # for us ;)
        except:
            data = None

        return data

    def __resolve_remote_addr(self):
        if request.environ.get('HTTP_X_FORWARDED_FOR') is not None:
            x_forwarded_for = request.environ['HTTP_X_FORWARDED_FOR'].split(',')
            addr = x_forwarded_for[0]
            try:
                ipaddress.ip_address(addr)
                return addr
            except:
                pass

        return request.remote_addr
