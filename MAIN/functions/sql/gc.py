import os

def get_table_name():
    current_file = os.path.basename(__file__)
    return current_file.upper().replace(".PY","")

TABLE_NAME = "ALLUSERS"

import functions.sql.basics

get = lambda body:functions.sql.basics.get(TABLE_NAME,body)
count = lambda body:functions.sql.basics.count(TABLE_NAME,body)
store = lambda body:functions.sql.basics.store(TABLE_NAME,body)
update = lambda body:functions.sql.basics.update(TABLE_NAME,body)
delete = lambda body:functions.sql.basics.delete(TABLE_NAME,body)
run = functions.sql.basics.run
js = functions.sql.basics.js


getDb = functions.sql.basics.getDb



def get_columns():return functions.sql.basics.get_columns(TABLE_NAME)
def pragma():return functions.sql.basics.pragma(TABLE_NAME)

try:
    os.mkdir("db")
except:
    pass


ALLUSERS_QRY = "CREATE TABLE IF NOT EXISTS "+TABLE_NAME+" (id VARCHAR(255) PRIMARY KEY,Email VARCHAR(255),Phone VARCHAR(255),FirstName VARCHAR(255),LastName VARCHAR(255),Photo VARCHAR(255),FullName VARCHAR(255));"
run(TABLE_NAME,{"QUERY":ALLUSERS_QRY},True)

def init_user(user_id):
    USER_CHAT_LIST_TABLE_NAME = user_id + "_USER_CHAT_LIST"
    CHAT_LIST_TABLE_NAME = user_id + "_CHAT_LIST"
    
    USER_CHAT_LIST = "CREATE TABLE IF NOT EXISTS "+USER_CHAT_LIST_TABLE_NAME+" (id VARCHAR(255) PRIMARY KEY,UNREAD INTEGER,LASTMESSAGE VARCHAR(255),LASTMESSAGEMS INTEGER);"
    CHAT_LIST = "CREATE TABLE IF NOT EXISTS "+CHAT_LIST_TABLE_NAME+" (mid VARCHAR(255) PRIMARY KEY, id VARCHAR(255),type VARCHAR(255),isStorable BOOLEAN,isLarge BOOLEAN,previewText TEXT,content TEXT,from_user VARCHAR(255),to_user VARCHAR(255),stage INTEGER,startOn INTEGER,sentOn INTEGER,receivedOn INTEGER,viewedOn INTEGER)"
    
    run(USER_CHAT_LIST_TABLE_NAME,{"QUERY":USER_CHAT_LIST},True)
    run(CHAT_LIST_TABLE_NAME,{"QUERY":CHAT_LIST},True)


def get_chat_list(body):
    try:
        user_id = body["UID"]
        init_user(user_id)
        List_of_chat_messages = functions.sql.basics.get(user_id+"_CHAT_LIST",{"COLUMNS":"id, mid, type, isStorable, isLarge, previewText, content, from_user, to_user, stage, startOn, sentOn, receivedOn, viewedOn","CONDITION":"WHERE id = '"+body["ID"]+"'"},True)
        return js(List_of_chat_messages)
    except Exception as e:
        return "Error : "+str(e)


def add_chat_list(body):
    try:
        user_id = body["UID"]

        txt_msg = body["DATA"]["isLarge"]
        if(txt_msg == True):
            txt_msg = body["DATA"]["previewText"]
        else:
            txt_msg = body["DATA"]["content"]
        
        run(user_id + "_USER_CHAT_LIST",{"QUERY":"UPDATE "+user_id + "_USER_CHAT_LIST"+" SET UNREAD=0,LASTMESSAGE='"+txt_msg+"',LASTMESSAGEMS="+str(body["DATA"]["startOn"])+" WHERE id='"+body["DATA"]["to_user"]+"'"},True)
        count = run(body["DATA"]["to_user"] + "_USER_CHAT_LIST",{"QUERY":"UPDATE "+body["DATA"]["to_user"] + "_USER_CHAT_LIST"+" SET UNREAD=UNREAD+1,LASTMESSAGE='"+txt_msg+"',LASTMESSAGEMS="+str(body["DATA"]["startOn"])+" WHERE id='"+user_id+"'"},True)
        if(count == 0):
            add_user_chat_list({
                "UID":body["DATA"]["to_user"],
                "ID":user_id,
                "DATA":{
                    "UNREAD":1,
                    "LASTMESSAGE":txt_msg,
                    "LASTMESSAGEMS":body["DATA"]["startOn"]
                }
            })
        return js(functions.sql.basics.store(user_id+"_CHAT_LIST",body))
    except Exception as e:
        return "Error : "+str(e)
    
def get_user_chat_list(body):
    try:
        user_id = body["UID"]
        init_user(user_id)

        List_of_chat_users = functions.sql.basics.get(user_id+"_USER_CHAT_LIST",{"COLUMNS":"UNREAD,LASTMESSAGE,LASTMESSAGEMS,id","CONDITION":""},True)

        columns = List_of_chat_users[0]+functions.sql.basics.get_columns(TABLE_NAME,True)[1:]

        List_of_chat_users[0] = columns

        for i in range(1,len(List_of_chat_users)):
            try:
                other_user_record = functions.sql.basics.get(TABLE_NAME,{
                    "COLUMNS":"Email,Phone,FirstName,LastName,Photo,FullName",
                    "CONDITION":"WHERE id = '" + List_of_chat_users[i][3] + "'"
                },True)
                List_of_chat_users[i] += tuple(other_user_record[1])
            except:
                List_of_chat_users[i] += (None,)*5
        # print(List_of_chat_users)
        return js(List_of_chat_users)
    except Exception as e:
        return "Error : "+str(e)

def add_user_chat_list(body):
    try:
        user_id = body["UID"]
        init_user(user_id)
        return js(functions.sql.basics.store(user_id+"_USER_CHAT_LIST",body))
    except Exception as e:
        return "Error : "+str(e)


def update_user_chat_list(body):
    try:
        user_id = body["UID"]
        init_user(user_id)
        return js(functions.sql.basics.update(user_id+"_USER_CHAT_LIST",body,True))
    except Exception as e:
        return "Error : "+str(e)

def on_user_logged_in(body):
    try:
        user_count = functions.sql.basics.count(TABLE_NAME,{
            "CONDITION":"WHERE id = '" + body["ID"] + "'"
        },True)
        if(user_count == 0):
            suc = functions.sql.basics.store(TABLE_NAME,body)
            if("ok" == suc):
                return "OK"
            else:
                return suc
        else:
            suc = functions.sql.basics.update(TABLE_NAME,{
                "CONDITION":"id = '" + body["ID"]+"'",
                "DATA": body["DATA"]
            },True)
            if(suc == "1"):
                return "OK"
            else:
                return suc
    except Exception as e:
        return "Error : "+str(e)
    



def emailMessage(body):
    pass