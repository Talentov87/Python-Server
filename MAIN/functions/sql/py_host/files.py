
import functions.sql.handler as Db
from functions.sql.py_host.token import get_user_data_for_token
import json
import datetime

Root_URL = "https://jayservice.fun:7777/service"

def listToJson(lis):
    return json.dumps(lis)

def jsonToList(jso):
    if(jso == None or jso == ""):
        return []
    return json.loads(jso)

def getTimeFromEpoch(epoch_time,format="%d/%m/%Y %I:%M %p"):
    # Convert epoch time to a datetime object
    dt_object = datetime.datetime.fromtimestamp(int(epoch_time))

    # Format the datetime object as "dd/MM/yyyy hh:mm a"
    formatted_datetime = dt_object.strftime(format)
    return formatted_datetime

def get_hosted_functions_api(body):
    try:
        Token = body["TOKEN"]

        userData = get_user_data_for_token(Token)
        if(userData == None):
            return None
        
        api_log_total_and_average = Db.select("execution_logs", "python_file_name, executed_function_name AS endpoint, AVG(elapsed_time) AS avg_elapsed_time, SUM(elapsed_time) AS total_elapsed_time, AVG(request_body_size) AS avg_request_body_size, SUM(request_body_size) AS total_request_body_size, AVG(response_body_size) AS avg_response_body_size, SUM(response_body_size) AS total_response_body_size, COUNT(*) AS total_executions", f"WHERE user_uid='{userData['id']}' GROUP BY python_file_name, executed_function_name")

        api_log_total_and_average = api_log_total_and_average[1:]

        # python_file_name, endpoint,     avg_elapsed_time,   total_elapsed_time, avg_request_body_size,  total_request_body_size,    avg_response_body_size, total_response_body_size, total_executions
        # 0                 1             2                   3                   4                       5                           6                       7                         8


        AllPyFiles = Db.select("hosted_files","id,file_name,functions,updated_on,file_size_in_bytes",f"WHERE user_id = '{userData["id"]}'")[1:]
        # id,   file_name,  functions,  updated_on, file_size_in_bytes
        # 0     1           2           3           4

        file_data = {}  # Dictionary to store file names and their functions

        for pf in AllPyFiles:
            file_name = pf[1]
            list_funtions = jsonToList(pf[2])
            functions = list_funtions
            for function in functions:
                Db.select("execution_logs","AVG(elapsed_time) AS avg_elapsed_time, SUM(elapsed_time) AS total_elapsed_time, AVG(request_body_size) AS avg_request_body_size, SUM(request_body_size) AS total_request_body_size, AVG(response_body_size) AS avg_response_body_size, SUM(response_body_size) AS total_response_body_size",f"WHERE user_uid='{userData["id"]}' and python_file_name='{file_name}' and executed_function_name='{function}'")
            functions_count = len(list_funtions)
            f_id = pf[0]
            f_size = pf[4]
            if file_name not in file_data:
                file_data[file_name] = {"functions_count":functions_count,"functions":functions,"f_size":f_size,"f_id":f_id,"updated_on":getTimeFromEpoch(pf[3])}

        # Sort file_data by file name for consistent order
        sorted_file_data = dict(sorted(file_data.items()))

        return {"FileData":sorted_file_data,"BaseUrl":Root_URL+"/"+userData["id"],"ApiLog":api_log_total_and_average}

    except Exception as e:
        return "Error : "+str(e)



def get_hosted_files_api(body):
    try:
        Token = body["TOKEN"]

        userData = get_user_data_for_token(Token)
        if(userData == None):
            return None

        AllPyFiles = Db.select("hosted_files","id,file_name,functions,updated_on,file_size_in_bytes",f"WHERE user_id = '{userData["id"]}'")[1:]
        # id,   file_name,  functions,  updated_on, file_size_in_bytes
        # 0     1           2           3           4

        file_data = {}  # Dictionary to store file names and their functions

        for pf in AllPyFiles:
            file_name = pf[1]
            list_funtions = jsonToList(pf[2])
            functions = list_funtions
            functions_count = len(list_funtions)
            f_id = pf[0]
            f_size = pf[4]
            if file_name not in file_data:
                file_data[file_name] = {"functions_count":functions_count,"functions":functions,"f_size":f_size,"f_id":f_id,"updated_on":getTimeFromEpoch(pf[3])}

        # Sort file_data by file name for consistent order
        sorted_file_data = dict(sorted(file_data.items()))

        return {"sorted_file_data":sorted_file_data}
        
    except Exception as e:
        return "Error : "+str(e)
