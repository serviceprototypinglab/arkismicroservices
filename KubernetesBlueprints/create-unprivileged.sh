#!/usr/bin/env bash

which kubectl >/dev/null
if [ $? -eq 1 ]; then
	echo "Error: You need to install and configure kubectl: https://kubernetes.io/docs/user-guide/kubectl-overview/" >&2
	exit 1
fi

for descriptor in `find -name *-deployment.json` `find -name *-service.json`
do
	echo "- $descriptor"
	grep -v namespace $descriptor | kubectl create -f -
done
