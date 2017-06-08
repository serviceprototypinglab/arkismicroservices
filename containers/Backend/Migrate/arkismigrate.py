import subprocess
import bottle
from bottle import response, request
import json
from bson import ObjectId
import os
import pymongo
import time
import requests


class JSONEncoder1(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class EnableCors(object):
    name = 'enable_cors'
    api = 2

    @staticmethod
    def apply(fn, context):
        def _enable_cors(*args, **kwargs):
            # print context
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS, DELETE'
            response.headers[
                'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
            response.headers['Content-type'] = 'application/json'
            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


app = bottle.app()
app.install(EnableCors())

print("START")


def get_database_host():
    try:
        host = os.environ.get('DATABASE_HOST')
    except Exception:
        host = None
    if host:
        pass
    else:
        host = 'arkismongopersistent'
    return host


def get_database_port():
    try:
        port = int(os.environ.get('DATABASE_PORT'))
    except Exception:
        port = None
    if port:
        pass
    else:
        port = 30010
    return port


def get_connection(user, option):
    if user:
        user = int(user)
    else:
        user = 0
    if option == 'E':
        host = 'arkismongopersistent' + str(user)
        port = 30010 + int(user)
    elif option == 'B':
        host = 'arkismongopersistentb'
        port = 30006
    elif option == 'A':
        host = 'arkismongopersistenta'
        port = 30005
    elif option == 'C':
        host = 'arkismongopersistentd'
        port = 30007
    elif option == 'D':
        host = 'arkismongopersistentd'
        port = 30008
    else:
        host = 'arkismongopersistent' + str(user)
        port = 30010 + int(user)
    # host = 'localhost'
    try:
        # host = '104.198.249.229'
        conn = pymongo.MongoClient(host=host, port=int(port))
    except Exception, e:
        return JSONEncoder1().encode([{"error": str(e)}])
    return conn


def get_database(conn, user, option):
    if user:
        user = str(user)
    if option == 'E':
        return conn['arkis']
    elif option == 'B':
        return conn['arkis']
    elif option == 'A':
        return conn['arkis']
    elif option == 'C':
        return conn['arkis']
    elif option == 'D':
        return conn['arkis' + user]
    else:
        return conn['arkis']


def get_collection(db, user, option, coll):
    if option == 'B':
        return db[str(coll) + str(user)]
    else:
        return db[str(coll)]


def deployment(num, op):
    num = int(num)
    with open('arkismongo-deployment.json') as data_file:
        data = json.load(data_file)

    data['spec']['template']['metadata']['labels']['service'] = 'arkismongopersistent' + str(num)
    data['metadata']['name'] = 'arkismongopersistent' + str(num)

    with open('arkismongo-deployment.json', 'w') as outfile:
        json.dump(data, outfile)

    with open('arkismongo-service.json') as data_file:
        data = json.load(data_file)

    data['metadata']['labels']['service'] = 'arkismongopersistent' + str(num)
    data['metadata']['name'] = 'arkismongopersistent' + str(num)
    data['spec']['ports'][0]['name'] = 'arkismongopersistent' + str(num)
    data['spec']['ports'][0]['port'] = 27017
    data['spec']['ports'][0]['nodePort'] = 30010 + num
    data['spec']['selector']['service'] = 'arkismongopersistent' + str(num)
    with open('arkismongo-service.json', 'w') as outfile:
        json.dump(data, outfile)

    subprocess.run(["kubectl", op, "-f", "arkismongo-deployment.json", "--kubeconfig=/usr/src/app/config"])
    subprocess.run(["kubectl", op, "-f", "arkismongo-service.json", "--kubeconfig=/usr/src/app/config"])
    if op == 'delete':
        pass
        # TODO DELETE REPLICA SET AND POD


def get_option(user):
    host = 'arkismongopersistentusers'
    # host = '104.198.249.229'
    conn = pymongo.MongoClient(host=host, port=int(30009))
    coll = conn.arkis['users']
    option = coll.find_one({'user': int(user)})['option']
    return option


def get_min_index(coll, option, user):
    if option == 'A':
        try:
            a1 = coll.find_one({"user": int(user)}, sort=[("other_id", 1)])
            a2 = a1['other_id']
            a = int(a2)
            return a
        except Exception, e:
            print "Error min"
            print e
            return -2
    else:
        try:
            a = int(coll.find_one(sort=[("other_id", 1)])['other_id'])
            return a
        except Exception, e:
            print "Error min"
            print e
            return -2


def get_max_index(coll, option, user):
    if option == 'A':
        try:
            a = int(coll.find_one({"user": int(user)}, sort=[("other_id", -1)])['other_id'])
            return a
        except Exception, e:
            print e
            return -2
    else:
        try:
            a = int(coll.find_one(sort=[("other_id", -1)])['other_id'])
            return a
        except Exception, e:
            print e
            return -2


def get_json(coll, i, option, user):
    if option == 'A':
        r = coll.find_one({"other_id": int(i), "user": int(user)})
    else:
        r = coll.find_one({"other_id": int(i)})
    return r


def check_json(coll, option, other_id, user):
    if option == 'A':
        try:
            r = coll.count({"other_id": int(other_id), "user": int(user)})
        except Exception, e:
            print e
            return False
    else:
        try:
            r = coll.count({"other_id": int(other_id)})
        except Exception, e:
            print e
            return False
    print r
    if r > 0:
        return True
    else:
        return False


def insert_json(coll, i):
    try:
        coll.insert_one(i)
    except Exception, e:
        print e
        return False
    return True


def delete_documents(coll, user):
    try:
        coll.delete_many({"user": int(user)})
    except Exception, e:
        print e
        return False
    return True


def change_user(new_option, user):
    try:
        host = 'arkismongopersistentusers'
        # host = '104.198.249.229'
        conn = pymongo.MongoClient(host=host, port=int(30009))
        coll = conn.arkis['users']
        # r = coll.find_one({"user": int(user)})
        # r['option'] = new_option
        if new_option == 'E':
            host = 'arkismongopersistent' + str(user)
            port = 30010 + int(user)
        elif new_option == 'B':
            host = 'arkismongopersistentb'
            port = 30006
        elif new_option == 'A':
            host = 'arkismongopersistenta'
            port = 30005
        elif new_option == 'C':
            host = 'arkismongopersistentd'
            port = 30007
        elif new_option == 'D':
            host = 'arkismongopersistentd'
            port = 30008
        else:
            host = 'arkismongopersistent' + str(user)
            port = 30010 + int(user)
        coll.update_one({"user": int(user)}, {'$set': {'option': new_option, 'port': port, 'host': host}}, upsert=False)
        return True
    except Exception, e:
        print e
        return False


@app.get('/deploy/<user>')
def aux(user):
    deployment(user, 'create')


@app.get('/migrate/<user>/<option>')
def migrate(user, option):
    current_option = get_option(user)
    new_option = option
    print current_option
    print new_option
    current_conn = get_connection(user, current_option)
    current_db = get_database(current_conn, user, current_option)
    current_coll = get_collection(current_db, user, current_option, 'documents')
    if new_option != 'E':
        new_conn = get_connection(user, new_option)
        new_db = get_database(new_conn, user, new_option)
        new_coll = get_collection(new_db, user, new_option, 'documents')
    else:
        # TODO Create deployment from MS
        # deployment(user, "create")
        success_created = True
        if success_created:
            new_conn = get_connection(user, new_option)
            new_db = get_database(new_conn, user, new_option)
            new_coll = get_collection(new_db, user, new_option, 'documents')
        else:
            return {"error": "no created deployment"}
    min_index = get_min_index(current_coll, current_option, user)
    if min_index == -2:
        min_index = 0
    max_index = get_max_index(current_coll, current_option, user)
    print min_index
    print max_index
    for i in range(min_index, max_index + 1):
        aux_json = get_json(current_coll, i, current_option, user)
        if aux_json:
            print i
            aux1 = {'number': aux_json['number'],
                    'other_id': aux_json['other_id'],
                    'user': aux_json['user'],
                    'title': aux_json['title'],
                    'blob': aux_json['blob'],
                    'name': aux_json['name'],
                    'tenant': aux_json['tenant'],
                    'tenant_option': new_option}
            inserts_bool = insert_json(new_coll, aux1)
            if inserts_bool:
                inserts_bool = check_json(new_coll, new_option, i, user)
                print inserts_bool
            else:
                inserts_bool = False
            if inserts_bool:
                pass
            else:
                return {"error inserting for row": i}
    try:
        new_coll.create_index([('blob', pymongo.TEXT)])
    except Exception, e:
        print e
        return {"error creating full text for the user": int(user)}
    change_user_bool = change_user(new_option, user)
    if change_user_bool:
        pass
    else:
        return {"error changing option tenant for user": int(user)}
    if option == 'E':
        # TODO DELETE DEPLOYMENT AND SVC
        # deployment(user, 'delete')
        deletes_bools = delete_documents(current_coll, user)
    else:
        deletes_bools = delete_documents(current_coll, user)
    if deletes_bools:
        return {"success": "migrated"}
    else:
        return {"error": "deleting data"}


app.run(host='0.0.0.0', port=50002, debug=True)
