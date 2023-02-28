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

            # If "region" exists, it means that the info of the given "ip" has already been checked in "ipinfo.io".
            if "region" not in hop["n"]:
                ip_list.append(hop["n"]["ip"])

    return set(ip_list)


def update_one_hop(neo4j_driver: BoltDriver, ip: str, info: IPInfo):

    # Overwrite
    if ip.startswith("192.168"):
        info = IPInfo(ip=ip, country="Ferrix", city="Unidentified Ferrix town", lat="0.0", lon="0.0")

    with neo4j_driver.session() as session:
        summary = session.execute_write(
            _update_one_hop,
            ip=ip, country=info.country, region=info.region, city=info.city, isp=info.isp, org=info.org, lat=info.lat,
            lon=info.lon
        )

        logger.info(f"Updated {asdict(info)} in the database")


def _get_all_hops(tx):
    result = tx.run("MATCH (n:Hop) WITH DISTINCT (n) RETURN n")

    records = list(result)
    summary = result.consume()

    return records, summary


def _update_one_hop(tx, ip, country, region, city, isp, org, lat, lon):
    result = tx.run("""
            MATCH (n:Hop {ip: $ip})
            SET n.country=$country, n.region=$region, n.city=$city, n.isp=$isp, n.org=$org, n.lat=$lat, n.lon=$lon
            """, ip=ip, country=country, region=region, city=city, isp=isp, org=org, lat=lat, lon=lon
                    )

    summary = result.consume()

    return summary
