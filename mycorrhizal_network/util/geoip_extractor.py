import logging

from geoip2.errors import AddressNotFoundError
from dataclasses import dataclass

logger = logging.getLogger("scapy")
logger.setLevel(logging.INFO)


@dataclass
class GeoIP(object):
    country: str
    city: str
    lat: str
    lon: str


def get_geoip_info(ip: str, database_reader) -> GeoIP:

    # Neo4j does not store null properties.
    # The example returned result might be:
    # ("country", "city", "lon", "lat"), (None, None, "lon", "lat"), or (None, None, None, None).
    if ip.startswith("192.168"):
        return get_local_geoip_info()
    else:
        return get_geoip_info_from_database(ip, database_reader)


def get_local_geoip_info() -> GeoIP:

    return GeoIP(country="Ferrix", city="Unidentified Ferrix town", lat="0.0", lon="0.0")


def get_geoip_info_from_database(ip: str, database_reader) -> GeoIP:

    try:
        result = database_reader.city(ip)

        # The result might be partial, e.g., with only country.
        # The not-found properties are of NoneType.
        country = result.country.name
        city = result.city.name
        lat = result.location.latitude
        lon = result.location.longitude

        return GeoIP(country=country, city=city, lat=lat, lon=lon)

    except AddressNotFoundError as ex:
        # If the IP address is not found in the database, then keep its geological info as None.
        logger.debug(ex)
        return None


