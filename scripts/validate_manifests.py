from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = [
    ROOT / "manifests" / "namespace.yaml",
    ROOT / "manifests" / "app" / "deployment.yaml",
    ROOT / "manifests" / "app" / "service.yaml",
    ROOT / "manifests" / "ingress" / "ingress.yaml",
    ROOT / "manifests" / "policies" / "default-deny.yaml",
    ROOT / "manifests" / "policies" / "allow-ingress.yaml",
    ROOT / "manifests" / "traffic-control" / "netem-pod.yaml",
]


def load_manifest(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not parse as a single YAML document")
    return data


def validate() -> list[str]:
    errors: list[str] = []

    kustomization = yaml.safe_load((ROOT / "manifests" / "kustomization.yaml").read_text(encoding="utf-8"))
    expected_resources = [
        "namespace.yaml",
        "app/deployment.yaml",
        "app/service.yaml",
        "ingress/ingress.yaml",
        "policies/default-deny.yaml",
        "policies/allow-ingress.yaml",
        "traffic-control/netem-pod.yaml",
    ]
    if kustomization.get("resources") != expected_resources:
        errors.append("kustomization.yaml resource list does not match the checked set")

    for path in MANIFESTS:
        manifest = load_manifest(path)
        for field in ("apiVersion", "kind", "metadata"):
          if field not in manifest:
            errors.append(f"{path.name} is missing {field}")
        metadata = manifest.get("metadata", {})
        if not metadata.get("name"):
            errors.append(f"{path.name} is missing metadata.name")

    deployment = load_manifest(ROOT / "manifests" / "app" / "deployment.yaml")
    service = load_manifest(ROOT / "manifests" / "app" / "service.yaml")
    ingress = load_manifest(ROOT / "manifests" / "ingress" / "ingress.yaml")
    traffic_pod = load_manifest(ROOT / "manifests" / "traffic-control" / "netem-pod.yaml")

    if deployment["spec"]["selector"]["matchLabels"].get("app") != "network-lab":
        errors.append("deployment selector is not wired to app=network-lab")
    if service["spec"]["selector"].get("app") != "network-lab":
        errors.append("service selector is not wired to app=network-lab")
    backend = ingress["spec"]["rules"][0]["http"]["paths"][0]["backend"]["service"]
    if backend.get("name") != "network-lab" or backend.get("port", {}).get("number") != 80:
        errors.append("ingress backend is not wired to the network-lab service")
    capabilities = traffic_pod["spec"]["containers"][0]["securityContext"]["capabilities"]["add"]
    if "NET_ADMIN" not in capabilities:
        errors.append("traffic-control pod does not request NET_ADMIN")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        return 1
    print("Manifest validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
