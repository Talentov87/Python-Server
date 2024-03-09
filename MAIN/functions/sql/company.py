import os

def get_table_name():
    current_file = os.path.basename(__file__)
    return current_file.upper().replace(".PY","")

import json
def js(resp):
    return json.dumps(resp)


TABLE_NAME = get_table_name()

import functions.sql.basics

get = lambda body:functions.sql.basics.get(TABLE_NAME,body)
count = lambda body:functions.sql.basics.count(TABLE_NAME,body)
store = lambda body:functions.sql.basics.store(TABLE_NAME,body)
update = lambda body:functions.sql.basics.update(TABLE_NAME,body)
delete = lambda body:functions.sql.basics.delete(TABLE_NAME,body)
run = lambda body:functions.sql.basics.run(TABLE_NAME,body)
def get_columns():return functions.sql.basics.get_columns(TABLE_NAME)
def pragma():return functions.sql.basics.pragma(TABLE_NAME)



def get_job_states_and_spocs_for_all():
    counts = {}
    companies = functions.sql.basics.get(TABLE_NAME,{
        "COLUMNS": "id",
        "CONDITION": ""
    },True)[1:]


    for company in companies:
        comid = company[0]

        active = functions.sql.basics.count("JOBS",{
            "CONDITION":f"WHERE Comid='{comid}' and Status = '0'"
        },True)
        closed = functions.sql.basics.count("JOBS",{
            "CONDITION":f"WHERE Comid='{comid}' and Status = '1'"
        },True)
        hold = functions.sql.basics.count("JOBS",{
            "CONDITION":f"WHERE Comid='{comid}' and Status = '2'"
        },True)
        unset = functions.sql.basics.count("JOBS",{
            "CONDITION":f"WHERE Comid='{comid}' and Status != '0' and Status != '1' and Status != '2'"
        },True)
        total = functions.sql.basics.count("JOBS",{
            "CONDITION":f"WHERE Comid='{comid}'"
        },True)

        spocs = functions.sql.basics.get("SPOC",{
            "COLUMNS": "Name",
            "CONDITION": f"WHERE Comid = '{comid}'"
        },True)[1:]

        #0 index - id
        counts[comid] = {
            "active":active,
            "closed":closed,
            "hold":hold,
            "unset":unset,
            "total":total,
            "spocs":spocs,
        }
    return js(counts)
    
