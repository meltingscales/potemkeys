## Running

Note: you need minikube

TODO: automate vagrant stuff

    kubectl apply -f pod.yaml

    kubectl get pod shell-demo

    kubectl exec --stdin --tty shell-demo -- /bin/bash