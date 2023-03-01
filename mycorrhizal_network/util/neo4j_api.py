import logging

logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("default")
logger.setLevel(logging.INFO)

from neo4j._sync.driver import BoltDriver
from dataclasses import asdict
from .ipinfo_crawler import IPInfo


def get_ip_set(neo4j_driver: BoltDriver):
    ip_list = []

    with neo4j_driver.session() as session:
        records, summary = session.execute_read(_get_all_hops)

        logger.info("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after,
        ))

        for record in records:
            hop = record.data()
            ip = hop["n"]["ip"]

            if not ip.startswith("192.168"):
                ip_list.append(hop["n"]["ip"])

    return set(ip_list)


def update_one_hop(neo4j_driver: BoltDriver, info: IPInfo):

    # Overwrite
    if info.ip.startswith("192.168"):
        info = IPInfo(ip=info.ip, country="Ferrix", city="Unidentified Ferrix town", lat="0.0", lon="0.0")

    with neo4j_driver.session() as session:
        summary = session.execute_write(
            _update_one_hop,
            ip=info.ip, country=info.country, region=info.region, city=info.city, isp=info.isp, lat=info.lat, lon=info.lon,
            org=info.org, services=info.services, hostname=info.hostname, asn=info.asn, assignment=info.assignment
        )

        logger.info(f"Updated {asdict(info)} in the database")


def _get_all_hops(tx):
    result = tx.run("MATCH (n:Hop) WHERE n.ip IS NOT NULL WITH DISTINCT (n) RETURN n")

    records = list(result)
    summary = result.consume()

    return records, summary


def _update_one_hop(tx, ip, country, region, city, isp, lat, lon, org, services, hostname, asn, assignment):
    result = tx.run("""
        MATCH (n:Hop {ip: $ip})
        SET n.country=$country, n.region=$region, n.city=$city, n.isp=$isp, n.lat=$lat, n.lon=$lon, n.org=$org, n.services=$services, n.hostname=$hostname, n.asn=$asn, n.assignment=$assignment
        """, ip=ip, country=country, region=region, city=city, isp=isp, lat=lat, lon=lon, org=org, services=services, hostname=hostname, asn=asn, assignment=assignment
    )

    summary = result.consume()

    return summary
