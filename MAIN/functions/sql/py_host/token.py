import os
import uuid
import time
import functions.sql.basics as basics

TABLE_NAME = "DataTokens"
# create table datatokens(id text primary key,data text,expires_on_epoch bigint)

def get_user_data_for_token_api(body):
    try:
        Token = body["TOKEN"]
        return get_user_data_for_token(Token)
    except Exception as e:
        return "Error : "+str(e)

def get_user_data_for_token(token):
    current_epoch_time = int(time.time())
    rows = basics.get(TABLE_NAME,{
        "COLUMNS":"data",
        "CONDITION" : f"WHERE id = '{token}' and expires_on_epoch > {current_epoch_time} limit 1"
    },True)

    if(len(rows) > 1):
        return basics.reverse_js(rows[1][0])
    else:
        return None
    
def store_token_for_user_data(data):
    new_token = str(uuid.uuid4())
    
    current_epoch_time = int(time.time())
    future_epoch_time = current_epoch_time + 3600

    basics.store(TABLE_NAME,{
        "ID":new_token,
        "DATA":{
            "data":basics.js(data),
            "expires_on_epoch":future_epoch_time
        }
    })

