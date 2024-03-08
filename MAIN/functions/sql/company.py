import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('company.db')



class SQLite:
    def __init__(self):
        self.conn = sqlite3.connect('company.db')
        self.cur = self.conn.cursor()
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
            self.cur.close()
        except:
            pass
        try:
            self.conn.commit()
        except:
            pass
        self.conn.close()

# Create a cursor object to execute SQL commands
cur = conn.cursor()

TABLE_NAME = 'COMPANY';

# Create a table
cur.execute(f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (NAME VARCHAR(255),id VARCHAR(255) PRIMARY KEY);
            ''')

cur.close()
conn.commit()
# conn.close()

def insert(id,name):
    db = SQLite()
    try:
        db.cur.execute(f"INSERT INTO {TABLE_NAME} (id, NAME) VALUES (?, ?)", (id, name))
        db.close()
        return "ok"
    except Exception as e:
        db.close()
        return "Error : "+str(e)


def select(cols,where = ""):
    db = SQLite()
    res = "ok"
    if(where == ""):
        res = db.exe(f"SELECT {cols} FROM {TABLE_NAME}")
    else:
        res = db.exe(f"SELECT {cols} FROM {TABLE_NAME} WHERE {where}")
    if(res == "ok"):
        comps = db.cur.fetchall()
        db.close()
        return str(comps)
    else:
        return res





def get(body):
    try:
        cols = body["COLUMNS"]
        where = body["WHERE"]
        return select(cols, where)
    except Exception as e:
        return "Error : "+str(e)
    

def store(body):
    try:
        id = body["ID"]
        name = body["NAME"]
        return insert(id, name)
    except Exception as e:
        return "Error : "+str(e)