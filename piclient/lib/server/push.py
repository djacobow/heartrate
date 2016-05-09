
import http.client
import json

class ServerPusher(object):
    def __init__(self, name, port, user):
        self.name = name
        self.port = port
        self.url = '/api/v1/users/' + user

    def push(self,data):
        conn = http.client.HTTPSConnection(self.name,self.port)
        pdata = json.dumps(data)
        headers = { 'Content-type':'application/json'}
        rval = '???' 
        try:
            if False:
                print('url:' + self.url)
                print('name:' + self.name)
                print('port:' + str(self.port))
                print('pdata:' + pdata)
            conn.request('POST', self.url, pdata, headers)
            resp = conn.getresponse()
            if resp is not None:
                rstr = resp.read().decode()
                rdata = None
                try:
                    rdata = json.loads(rstr)
                except:
                    pass
                if rdata is not None and 'message' in rdata and rdata['message'] == 'thanks!':
                    rval = 'ok'
        except Exception as e:
            print(repr(e))
            rval = 'fail'

        return rval

