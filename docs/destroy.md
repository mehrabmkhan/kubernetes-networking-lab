# Cleanup

Remove the lab with:

```bash
kubectl delete -k manifests
```

If the namespace stays behind for any reason, remove it directly:

```bash
kubectl delete namespace k8s-network-lab
```
