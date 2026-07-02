# Architecture

The lab is built around one namespace, `k8s-network-lab`.

The app runs as a small Deployment behind a ClusterIP Service. Ingress traffic enters through `ingress-nginx`, hits the Service, and lands on the app pods. A default-deny NetworkPolicy closes the namespace down, and a narrower allow policy opens only the path needed for the ingress controller.

The traffic-control example is a single pod with `NET_ADMIN` capability. It applies a `tc netem` rule so you can see latency and loss handling without having to build a separate node-level setup.

## Design boundaries

This is a learning lab, not a production cluster baseline. It does not install an ingress controller, certificate manager, observability stack, or cloud load balancer. Those pieces are intentionally left outside the repository so the networking behavior in the manifests stays easy to inspect.
