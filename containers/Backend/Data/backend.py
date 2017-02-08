import bottle
import pymongo
from bottle import response, request
from bson import ObjectId
import os
import random
import json
from loremipsum import generate_paragraphs


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


def get_connection():

    host = get_database_host()
    port = get_database_port()
    # host = 'localhost'
    try:
        conn = pymongo.MongoClient(host=host, port=int(port))
    except Exception, e:
        conn = None
        print e
    return conn


def get_connection1(host, port):
    try:
        conn = pymongo.MongoClient(host=host, port=int(port))
    except Exception, e:
        conn = None
        print e
    return conn


def get_database(conn):
    return conn.arkis


def get_database1(conn, option, user):
    if option == 'D':
        return conn['arkis'+str(user)]
    else:
        return conn.arkis


def get_collection(db, coll):
    return db[str(coll)]


def get_collection1(db, coll, option, user):
    if option == 'B':
        return db[str(coll)+str(user)]
    else:
        return db[str(coll)]


@app.route('/')
def start():
    try:
        host = get_database_host()
        port = get_database_port()
        a1 = {"port": port}
        a2 = {"host": host}
        res = [a1, a2]
    except Exception, e:
        print e
        return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode(res)


def get_blob():
    res = ''
    for p in generate_paragraphs(10, False):
        res += p[2]
    return res


def create_aux_json(prefix_name, multi_tenant_option, count, user):
    blob = get_blob()
    name = blob[:5]
    path = '/data/blobs/' + prefix_name + '_' + multi_tenant_option + '_' + str(count) + '_' + name + '.txt'
    number_aux = random.randint(1, 100)
    aux_json = {'title': name,
                'tenant': user,
                'user': user,
                'name': name,
                'tenant_option': multi_tenant_option,
                'other_id': count,
                'path': path,
                'blob': blob,
                'number': number_aux}
    return aux_json


def get_max_row_id(coll):
    try:
        a = int(coll.find_one(sort=[("other_id", -1)])['other_id'])
        return a
    except Exception, e:
        print e
        return -2


@app.get('/data/<user>/<option>/<limit>')
def add_data(user, option, limit):
    try:
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
        conn = get_connection1(host, port)
        db = get_database1(conn, option, user)
        coll = get_collection1(db, 'documents', option, user)
        try:
            count = get_max_row_id(coll)
            if count == -2:
                count = 0
        except Exception, e:
            print e
            count = 0
        for i in range(0, int(limit)):
            json_data = create_aux_json('arkis', option, count + i, int(user))
            coll.insert_one(json_data)
        coll.create_index([('blob', pymongo.TEXT)])
        conn.close()
    except Exception, e:
        return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode([{"error": "No error"}])

app.run(host='0.0.0.0', port=55555, debug=True)
