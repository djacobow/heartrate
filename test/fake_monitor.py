#!/usr/local/bin/python3

import math
import time
import os
import ssl
import http.client
import json
import uuid
import random

use_local_server = False;

count = 0
res = 100

user = str(uuid.uuid4())
twopi = 2 * 3.14159656358

host = '52.34.85.6'
if use_local_server:
    host = 'localhost'


random.seed()

phase0 = random.uniform(0,twopi)
phase1 = random.uniform(0,twopi)

while True:
    tcount = count % res;
    a0 = twopi * float(tcount) / float(res)
    a1 = 2.0 * twopi * float(tcount) / float(res)
    a0 += phase0
    a1 += phase1

    while a0 > twopi:
        a0 -= twopi
    while a1 > twopi:
        a1 -= twopi
    v0 = 50 + 50 * math.sin(a0)
    v1 = 50 + 25 * math.cos(a1)

    conn = None
    if use_local_server:
        conn = http.client.HTTPConnection(host,8001)
    else:
        # this is a workaround for my homemade key file(s)
        ctx = ssl.create_default_context(cafile='./davej.crt')
        ctx.check_hostname = False
        conn = http.client.HTTPSConnection(host,port=8000,context=ctx)

    data = { 'var1': v0 };
    if tcount > 10 and tcount < 40:
        data['var2'] = v1

    pdata = json.dumps(data);
    headers = {'Content-type':'application/json'}
    url = '/api/v1/users/' + user
    try:
        conn.request('POST', url, pdata, headers)
        resp = conn.getresponse()
        print(resp.read().decode())
    except Exception as e:
        print("whoops:" + repr(e))

    time.sleep(1.0)
    count += 1

