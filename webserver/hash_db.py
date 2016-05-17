import calendar
import time

def get_now():
    return int(calendar.timegm(time.gmtime()))

class SimpleDB(object):
    def __init__(self,max_age=5*60):
        self._db = {}
        self.max_age = max_age
    def del_old(self):
        now = get_now()
        to_del = []
        for k in self._db:
            if now > (k + self.max_age):
                to_del.append(k)
        for k in to_del:
            del self._db[k]

    def add(self,data,userid):
        if data is not None:
            now = get_now()
            for k in data:
                v = data[k];
                if isinstance(v,(int, float)):
                    v = float(v)
                    
                    if now not in self._db:
                        self._db[now] = {}
                    if userid not in self._db[now]:
                        self._db[now][userid] = {}

                    self._db[now][userid][k] = v

    def get(self,since=0,userid=None):
        rv = {}
        for k in self._db:
            if k > since:
                if userid is not None and userid in self._db[k]:
                    rv[k] = self._db[k][userid]
                else:
                    rv[k] = self._db[k]
        return rv



