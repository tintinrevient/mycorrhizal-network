# Mycorrhizal Network

## Overview

<p float="left">
    <img src="pix/mycorrhizal-network-infrastructure.png" width="800" />
</p>

## Prerequisite

* Kubernetes 1.18+
* Helm 3.0+ ([installing helm](https://helm.sh/docs/intro/install/))
* Python 3.9
* Poetry ([installing poetry](https://python-poetry.org/))

## Part 1 🧠 - Install the `Kafka` cluster with `neo4j`

<ins>**Ensure that the server has at least `8GB` memory for Docker**</ins>

0. Create a namespace `data-door`:
```bash
kubectl create namespace data-door
```

1. Install the `Kafka` cluster with the `neo4j` database:
```bash
helm repo add datadoor https://tintinrevient.github.io/helm-chart
helm repo update
helm install data-door-release datadoor/data-door-chart --namespace "data-door"
```

2. Expose the following four services in the host machine:
```bash
kubectl port-forward svc/external-broker -n data-door 9093:9093 --address='0.0.0.0'
kubectl port-forward svc/control-center -n data-door 9021:9021
kubectl port-forward svc/neo4j -n data-door 7687:7687
kubectl port-forward svc/neo4j-web -n data-door 7474:7474
```

3. Access the control center via http://localhost:9021/ and create [this Neo4j connector](ksql/neo4j_traffic_sink.sql) in ksqlDB.

4. When finished, the environment can be nuked by the following command:
```bash
$ helm uninstall data-door-release --namespace "data-door"
```

## Part 2 🐙 - Install the `Kafka` producer with `scapy` 

1. Install all the dependencies:
```bash
poetry install
```

2. Run the packet sniffer to capture and dissect IP frame:
```bash
poetry run network monitor_ip --broker="[local IP address of your exposed external Kafka broker]:9093"
```

3. Run the packet sniffer to capture and dissect DNS message:
```bash
poetry run network monitor_dns --broker="[local IP address of your exposed external Kafka broker]:9093" --dns="[dns server]"
```

## Result

1. Access the Neo4j UI via http://localhost:7474/browser/ and commit the test query `MATCH p=(src)-[:TO]->(dst) RETURN p LIMIT 25;`, the following graph will display:
<p float="left">
    <img src="pix/neo4j.png" width="800" />
</p>

2. It can be also viewed in neovis via [this html](neovis/network.html) after configuring your neo4j URL:
<p float="left">
    <img src="pix/neovis.png" width="700" />
</p>

## References
* https://en.wikipedia.org/wiki/Mycorrhizal_network
