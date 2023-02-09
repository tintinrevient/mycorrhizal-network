# Mycorrhizal Network

## Prerequisite

* Kubernetes 1.18+
* Helm 3.0+ ([installing helm](https://helm.sh/docs/intro/install/))

## Environment

0. Create a namespace `data-door`:
```bash
kubectl create namespace data-door
```

1. Install the `Kafka` cluster with the `Neo4j` database:
```bash
helm repo add datadoor https://tintinrevient.github.io/helm-chart
helm repo update
helm install data-door-release datadoor/data-door-chart --namespace "data-door"
```

2. When finished, the environment can be cleaned up by the following command:
```bash
$ helm uninstall data-door-release --namespace "data-door"
```

## References
* https://en.wikipedia.org/wiki/Mycorrhizal_network
