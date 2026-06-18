from pathlib import Path

from scripts.validate_manifests import validate


def test_manifest_bundle_validates():
    assert validate() == []


def test_kustomization_exists():
    assert Path("manifests/kustomization.yaml").exists()
