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
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
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


@bottle.route('/documents/<user>/<option>', method='OPTIONS')
def post1(user, option):
    pass


@bottle.route('/documents/<user>/<option>/<other_id>', method='OPTIONS')
def post2(user, option, other_id):
    pass

@bottle.route('/documents/<user>/<option>/last', method='OPTIONS')
def post3(user, option):
    pass

@bottle.route('/documents/<user>/<option>/lim/<lim>', method='OPTIONS')
def post4(user, option, lim):
    pass

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


@app.get('/documents/<user>/<option>/lim/<lim>')
def get_all(user, option, lim):
    user = int(user)
    try:
        conn = get_connection(user, option)
        db = get_database(conn, option, user)
        if lim == 'nolimit':
            # Change the limit
            r = get_collection(option, db, user, 'documents').find({"user": user}).limit(10000)
        else:
            r = get_collection(option, db, user, 'documents').find({"user": user}).limit(int(lim))
        res1 = []
        if r:
            for a in r:
                res1.append(a)
        res = JSONEncoder1().encode(res1)
        response.status = 200
        conn.close()
    except Exception, e:
        print e
        error_str = "ERROR LOOKING DOCUMENTS FOR USER " + str(user) \
                    + " WITH MT OPTION " + str(option) \
                    + " ERROR " + str(e)
        a = {"error": error_str}
        res = JSONEncoder1().encode(a)
        response.status = 500

    response.content_type = 'application/json'
    response.body = res
    return response


@app.get('/documents/<user>/<option>/last')
def get_last(user, option):
    user = int(user)
    try:
        conn = get_connection(user, option)
        db = get_database(conn, option, user)
        r = get_collection(option, db, user, 'documents').find_one(sort=[("other_id", -1)])
        conn.close()
        response.status = 200
    except Exception, e:
        print e
        error_str = "ERROR LOOKING DOCUMENTS FOR USER " + str(user) + " WITH MT OPTION " + str(option)
        r = {"error": error_str}
        response.status = 500
    res = JSONEncoder1().encode(r)
    response.content_type = 'application/json'
    response.body = res
    return response


@app.get('/documents/<user>/<option>/<other_id>')
def get_by_id(user, option, other_id):
    try:
        conn = get_connection(user, option)
        db = get_database(conn, option, user)
        user = int(user)
        r = get_collection(option, db, user, 'documents').find_one({"other_id": int(other_id), "user": user})
        conn.close()
    except Exception, e:
        print e
        return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode(r)


def get_max_row_id(user, option):
    try:
        conn = get_connection(user, option)
        db = get_database(conn, option, user)
        a = int(get_collection(option, db, user, 'documents').find_one(sort=[("other_id", -1)])['other_id'])
        conn.close()
        return a
    except Exception, e:
        print e
        return -2


@app.post('/documents/<user>/<option>')
def post(user, option):
    try:
        data = request.json
        user = int(user)
        blob = data.get('blob')
        number = int(data.get('number'))
        name = data.get('name')
        title = data.get('title')
        path = '/data/blobs/arkis_' + option + '_' + str(user) + '_' + name + '.txt'
        max_index = get_max_row_id(user, option)
        #max_index = 2
        if max_index == -1:
            return JSONEncoder1().encode([{"error": "no index"}])
        else:
            other_id = max_index + 1
        # print rowident
        aux_blob = {'blob': blob,
                    'number': number,
                    'name': name,
                    'title': title,
                    'other_id': other_id,
                    'user': user,
                    'tenant': user,
                    'tenant_option': option,
                    'path': path}

        conn = get_connection(user, option)
        db = get_database(conn, option, user)
        get_collection(option, db, user, 'documents').insert_one(aux_blob)
        conn.close()
    except Exception, e:
        return JSONEncoder1().encode([{"error": str(e)}])
    res = JSONEncoder1().encode(aux_blob)
    response.content_type = 'application/json'
    response.status = 200
    response.body = res
    return response


