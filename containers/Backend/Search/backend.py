import bottle
import pymongo
from bottle import response, request
import json
from bson import ObjectId
import os
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

print "START"
coll_name = 'documents'


def get_database_host():
    try:
        host = os.environ.get('DATABASE_HOST')
    except Exception, e:
        print e
        host = None
        print "ERROR"
    if host:
        pass
    else:
        host = 'arkismongopersistent'
    return host


def get_database_port():
    try:
        port = int(os.environ.get('DATABASE_PORT'))
    except Exception, e:
        print e
        port = None
        print "ERROR"
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
        host = 'arkismongopersistentc'
        port = 30007
    elif option == 'D':
        host = 'arkismongopersistentd'
        port = 30008
    else:
        host = 'arkismongopersistent' + str(user)
        port = 30010 + int(user)
    # host = 'localhost'
    try:
        conn = pymongo.MongoClient(host=host, port=int(port))
    except Exception, e:
        return JSONEncoder1().encode([{"error": str(e)}])
    return conn


def get_database(conn, option, user):
    if user:
        user = str(user)
    if option == 'A':
        return conn['arkis']
    elif option == 'B':
        return conn['arkis']
    elif option == 'C':
        return conn['arkis']
    elif option == 'E':
        return conn['arkis']
    elif option == 'D':
        return conn['arkis' + str(user)]
    else:
        return conn['arkis']


def get_collection(option, db, user, coll):
    if option == 'B':
        return db[str(coll) + str(user)]
    else:
        return db[str(coll)]


@app.route('/')
def start():
    host = get_database_host()
    port = get_database_port()
    a1 = {"port": port}
    a2 = {"host": host}
    res = [a1, a2]
    return JSONEncoder1().encode(res)


@app.route('/connection/<user>/<option>')
def connection(user, option):
    user = int(user)
    try:
        conn = get_connection(user, option)
    except Exception, e:
        collection_names = ["error connection", e]
        return JSONEncoder1().encode({"collections": collection_names})
    try:
        db = get_database(conn, option, user)
    except Exception, e:
        collection_names = ["error database", e]
        return JSONEncoder1().encode({"collections": collection_names})
    collection_names = db.collection_names()
    conn.close()
    return JSONEncoder1().encode({"collections": collection_names})


@app.get('/documents/search/<user>/<option>/<pattern>')
def search(user, option, pattern):
    user = int(user)
    try:
        conn = get_connection(user, option)
        db = get_database(conn, option, user)
        name = pattern
        example = get_collection(option, db, user, 'documents').find_one(
            {"user": user, "$text": {"$search": name, "$caseSensitive": True}})
        conn.close()
        # TODO CYCLOPS ENDPOINT
        if False:
            try:
                cyclops_endpoint = os.environ.get('CYCLOPS_ENDPOINT')
                if cyclops_endpoint:
                    pass
                else:
                    cyclops_endpoint = '35.160.33.120:4567'
                try:
                    cyclops_time = time.time()
                except Exception, e:
                    print e
                data = {"_class": "ArkisSearchUsage",
                        "account": "ArkisUser",
                        "usage": 1,
                        "unit": "query"}
                # url = 'http://160.85.4.150:4567/data'
                url = 'http://' + cyclops_endpoint + '/data'
                # url = 'http://35.160.33.120:4567/data'
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                rcyclops = requests.post(url, data=json.dumps(data), headers=headers)
                print rcyclops.status_code
                print rcyclops.content
            except Exception, e:
                print "Error with petition post to cyclops"
                print e
        return JSONEncoder1().encode(example)
    except Exception, e:
        return JSONEncoder1().encode([{"error": str(e)}])

app.run(host='0.0.0.0', port=55555, debug=True)
