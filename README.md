# kubeflow-playground

## prerequisites

- [Rancher Desktop](https://github.com/rancher-sandbox/rancher-desktop): `1.9.0`
- Kubernetes: `v1.25.10`
- kubectl `v1.26.0`
- Helm: `v3.11.2`
- [kustomize](https://github.com/kubernetes-sigs/kustomize): `v5.1.0`
- [PDM](https://pdm.fming.dev/latest/)

## setup

### install kubeflow

`./scripts/install.sh`

### local dev

`pdm install`

## playground

visit [kubeflow web ui](http://localhost:8080) after port-forwarding with credential

```sh
email: user@example.com
password: 12341234
```

### ping

```sh
$ pdm run kubeflow_playground/ping.py | jq -c '.[].name'

"[Demo] XGBoost - Iterative model training"
"[Demo] TFX - Taxi tip prediction model trainer"
"[Tutorial] Data passing in python components"
"[Tutorial] DSL - Control structures"
```

```sh
kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80
```

## cleanup

TODO:
