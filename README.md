# Mycorrhizal Network

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
