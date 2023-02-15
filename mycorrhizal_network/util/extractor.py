import logging

from geoip2.errors import AddressNotFoundError

logger = logging.getLogger("scapy")
logger.setLevel(logging.INFO)


def get_geo_info(ip: str, database_reader) -> (str, str, str, str):
    country, city, latitude, longitude = ("None", "None", "None", "None")

    try:
        if ip.startswith("192.168"):
            country, city, latitude, longitude = get_local_geo_info()
        else:
            country, city, latitude, longitude = get_geo_info_from_database(ip, database_reader)
    except AddressNotFoundError as ex:
        # If the IP address is not found in the database, then keep its geological info as None.
        logger.debug(ex)

    return country, city, latitude, longitude


def get_local_geo_info() -> (str, str, str, str):

    return "Netherlands", "Utrecht", "52.0908", "5.1222"


def get_geo_info_from_database(ip: str, database_reader) -> (str, str, str, str):

    result = database_reader.city(ip)

    country = result.country.name if result.country.name else None
    city = result.city.name if result.city.name else None
    latitude = result.location.latitude if result.location.latitude else None
    longitude = result.location.longitude if result.location.longitude else None

    return country, city, latitude, longitude
