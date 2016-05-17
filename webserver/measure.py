import os
import uuid
import json
import falcon
#import hash_db as dbwrap
import sqlite_db as dbwrap


db = dbwrap.SimpleDB()


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
        db.del_old()

        data = slurp_and_parse(req)
        if data is not None:
            db.add(data,userid)
            resp.body = json.dumps({'message':'thanks!'})
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
            resp.body = 'uh-oh'

    def on_get(self, req, resp, userid):
        since = req.get_param_as_int('since',required=False)
        if since is None:
            since = 0
        rv = db.get(since, userid)
        resp.body = json.dumps(rv)
        resp.status = falcon.HTTP_200


class MeasureAllClients(object):
    def on_get(self, req, resp):
        since = req.get_param_as_int('since',required=False)
        if since is None:
            since = 0
        rv = db.get(since)
        resp.body = json.dumps(rv)
        resp.status = falcon.HTTP_200


