import bottle
import pymongo
from bottle import response, request
import json
from bson import ObjectId
import os


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
    if host:
        pass
    else:
        host = 'arkismongopersistentusers'
    return host


def get_database_port():
    try:
        port = int(os.environ.get('DATABASE_PORT'))
    except Exception, e:
        print e
        port = None
    if port:
        pass
    else:
        port = 30009
    return port


def get_connection():
    host = get_database_host()
    port = get_database_port()
    # host = '104.198.249.229'
    # host = 'localhost'
    try:
        conn = pymongo.MongoClient(host=host, port=int(port))
    except Exception, e:
        conn = None
        print e
    return conn


def get_database(conn):
    return conn.arkis


def get_collection(db, coll):
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


@app.get('/len')
def get_users():
    try:
        conn = get_connection()
        db = get_database(conn)
        r = get_collection(db, 'users').find({}).count()
        conn.close()
        res = {"len": r}
    except Exception, e:
        return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode(res)


@app.get('/validate/<user>/<password>')
def validate(user, password):
    print "validate"
    try:
        user = int(user)
        aux_id = True
    except Exception, e1:
        aux_id = False
    if aux_id:
        try:
            password = int(password)
            conn = get_connection()
            db = get_database(conn)
            collection = get_collection(db, 'users')
            r = collection.find({"user": user, "pass": password}).count()
            if r > 0:
                aux_user = collection.find_one({"user": int(user), "pass": password})
                return JSONEncoder1().encode([{"res": "yes",
                                               "user": aux_user['user'],
                                               "username": aux_user['username'],
                                               "option": aux_user['option'],
                                               "role": aux_user['role']}])
        except Exception, e:
            return JSONEncoder1().encode([{"res": "error", "error": str(e)}])
    else:
        try:
            password = int(password)
            conn = get_connection()
            db = get_database(conn)
            collection = get_collection(db, 'users')
            r = collection.find({"username": user, "pass": password}).count()
            if r > 0:
                aux_user = collection.find_one({"username": user, "pass": password})
                return JSONEncoder1().encode([{"res": "yes",
                                               "user": aux_user['user'],
                                               "username": aux_user['username'],
                                               "option": aux_user['option'],
                                               "role": aux_user['role']}])
        except Exception, e:
            return JSONEncoder1().encode([{"res": "error", "error": str(e)}])
    return JSONEncoder1().encode([{"res": "no"}])


@app.route('/connection')
def connection():
    try:
        conn = get_connection()
    except Exception, e:
        collection_names = ["error connection", e]
        return JSONEncoder1().encode({"collections": collection_names})
    try:
        db = get_database(conn)
        conn.close()
    except Exception, e:
        collection_names = ["error database", e]
        return JSONEncoder1().encode({"collections": collection_names})
    collection_names = db.collection_names()
    return JSONEncoder1().encode({"collections": collection_names})


@app.get('/users')
def get_users():
    try:
        conn = get_connection()
        db = get_database(conn)
        collection = get_collection(db, 'users')
        r = collection.find({})
        res = []
        conn.close()
        for a in r:
            res.append(a)
    except Exception, e:
        return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode(res)


@app.get('/users/<user>')
def get_user(user):
    try:
        conn = get_connection()
        db = get_database(conn)
        collection = get_collection(db, 'users')
        r = collection.find_one({"user": int(user)})
        conn.close()
    except Exception, e:
        return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode(r)


@app.get('/users/<user>/option')
def get_user(user):
    try:
        conn = get_connection()
        db = get_database(conn)
        collection = get_collection(db, 'users')
        r = collection.find_one({"user": int(user)})['option']
        conn.close()
    except Exception, e:
        return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode({"option": r})


@app.get('/lastid')
def get_max_row_id1():
    try:
        conn = get_connection()
        db = get_database(conn)
        a1 = get_collection(db, 'users').find_one(sort=[("user", -1)])['user']
        print "get from db"
        print a1
        a = int(a1)
        print "convert to int"
        print a
        conn.close()
        return {"id": a}
    except Exception, e:
        print "error get_max"
        print e
        return {"id": -1}


