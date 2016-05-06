import os
import calendar
import time
import uuid
import json

import falcon

# not gonna user a real database, just something in memory
max_age = 5*60

database = {}

def del_old():
    now = get_now()
    to_del = []
    for k in database:
        if now > (k + max_age):
            to_del.append(k)

    for k in to_del:
        del database[k]

def get_now():
    return int(calendar.timegm(time.gmtime()))

def slurp_and_parse(req):
    jsonbytes = b''
    if req.content_type != 'application/json':
        return None 

    while True and len(jsonbytes) < 2048:
        chunk = req.stream.read(1024)
        if not chunk:
            break
        jsonbytes += chunk

    if len(jsonbytes):
        return json.loads(jsonbytes.decode('utf-8'))
    return None 


class MeasureOneClient(object):
    def on_post(self, req, resp, userid):
        del_old()

        data = slurp_and_parse(req)
        if data is not None:
            now = get_now()
            for k in data:
                v = data[k];
                if isinstance(v,(int, float)):
                    v = float(v)
                    
                    if now not in database:
                        database[now] = {}
                    if userid not in database[now]:
                        database[now][userid] = {}

                    database[now][userid][k] = v

            resp.body = json.dumps({'message':'thanks!'})
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            resp.body = 'uh-oh'

    def on_get(self, req, resp, userid):
        since = req.get_param_as_int('since',required=False)
        if since is None:
            since = 0
        rv = {}
        for k in database:
            if k > since and userid in database[k]:
                rv[k] = database[k][userid]
        resp.body = json.dumps(rv)
        resp.status = falcon.HTTP_200


class MeasureAllClients(object):
    def on_get(self, req, resp):
        since = req.get_param_as_int('since',required=False)
        if since is None:
            since = 0
        rv = {}
        for k in database:
            if k > since:
                rv[k] = database[k]
        resp.body = json.dumps(rv)
        resp.status = falcon.HTTP_200


