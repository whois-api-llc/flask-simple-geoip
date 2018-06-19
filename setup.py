"""
Flask-Simple-GeoIP
------------------

The simplest GeoIP lookup library for Flask.
"""


from setuptools import setup


setup(
    name="Flask-Simple-GeoIP",
    version="0.1.0",
    url="https://github.com/whois-api-llc/flask-simple-geoip",
    license="BSD",
    author="Randall Degges",
    author_email="r@rdegges.com",
    description="The simplest GeoIP lookup library for Flask.",
    long_description=__doc__,
    py_modules=["flask_simple_geoip"],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=["Flask", "simple-geoip"],
    extras_require={
        "test": ["pytest"],
    },
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
