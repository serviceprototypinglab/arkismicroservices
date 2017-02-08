# Cloud native ARKIS Prototype

It is a [cloud native document management system](https://blog.zhaw.ch/icclab/cloud-native-document-management/)
created using a microservice architecture.  

## Microservice architecture

  Each microservice is created using a docker image container.
  You can see the code inside the folder container. 
  All the images are in the public docker hub repository: [chumbo](https://hub.docker.com/u/chumbo/)
  
### Frontend microservices

#### Login

port_login: 32000
UI for the login web page.
You can try to login and create a new user.
    
#### Users

port_users: 32000
UI for the users web page.
You can manage all the documents of these user.(create, delete, search, ...)
    
#### Admin

port_login: 32000
Admin UI web page.
You can see users, delete users, add new generic documents, migrate between the different multi-tenant options.


### Backend microservices

#### Documents

port_documents: 30000
CRUD of documents

#### Search

port_search: 30004
Full text search in the documents of one user.

#### Migrate

port_migrate: 30003
Move the documents of one user to a different multi-tenant option.

#### Data

port_data: 30002
For add generic documents to one user.

#### Users

port_users: 30001
CRUD users.

### Database microservices

Persistent deployment for documents and users.
The container image is the official mongo image.
The database for users is running in the port 30009.
 
#### Documents

   Different multitenant option. All these options are working in these version.
 
   - A: Shared DBMS, Shared database, shared schema, shared table/collection
    - port: 30005
   - B: Shared DBMS, Shared database, shared schema, one table/collection per tenant
    - port: 30006
   - C: Shared DBMS, Shared database, one schema per tenant. (Not make sense with mongo) 
    - port: 30007
   - D: Shared DBMS, one database per tenant
    - port: 30008
   - E: One DBMS per tenant
    - port: 30010 + tenant_id
    
## API REST

Useful endpoints for the API REST:

### Users

  - GET: host:port_user/users/(id)
  - GET: host:port_user/users/
  - POST: host:port_user/users
  - PUT: host:port_user/users 
  - DELETE: host:port_user/users/(id)
  - GET: host:port_user/validate/(user)/(password)

### Documents

  - GET: host:port_documents/documents/(user)/(option)/last
  - GET: host:port_documents/documents/(user)/(option)/lim/(lim)
  - GET: host:port_documents/documents/(user)/(option)/(other_id)
  - POST: host:port_documents/documents/(user)/(option)
  - PUT: host:port_documents/documents/(user)/(option)/(other_id)
  - DELETE: host:port_documents/documents/(user)/(option)/(other_id)

  
### Search

  - GET: host:port_search/documents/search/(user)/(option)/(pattern)
    
### Data

  - GET: host:port_data/data/(user)/(option)/(limit)
  
### Migrate

  - GET: host:port_migrate/migrate/(user)/(option)
  
## Tutorial

### Create

0. Clone this repository.
1. Create a [kubernetes cluster in google cloud](https://cloud.google.com/container-engine/).
2. Create the next [persistent disks](https://cloud.google.com/compute/docs/disks/add-persistent-disk#create_disk ) in the same zone that you have your cluster:
 - a: mongodb-disk-a
 - b: mongodb-disk-b
 - c: mongodb-disk-c
 - d: mongodb-disk-d
 - e: mongodb-disk-(number of tenant) where number of tenant belong to {0,1, ... ,9}
 - users: disk-mongo-shared-users
3. Install [kubectl](https://kubernetes.io/docs/user-guide/kubectl-overview/) 
4. Run the script: create.sh 

Until here, you have running ARKIS 3.0.
Now, you can add users and documents using the Admin UI or the API REST.
Also, you have available the User UI to start to use the prototype. 

5. If you want create more tenants with the multitenant option E:
    - Create the persistent: disk mongodb-disk-(number of tenant)
    - Create the microservice:
        - cd KubernetesBlueprints/DatabaseMicroServices/googlecloudpersistance/OPTIONE
        - change the nodePort to 30010 + number of tenant
        - run: kubectl create -f .

Note: If you delete all the persistent disk in the persistent deployments (database microservice),
you have a prototype independently to the google cloud provider and you can run it in any 
kubernetes cluster but, of course, without persistent data.  

### Delete

1. 
    - If you want keep your cluster: Run the script: delete.sh
    - If you don't want keep your cluster: Just delete your cluster 
2. Delete all the persistent disk.

## Next steps

1. Create automatically the microservice for multi-tenant option E.
2. Create blueprints for docker-swarm.
3. Create a microservice using .netCore