def get_max_row_id():
    try:
        conn = get_connection()
        db = get_database(conn)
        a1 = get_collection(db, 'users').find_one(sort=[("user", -1)])['user']
        a = int(a1)
        conn.close()
        return a
    except Exception, e:
        print "error get_max"
        print e
        return -1


@app.post('/users')
def post():
    try:
        option = request.forms.get('option')
        aux_pass = int(request.forms.get('pass'))
        path = request.forms.get('path')
        username = request.forms.get('username')
        max_index = get_max_row_id()
        if max_index != -1:
            other_id = max_index + 1
            role = 'user'
        else:
            other_id = 1
            role = 'admin'
        user = other_id
        tenant = other_id
        if option == 'E':
            host = 'arkismongopersistent' + str(user)
            port = 30010 + user
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
            port = 30010 + user
        aux_user = {'other_id': other_id,
                    'user': user,
                    'tenant': tenant,
                    'option': option,
                    'username': username,
                    'path': path,
                    'host': host,
                    'port': port,
                    'pass': aux_pass,
                    'role': role}
        conn = get_connection()
        db = get_database(conn)
        get_collection(db, 'users').insert_one(aux_user)
        conn.close()
    except Exception, e:
        return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode([aux_user])


@app.put('/users/<user>')
def put(user):
    r = None
    try:
        try:
            user = int(user)
            conn = get_connection()
            db = get_database(conn)
            r = get_collection(db, 'users').find_one({"user": int(user)})
        except Exception, e:
            return JSONEncoder1().encode([{"error": str(e)}])
        option = request.forms.get('option')
        aux_pass = request.forms.get('pass')
        port = request.forms.get('port')
        host = request.forms.get('host')
        path = request.forms.get('path')
        if option:
            r['option'] = option
        if aux_pass:
            r['pass'] = aux_pass
        if port:
            r['port'] = port
        if host:
            r['host'] = host
        if path:
            r['path'] = path
        get_collection(db, 'users').update({"user": int(user)}, r)
        conn.close()
    except Exception, e:
        if r:
            return JSONEncoder1().encode([{"error": str(e)}, r])
        else:
            return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode(r)


@app.post('/put/users/<user>')
def put1(user):
    r = None
    try:
        try:
            user = int(user)
            conn = get_connection()
            db = get_database(conn)
            r = get_collection(db, 'users').find_one({"user": int(user)})
        except Exception, e:
            return JSONEncoder1().encode([{"error": str(e)}])
        option = request.forms.get('option')
        aux_pass = request.forms.get('pass')
        port = request.forms.get('port')
        host = request.forms.get('host')
        path = request.forms.get('path')
        if option:
            r['option'] = option
        if aux_pass:
            r['pass'] = aux_pass
        if port:
            r['port'] = port
        if host:
            r['host'] = host
        if path:
            r['path'] = path
        get_collection(db, 'users').update({"user": int(user)}, r)
        conn.close()
    except Exception, e:
        if r:
            return JSONEncoder1().encode([{"error": str(e)}, r])
        else:
            return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode(r)


@app.delete('/users/<user>')
def delete(user):
    try:
        user = int(user)
        conn = get_connection()
        db = get_database(conn)
        get_collection(db, 'users').delete_one({"user": int(user)})
        conn.close()
    except Exception, e:
        print e
        return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode([{"res": "Deleted"}])


@app.get('/delete/users/<user>')
def delete1(user):
    try:
        user = int(user)
        conn = get_connection()
        db = get_database(conn)
        get_collection(db, 'users').delete_one({"user": int(user)})
        conn.close()
    except Exception, e:
        print e
        return JSONEncoder1().encode([{"res": str(e)}])
    return JSONEncoder1().encode([{"res": "Deleted"}])

app.run(host='0.0.0.0', port=50000, debug=True)
