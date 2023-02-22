import json
import logging

from scapy.all import *
import geoip2.database
from kafka import KafkaProducer

import click

from .util.extractor import get_geo_info

logging.basicConfig(level=logging.INFO, filename="logs/traffic.log", format="%(asctime)s %(message)s")
logger = logging.getLogger("scapy")
logger.setLevel(logging.INFO)


@click.group()
@click.version_option()
def cli() -> None:
    """Command line interface for the mycorrhizal network."""


@cli.command("monitor_ip")
@click.option("--broker", default="127.0.0.1:9093")
@click.option("--count", default=0)
def monitor_ip(broker: str, count: int) -> None:
    # Initialize the database
    database_reader = geoip2.database.Reader("mycorrhizal_network/data/GeoIP2-City.mmdb")

    # Initialize the Kafka producer
    kafka_producer = KafkaProducer(
        bootstrap_servers=[broker],
        value_serializer=lambda m: json.dumps(m).encode("utf-8"),
    )

    # Define the callback function as to how to process the IP packet
    def print_and_produce_pkt_summary(packet) -> None:

        if IP in packet:
            # Step 1: Get the source and destination IP addresses, which for sure exist.
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst

            # Step 2: Get the geological info, such as city name.
            country_src, city_src, latitude_src, longitude_src = get_geo_info(ip_src, database_reader)
            country_dst, city_dst, latitude_dst, longitude_dst = get_geo_info(ip_dst, database_reader)

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

                logger.info(f"{ip_src} ({city_src}) -> {ip_dst} ({city_dst})")

            except KeyboardInterrupt:
                return
            except ValueError:
                logger.error("Invalid input, discarding record...")
                return
            except Exception as ex:
                logger.error(ex)
                return

    sniff(filter="ip", prn=print_and_produce_pkt_summary, store=0, count=count)

    kafka_producer.flush()
    database_reader.close()


@cli.command("monitor_dns")
@click.option("--broker", default="127.0.0.1:9093")
@click.option("--dns", default="192.168.31.1")
@click.option("--count", default=0)
def monitor_dns(broker: str, dns: str, count: int) -> None:
    # Initialize the database
    database_reader = geoip2.database.Reader("mycorrhizal_network/data/GeoIP2-City.mmdb")

    # Initialize the Kafka producer
    kafka_producer = KafkaProducer(
        bootstrap_servers=[broker],
        value_serializer=lambda m: json.dumps(m).encode("utf-8"),
    )

    # Define the callback function as to how to process the DNS packet
    def print_and_produce_pkt_summary(packet) -> None:
        if UDP in packet and DNS in packet and DNSQR in packet:
            answer = sr1(IP(src="192.168.31.52") / UDP(sport=packet[UDP].sport) / DNS(rd=1, id=packet[DNS].id, qd=DNSQR(qname=packet[DNSQR].qname)), verbose=0)

            # the example answer[DNSRR] might be as below in the format (rdata, rrname):
            # b'clients.l.google.com.' <class 'bytes'> clients4.google.com. <class 'bytes'>
            # 142.250.179.206 <class 'str'> encrypted-tbn0.gstatic.com. <class 'bytes'>
            if DNSRR in answer and not isinstance(answer[DNSRR].rdata, (bytes, bytearray)):

                # Step 1: Get the source and destination IP addresses.
                ip = answer[DNSRR].rdata
                url = answer[DNSRR].rrname.decode("utf-8")

                # Step 2: Store in Kafka cluster
                # Serve on_delivery callbacks from previous calls to produce()
                try:
                    kafka_producer.send(
                        "mapping",
                        {
                            "ip": ip,
                            "url": url,
                        },
                    )

                    logger.info(f"{ip} -> {url}")

                except KeyboardInterrupt:
                    return
                except ValueError:
                    logger.error("Invalid input, discarding record...")
                    return
                except Exception as ex:
                    logger.error(ex)
                    return

    sniff(filter=f"ip dst {dns}", prn=print_and_produce_pkt_summary, store=0, count=count)

    kafka_producer.flush()
    database_reader.close()


if __name__ == "__main__":
    cli()
