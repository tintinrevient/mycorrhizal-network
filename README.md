# Mycorrhizal Network

## Prerequisite

* Kubernetes 1.18+
* Helm 3.0+ ([installing helm](https://helm.sh/docs/intro/install/))

## Environment

1. Install the `Kafka` cluster with the `Neo4j` database with `helm`:
```bash
$ helm repo add datadoor https://tintinrevient.github.io/helm-chart
$ helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "datadoor" chart repository
Update Complete. ⎈Happy Helming!⎈

$ helm search repo datadoor
NAME                    	CHART VERSION	APP VERSION	DESCRIPTION
datadoor/data-door-chart	0.1.0        	1.16.0     	A Helm chart for Kubernetes

$ helm install data-door-release datadoor/data-door-chart --namespace "data-door"
```

2. When finished, the environment can be cleaned up by the following command:
```bash
$ helm uninstall data-door-release --namespace "data-door"
```

## References
* https://en.wikipedia.org/wiki/Mycorrhizal_network
