#!/usr/bin/env bash
# Create databases MS
kubectl delete -f ./DatabaseMicroServices/nopersistance/OPTIONA/
kubectl delete -f ./DatabaseMicroServices/nopersistance/USERS/
# Create backend MS
kubectl delete -f ./BackendMicroServices/dataMS/
kubectl delete -f ./BackendMicroServices/documentsMS/
kubectl delete -f ./BackendMicroServices/migrateMS/
kubectl delete -f ./BackendMicroServices/searchMS/
kubectl delete -f ./BackendMicroServices/usersMS/
# Create frontend MS
kubectl delete -f ./FrontendMicroServices/adminFrontendMS/
kubectl delete -f ./FrontendMicroServices/userFrontendMS/
kubectl delete -f ./FrontendMicroServices/loginFrontendMS/
# Create ARKIS namespace
kubectl delete -f namespace.yaml