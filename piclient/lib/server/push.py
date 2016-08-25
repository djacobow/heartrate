
import ssl
import http.client
import json

debug = True

class ServerPusher(object):
    def __init__(self, name, port, user):
        self.name = name
        self.port = port
        self.url = '/api/v1/users/' + user

    def push(self,data):
        # workaround for the fact that the cert on my test server
        # is self-signed and not matching to the hostname
        ctx  = ssl.create_default_context(cafile='./davej.crt')
        ctx.check_hostname = False
        conn = http.client.HTTPSConnection(self.name,port=self.port,context=ctx)
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
            if debug:
                print('Sent: ' + pdata)
            resp = conn.getresponse()
            if resp is not None:
                rstr = resp.read().decode()
                if debug:
                    print('Received: ' + resp)
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

