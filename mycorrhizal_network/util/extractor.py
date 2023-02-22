import logging

from geoip2.errors import AddressNotFoundError

logger = logging.getLogger("scapy")
logger.setLevel(logging.INFO)


def get_geo_info(ip: str, database_reader) -> (str, str, str, str):

    # Neo4j does not store null properties.
    # The example returned result might be:
    # ("country", "city", "lon", "lat"), (None, None, "lon", "lat"), or (None, None, None, None).
    if ip.startswith("192.168"):
        country, city, latitude, longitude = get_local_geo_info()
    else:
        country, city, latitude, longitude = get_geo_info_from_database(ip, database_reader)

    return country, city, latitude, longitude


def get_local_geo_info() -> (str, str, str, str):

    return "Netherlands", "Utrecht", "52.0908", "5.1222"


def get_geo_info_from_database(ip: str, database_reader) -> (str, str, str, str):

    try:
        result = database_reader.city(ip)

        # The result might be partial, e.g., with only country.
        # The not-found properties are of NoneType.
        country = result.country.name
        city = result.city.name
        latitude = result.location.latitude
        longitude = result.location.longitude

        return country, city, latitude, longitude

    except AddressNotFoundError as ex:
        # If the IP address is not found in the database, then keep its geological info as None.
        logger.debug(ex)
        return None, None, None, None


