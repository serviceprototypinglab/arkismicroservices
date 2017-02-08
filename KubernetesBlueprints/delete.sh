#!/usr/bin/env bash
kubectl delete deployment,rs,pod,svc --all --namespace=arkis
kubectl delete namespace arkis