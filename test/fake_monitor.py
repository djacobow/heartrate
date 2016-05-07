#!/usr/local/bin/python3

import math
import time
import os
import http.client
import json
import uuid
import random


count = 0
res = 100

user = str(uuid.uuid4())
twopi = 2 * 3.14159656358

#host = 'localhost'
host = '52.34.85.6'


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

    conn = http.client.HTTPSConnection(host,8000)
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

