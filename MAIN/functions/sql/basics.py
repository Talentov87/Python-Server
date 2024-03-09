import functions.sql.handler
import json

def js(resp):
    return json.dumps(resp)

def get(TABLE_NAME,body):
    try:
        cols = body["COLUMNS"]
        cond = body["CONDITION"]
        return js(functions.sql.handler.select(TABLE_NAME,cols, cond))
    except Exception as e:  
        return "Error : "+str(e)
    
def count(TABLE_NAME,body):
    try:
        cond = body["CONDITION"]
        return js(functions.sql.handler.count(TABLE_NAME, cond))
    except Exception as e:
        return "Error : "+str(e)
    

def store(TABLE_NAME,body):
    try:
        id = body["ID"]
        data = body["DATA"]
        return functions.sql.handler.insert(TABLE_NAME,id, data)
    except Exception as e:
        return "Error : "+str(e)


def update(TABLE_NAME,body):
    try:
        data = body["DATA"]
        cond = body["CONDITION"]
        return js(functions.sql.handler.update(TABLE_NAME,cond, data))
    except Exception as e:  
        return "Error : "+str(e)
    

def delete(TABLE_NAME,body):
    try:
        cond = body["CONDITION"]
        return js(functions.sql.handler.delete(TABLE_NAME,cond))
    except Exception as e:
        return "Error : "+str(e)


def run(TABLE_NAME,body):
    try:
        qry = body["QUERY"]
        return js(functions.sql.handler.direct_query(TABLE_NAME,qry))
    except Exception as e:
        return "Error : "+str(e)
    
def get_columns(TABLE_NAME):
    try:
        return js(functions.sql.handler.get_column_names(TABLE_NAME))
    except Exception as e:
        return "Error : "+str(e)

def pragma(TABLE_NAME):
    try:
        return js(functions.sql.handler.pragma(TABLE_NAME))
    except Exception as e:
        return "Error : "+str(e)
    