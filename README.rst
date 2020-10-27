flask-simple-geoip
==================

The simplest GeoIP lookup library for Flask.

.. image:: https://raw.githubusercontent.com/whois-api-llc/flask-simple-geoip/master/images/geoip.png

.. image:: https://img.shields.io/pypi/v/flask-simple-geoip.svg
    :alt: flask-simple-geoip Release
    :target: https://pypi.python.org/pypi/flask-simple-geoip

.. image:: https://img.shields.io/travis/whois-api-llc/flask-simple-geoip.svg
    :alt: flask-simple-geoip Build
    :target: https://travis-ci.org/whois-api-llc/flask-simple-geoip


Meta
----
- Author: Randall Degges
- Email: r@rdegges.com
- Twitter: https://twitter.com/rdegges
- Site: http://www.rdegges.com
- Status: production ready


Prerequisites
-------------

To use this library, you'll need to create a free GeoIPify account:
https://geoipify.whoisxmlapi.com/

If you haven't done this yet, please do so now; you will obtain an API
key that will be needed to use the library.



Installation
------------

To install ``flask-simple-geoip`` using `pypi <https://pypi.org/>`_, simply run:

.. code-block:: console

    $ pip install flask-simple-geoip

In the root of your project directory.


Usage
-----

Once you have `flask-simple-geoip` installed, you can use it to easily find the
physical location of a given IP address.

This library gives you access to all sorts of geographical location data that
you can use in your application in any number of ways.

Here's a simple Flask app that makes use of the geolocation lookups:

.. code-block:: python

    from flask import Flask, jsonify
    from flask_simple_geoip import SimpleGeoIP


    app = Flask(__name__)

    # The API key is obtained from the GEOIPIFY_API_KEY environment variable.
    # Alternatively it can be set as follows:
    # app.config.update(GEOIPIFY_API_KEY='YOUR_API_KEY')
    
    # Initialize the extension
    simple_geoip = SimpleGeoIP(app)


    @app.route('/')
    def test():
        # Retrieve geoip data for the given requester
        geoip_data = simple_geoip.get_geoip_data()

        return jsonify(data=geoip_data)

Here's the sort of data you might get back when performing a geoip lookup
request:

.. code-block:: json

    {
      "ip": "8.8.8.8",
      "location": {
        "country": "US",
        "region": "California",
        "city": "Mountain View",
        "lat": 37.40599,
        "lng": -122.078514,
        "postalCode": "94043",
        "timezone": "-08:00"
      }
    }

By default, this library handles retrying failed HTTP requests for you. For
instance: if the GeoIPify API service is currently down or having issues,
your request will be retried up to three consecutive times before failing.

In the event a geoip lookup still can't return successfully, the data returned
will be `None`. This library will *never* throw an exception. This decision was
made strategically: not having geoip data should never be the cause of a failed
request. =)


Changelog
---------

All library changes in descending order.

Version 0.2.4
*************

**Released October 27, 2020.**

- Described in the readme how to supply the API key.


Version 0.2.3
*************

**Released August 26, 2020.**

- Fixed pypy support.

Version 0.2.2
*************

**Released August 24, 2020.**

- Added X_FORWARDED_FOR headers support.

Version 0.1.1
*************

**Released June 18, 2018.**

- Fixing readme so it shows properly on PyPI :(


Version 0.1.0
*************

**Released June 18, 2018.**

- First release!
