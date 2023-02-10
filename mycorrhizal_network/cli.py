import json
import logging

import geoip2.database
from kafka import KafkaProducer

logger = logging.getLogger("scapy")
logger.setLevel(logging.INFO)

import click
from scapy.all import *

from .util.extractor import get_geo_info


@click.group()
@click.version_option()
def cli() -> None:
    """Command line interface for the mycorrhizal network."""


@cli.command()
@click.option("--broker", default="127.0.0.1:9093")
@click.option("--count", default=0)
def monitor(broker: str, count: int) -> None:

    # Initialize the database
    database_reader = geoip2.database.Reader(
        "mycorrhizal_network/data/GeoIP2-City.mmdb"
    )

    # Initialize the Kafka producer
    kafka_producer = KafkaProducer(
        bootstrap_servers=[broker],
        value_serializer=lambda m: json.dumps(m).encode("utf-8"),
    )

    # Define the callback function as to how to process the packet
    def print_and_produce_pkt_summary(packet) -> None:

        if IP in packet:
            # Step 1: Get the source and destination IP addresses.
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst

            # Step 2: Get the geological info, such as city name.
            country_src, city_src, latitude_src, longitude_src = get_geo_info(
                ip_src, database_reader
            )
            country_dst, city_dst, latitude_dst, longitude_dst = get_geo_info(
                ip_dst, database_reader
            )

            # Step 3: Store in Kafka cluster
            # Serve on_delivery callbacks from previous calls to produce()
            try:
                kafka_producer.send(
                    "traffic",
                    {
                        "ip_src": str(ip_src),
                        "country_src": country_src,
                        "city_src": city_src,
                        "latitude_src": latitude_src,
                        "longitude_src": longitude_src,
                        "ip_dst": str(ip_dst),
                        "country_dst": country_dst,
                        "city_dst": city_dst,
                        "latitude_dst": latitude_dst,
                        "longitude_dst": longitude_dst,
                    },
                )

                print(
                    "{0} ({1}) -> {2} ({3})".format(ip_src, city_src, ip_dst, city_dst)
                )

            except KeyboardInterrupt:
                return
            except ValueError:
                print("Invalid input, discarding record...")
                return

    sniff(filter="ip", prn=print_and_produce_pkt_summary, store=0, count=count)

    kafka_producer.flush()
    database_reader.close()


if __name__ == "__main__":
    cli()
