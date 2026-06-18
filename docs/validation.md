# Validation

Run the checks from the repo root:

```bash
python scripts/validate_manifests.py
pytest
```

The validation script checks the manifest bundle for:

- the expected files in the kustomization
- required Kubernetes resource fields
- service and ingress wiring
- the traffic-control capability flag
