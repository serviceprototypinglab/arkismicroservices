#!/usr/bin/env bash

which kubectl >/dev/null
if [ $? -eq 1 ]; then
	echo "Error: You need to install and configure kubectl: https://kubernetes.io/docs/user-guide/kubectl-overview/" >&2
	exit 1
fi

kubectl delete deployment,rs,pod,svc --all --namespace=arkis
kubectl delete namespace arkis
