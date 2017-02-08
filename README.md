# Containerized  architecture 

It is a containerized  architecture using docker.
We can run with docker-compose easily using the build.sh in our machine.
Also, we deploy it in Kubernetes, Vamp and Azure.
Currently from the frontend we must configure the connexion with the REST API (backend).
It is because we want deploy it with different orchestrations tools and in different cloud provider.
Soon, this connexion will be automatically in the most of the case.

## Kubernetes

 (ARKIS FRONTEND chumbo/arkisfrontend:2.0.3)
 http://52.34.213.48:31471 
 
 (ARKIS  chumbo/arkisbackend:2.0.2) 
 host = 52.34.213.48
 port= 32767 
 
## Azure

 (ARKIS 1.8.1 frontend)
 
 http://swarmmgmt.japaneast.cloudapp.azure.com:44444/ 
 
 (ARKIS 1.8.1 BACKEND)
 HOST = swarmmgmt.japaneast.cloudapp.azure.com
 PORT = 55555
 
 (ARKIS 2.0 mono container)
 http://swarmmgmt.japaneast.cloudapp.azure.com:9000/ 

## Vamp (with Rancher)

(ARKIS 1.8.1 frontend)
http://35.160.127.206:44444/

 (ARKIS 1.8.1 BACKEND)
host=35.160.127.206
port=55555

(ARKIS database)
host=35.160.127.206
port= 27017