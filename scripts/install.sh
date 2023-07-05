pushd manifests
while ! kustomize build example | awk '!/well-defined/' | kubectl apply -f -; do
    echo "Retrying to apply resources"
    sleep 10
done
