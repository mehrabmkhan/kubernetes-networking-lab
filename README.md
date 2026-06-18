# Kubernetes networking lab

This repo holds a small set of Kubernetes manifests for networking work:

- a namespace-scoped sample app
- a ClusterIP service
- an ingress object for `ingress-nginx`
- a default-deny network policy
- an allow rule for ingress traffic to the app
- a traffic-control pod that applies `tc netem`

The manifests are kept deliberately small so they can be read, applied, and adjusted without digging through a large stack.

## Layout

- `manifests/` holds the Kubernetes YAML
- `scripts/validate_manifests.py` checks that the bundle is internally consistent
- `tests/` covers the manifest helpers
- `docs/` contains run notes
- `diagrams/` contains the topology sketch
- `screenshots/` is a placeholder only

## Local setup

```bash
python -m pip install -r requirements-dev.txt
```

## Apply the lab

```bash
kubectl apply -k manifests
kubectl get all -n k8s-network-lab
```

The ingress example expects an `ingress-nginx` controller to be installed in the cluster.

## Validation

```bash
python scripts/validate_manifests.py
pytest
```

## Cleanup

```bash
kubectl delete -k manifests
```
