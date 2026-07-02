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

CI runs the same validation on pushes and pull requests that change manifests, scripts, tests, dependency files, or the workflow itself. The workflow can also be started manually from GitHub Actions when a fresh validation signal is needed without changing lab code.
