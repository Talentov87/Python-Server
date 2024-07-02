import functions.sql.handler
from functions.sql.basics import js
from functions.sql.py_host.token import get_user_data_for_token
import sys
import uuid


def get_size(obj):
    try:
        return len(str(obj).encode('utf-8')) * 8
        # return sys.getsizeof(str(obj)) * 8
    except Exception as e:
        try:
            return sys.getsizeof(obj)
        except:
            return 0

# Table execution_logs
# id text primary key,
# python_file_path text,
# user_uid text,
# python_file_name text,
# executed_function_name text,
# request_body_size NUMERIC,
# response_body_size NUMERIC,
# start_time_epoch NUMERIC,
# end_time_epoch NUMERIC,
# elapsed_time NUMERIC

def store_execution_log(file_path: str,func_name: str,request_body,response_body,TimeDurationData: dict):
    file_path = file_path.replace('\\','/')
    log_uid = str(uuid.uuid4())
    logData = {
        "python_file_path": file_path,
        "user_uid": file_path.split('/')[-2],
        "python_file_name": file_path.split('/')[-1],
        "executed_function_name": func_name,
        "request_body_size": get_size(request_body),
        "response_body_size": get_size(response_body),
        "start_time_epoch": TimeDurationData["Start"],
        "end_time_epoch": TimeDurationData["End"],
        "elapsed_time": TimeDurationData["Elapsed"]
    }

    functions.sql.handler.insert("execution_logs",log_uid, logData)



def get_log_info_api(body):
    try:
        Token = body["TOKEN"]
        User_Info = get_user_data_for_token(Token)

        if(User_Info == None):
            return None
        
        return None

    except Exception as e:
        return "Error : "+str(e)

