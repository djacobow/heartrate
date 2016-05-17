import os
import calendar
import time
import sqlite3

db_filename = './demo_db.sqlite3'


def get_now():
    return int(calendar.timegm(time.gmtime()))

class SimpleDB(object):
    def __init__(self,max_age=5*60):
        self.max_age = max_age
        db_exists = os.path.isfile(db_filename)
        self._connection = sqlite3.connect(db_filename)
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
        now = get_now()
        self._cursor.execute("DELETE FROM heartrate_data WHERE timestamp < ?;",
                ((now - self.max_age),))

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



