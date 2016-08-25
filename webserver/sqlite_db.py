import os
import calendar
import time
import sqlite3



def get_now():
    return int(calendar.timegm(time.gmtime()))

class SimpleDB(object):
    def __init__(self,**kwargs):
        self.db_filename = './demo_db.sqlite3'
        self.really_delete_old = False
        for name, value in kwargs.items():
            if name == 'max_age':
                self.max_age = value
            elif name == 'filename':
                self.db_filename = value

        db_exists = os.path.isfile(self.db_filename)
        self._connection = sqlite3.connect(self.db_filename)
        self._cursor = self._connection.cursor()
        self.create_tables()

        
    def create_tables(self):
        sqlstr = 'CREATE TABLE IF NOT EXISTS heartrate_data(rowid INTEGER PRIMARY KEY, timestamp INTEGER, userid TEXT, patient TEXT, rate REAL)'
        print("====")
        print(sqlstr)
        print("====")
        self._cursor.execute(sqlstr)
        self._connection.commit()

    def del_old(self):
        if not self.really_delete_old:
            return
        now = get_now()
        self._cursor.execute("DELETE FROM heartrate_data WHERE timestamp < ?;", ((now - self.max_age),))


    def add(self,data,userid):
        if data is not None:
            now = get_now()
            for k in data:
                v = data[k];
                if isinstance(v,(int, float)):
                    v = float(v)
                    self._cursor.execute("INSERT INTO heartrate_data("
                            "timestamp,userid,patient,rate) VALUES (?,?,?,?)",
                            (now,userid,k,v))
                    self._connection.commit()


    def get(self,since=0,userid=None):
        rv = {}
        if userid is not None:
            qry = 'SELECT * from heartrate_data where timestamp > ? and userid = ?;'
            self._cursor.execute(qry,(since,userid))
            for record in self._cursor:
                ts = record[1]
                patient = record[3]
                rate = record[4]
                if not ts in rv:
                    rv[ts] = {}
                if not patient in rv[ts]:
                    rv[ts][patient] = rate
        else:
            qry = 'SELECT * from heartrate_data where timestamp > ?;'
            self._cursor.execute(qry,(since,))
            for record in self._cursor:
                ts = record[1]
                ruserid = record[2]
                patient = record[3]
                rate = record[4]
                if not ts in rv:
                    rv[ts] = {}
                if not ruserid in rv[ts]:
                    rv[ts][ruserid] = {}
                rv[ts][ruserid][patient] = rate
        return rv



