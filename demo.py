# import sqlite3

import psycopg2
# Define your PostgreSQL connection string

IP = "52.66.183.158"

import sys

connection_pool = psycopg2.connect(f"postgresql://jay:1234@{IP}:5432/pythonhotsingdb")

print(connection_pool)

class SQLite:
    def __init__(self):
        self.conn = connection_pool
        self.cur = self.conn.cursor()
        print(self.cur)
    def cur(self):
        return self.cur
    def exe(self,qry):
        try:
            self.cur.execute(qry)
            return "ok"
        except Exception as e:
            return "Error : "+str(e)
    def close(self):
        try:
            self.conn.commit()
        except:
            pass
        # self.conn.close()

        self.cur.close()

connection = ""

def getDb():
    return SQLite()
    # return SQLite("db/"+TABLE_NAME+".db")

def getTable(TABLE_NAME):
    if("/" in TABLE_NAME):
        return TABLE_NAME.split("/")[-1]
    else:
        return TABLE_NAME
    
def insert(TABLE_NAME,id,data):
    db = getDb(TABLE_NAME)
    TABLE_NAME = getTable(TABLE_NAME)
    values = tuple()
    cols = ""
    inp = ""

    for key,val in data.items():
        inp += ",%s"
        values += (val,)
        cols += f",{key}"
        
    try:
        db.cur.execute(f"INSERT INTO {TABLE_NAME} (id{cols}) VALUES (%s{inp})", (id,)+values)
        db.close()
        return "ok"
    except Exception as e:
        db.close()
        return "Error : "+str(e)


def update(TABLE_NAME,condition,data):
    db = getDb(TABLE_NAME)
    TABLE_NAME = getTable(TABLE_NAME)
    values = tuple()
    upd = ""

    row = 0
    for key,val in data.items():
        if row > 0:
            upd+= ","
        upd += f"{key}=%s"
        values += (val,)
        row += 1
        
    try:
        # print(f"UPDATE {TABLE_NAME} SET {upd} WHERE {condition}")
        db.cur.execute(f"UPDATE {TABLE_NAME} SET {upd} WHERE {condition}", values)
        num_updated = db.cur.rowcount
        db.close()
        return str(num_updated)
    except Exception as e:
        db.close()
        return "Error : "+str(e)


def select(TABLE_NAME, cols, cond=""):
    db = getDb(TABLE_NAME)
    TABLE_NAME = getTable(TABLE_NAME)
    res = db.exe(f"SELECT {cols} FROM {TABLE_NAME} {cond}")
    if res == "ok":
        comps = db.cur.fetchall()
        resp = []
        column_names = [desc[0] for desc in db.cur.description]
        resp = [column_names] + comps
        db.close()
        return resp
    else:
        db.close()
        return res

def count(TABLE_NAME, cond=""):
    db = getDb(TABLE_NAME)
    TABLE_NAME = getTable(TABLE_NAME)
    res = db.exe(f"SELECT COUNT(ID) FROM {TABLE_NAME} {cond}")
    if res == "ok":
        count = db.cur.fetchone()[0]
        db.close()
        return count
    else:
        db.close()
        return res


def delete(TABLE_NAME, cond=""):
    db = getDb(TABLE_NAME)
    TABLE_NAME = getTable(TABLE_NAME)
    res = db.exe(f"DELETE FROM {TABLE_NAME} WHERE {cond}")
    if res == "ok":
        num_deleted = db.cur.rowcount
        db.close()
        return str(num_deleted)
    else:
        db.close()
        return res


def direct_query(query=""):
    # if query.strip().lower().startswith("create table"):
    #     # For CREATE TABLE queries
    #     return "Restricted Query"
    # elif query.strip().lower().startswith("drop table"):
    #     # For CREATE TABLE queries
    #     return "Restricted Query"

    db = getDb()
    res = db.exe(query)
    if res == "ok":
        if query.strip().lower().startswith("select"):
            comps = db.cur.fetchall()
            db.close()
            return comps
        elif query.strip().lower().startswith(("insert", "update", "delete")):
            # For INSERT, UPDATE, DELETE queries
            affected_rows = db.cur.rowcount
            db.close()
            return affected_rows
        else:
            # For other queries (e.g., ALTER TABLE, DROP TABLE, etc.)
            db.close()
            return "Query executed successfully"
    else:
        db.close()
        return res


def get_column_names(TABLE_NAME):
    db = getDb(TABLE_NAME)
    TABLE_NAME = getTable(TABLE_NAME)
    # res = db.exe(f"PRAGMA table_info({TABLE_NAME})")
    q = f"SELECT data_type,column_name FROM information_schema.columns WHERE table_name = '{TABLE_NAME.lower()}';"
    res = db.exe(q)
    if res == "ok":
        columns = [row[1] for row in db.cur.fetchall()]
        db.close()
        return columns
    else:
        db.close()
        return res


def pragma(TABLE_NAME):
    db = getDb(TABLE_NAME)
    TABLE_NAME = getTable(TABLE_NAME)
    res = db.exe(f"PRAGMA table_info({TABLE_NAME})")
    if res == "ok":
        columns = db.cur.fetchall()
        db.close()
        return columns
    else:
        db.close()
        return res



while True:
    qry = input("Query : ")
    if(qry == "exit"):
        break
    dat = direct_query(qry)
    print(dat)

