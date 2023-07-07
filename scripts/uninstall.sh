pushd manifests
kustomize build example | awk '!/well-defined/' | kubectl delete -f -
kubectl delete all --all -n kubeflow-user-example-com
kubectl delete namespace kubeflow-user-example-com
kubectl patch ns knative-serving -p '{"metadata":{"finalizers":null}}'
