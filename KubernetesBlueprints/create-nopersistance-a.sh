#!/usr/bin/env bash

which kubectl >/dev/null
if [ $? -eq 1 ]; then
	echo "Error: You need to install and configure kubectl: https://kubernetes.io/docs/user-guide/kubectl-overview/" >&2
	exit 1
fi

# Create ARKIS namespace
kubectl create -f namespace.yaml
# Create databases MS
kubectl create -f ./DatabaseMicroServices/nopersistance/OPTIONA/
kubectl create -f ./DatabaseMicroServices/nopersistance/USERS/
# Create backend MS
kubectl create -f ./BackendMicroServices/dataMS/
kubectl create -f ./BackendMicroServices/documentsMS/
kubectl create -f ./BackendMicroServices/migrateMS/
kubectl create -f ./BackendMicroServices/searchMS/
kubectl create -f ./BackendMicroServices/usersMS/
# Create frontend MS
kubectl create -f ./FrontendMicroServices/adminFrontendMS/
kubectl create -f ./FrontendMicroServices/userFrontendMS/
kubectl create -f ./FrontendMicroServices/loginFrontendMS/