@app.put('/documents/<user>/<option>/<other_id>')
def put(user, option, other_id):
    r = None
    try:
        data = request.json
        try:
            user = int(user)
            conn = get_connection(user, option)
            db = get_database(conn, option, user)
            r = get_collection(option, db, user, 'documents').find_one({"other_id": int(other_id), "user": user})
        except Exception, e:
            return JSONEncoder1().encode([{"error": str(e)}])
        aux_blob = data.get('blob')
        aux_number = data.get('number')
        aux_name = data.get('name')
        aux_title = data.get('title')
        aux_path = None
        if aux_title:
            r['title'] = aux_title
        if aux_name:
            aux_path = '/data/blobs/arkis_' + option + '_' + str(user) + '_' + aux_name + '.txt'
            r['name'] = aux_name
        if aux_path:
            r['path'] = aux_path
        if aux_number:
            aux_number = int(aux_number)
            r['number'] = aux_number
        if aux_blob:
            r['blob'] = aux_blob
        get_collection(option, db, user, 'documents').update({"other_id": int(other_id)}, r)
        conn.close()
        res = JSONEncoder1().encode(r)
        response.status = 200
    except Exception, e:
        response.status = 500
        if r:
            res = JSONEncoder1().encode([{"error": str(e)}, r])
        else:
            res = JSONEncoder1().encode([{"error": str(e)}])
    response.content_type = 'application/json'
    response.body = res
    return response


@app.post('/put/documents/<user>/<option>/<other_id>')
def put1(user, option, other_id):
    r = None
    try:
        try:
            user = int(user)
            conn = get_connection(user, option)
            db = get_database(conn, option, user)
            r = get_collection(option, db, user, 'documents').find_one({"other_id": int(other_id), "user": user})
        except Exception, e:
            return JSONEncoder1().encode([{"error": str(e)}])
        aux_blob = request.forms.get('blob')
        aux_number = request.forms.get('number')
        aux_name = request.forms.get('name')
        aux_title = request.forms.get('title')
        aux_path = None
        if aux_title:
            r['title'] = aux_title
        if aux_name:
            aux_path = '/data/blobs/arkis_' + option + '_' + str(user) + '_' + aux_name + '.txt'
            r['name'] = aux_name
        if aux_path:
            r['path'] = aux_path
        if aux_number:
            aux_number = int(aux_number)
            r['number'] = aux_number
        if aux_blob:
            r['blob'] = aux_blob
        get_collection(option, db, user, 'documents').update({"other_id": int(other_id)}, r)
        conn.close()
    except Exception, e:
        if r:
            return JSONEncoder1().encode([{"error": str(e)}, r])
        else:
            return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode(r)


@app.delete('/documents/<user>/<option>/<other_id>')
def delete(user, option, other_id):
    try:
        user = int(user)
        conn = get_connection(user, option)
        db = get_database(conn, option, user)
        get_collection(option, db, user, 'documents').delete_one({"other_id": int(other_id), "user": user})
        conn.close()
        res = JSONEncoder1().encode({"id": other_id})
        response.status = 200
    except Exception, e:
        print e
        response.status = 500
        res = JSONEncoder1().encode({"error": str(e)})

    response.content_type = 'application/json'

    response.body = res
    return response


@app.get('/delete/documents/<user>/<option>/<other_id>')
def delete1(user, option, other_id):
    try:
        user = int(user)
        conn = get_connection(user, option)
        db = get_database(conn, option, user)
        get_collection(option, db, user, 'documents').delete_one({"other_id": int(other_id), "user": user})
        conn.close()
    except Exception, e:
        print e
        return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode([{"res": "Deleted"}])


@app.get('/blobs/host/<host1>')
def change_host(host1):
    try:
        os.environ["DATABASE_HOST"] = host1
    except Exception, e:
        print e
        return JSONEncoder1().encode([{"error": str(e)}])
    res = os.environ["DATABASE_HOST"]
    return JSONEncoder1().encode([{"host": res}])


@app.get('/blobs/port/<port1>')
def change_port(port1):
    try:
        os.environ["DATABASE_PORT"] = port1
    except Exception, e:
        print e
        return JSONEncoder1().encode([{"error": str(e)}])
    res = os.environ["DATABASE_PORT"]
    return JSONEncoder1().encode([{"port": res}])


@app.get('/blobs/rcb/<rcb1>')
def change_rcb(rcb1):
    try:
        os.environ["CYCLOPS_ENDPOINT"] = rcb1
    except Exception, e:
        print e
        return JSONEncoder1().encode([{"error": str(e)}])
    res = os.environ["CYCLOPS_ENDPOINT"]
    return JSONEncoder1().encode([{"localhost": res}])


app.run(host='0.0.0.0', port=50003, debug=True)
