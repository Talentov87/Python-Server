import os

def get_table_name():
    current_file = os.path.basename(__file__)
    return current_file.upper().replace(".PY","")

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


def job_init_data(body):
    try:
        JOBID = body["JOBID"]

        JOB_DETAIL = functions.sql.basics.get(TABLE_NAME,{
            "COLUMNS": "id,Name,Comid,Description,Opening,Closed,Status,UserList,Comment,Spocid,CreatedBy,CreatedOn,CreatedOnMS",
            "CONDITION": f"WHERE id = {JOBID}"
        },True)[1]

        COMID = JOB_DETAIL[2]

        COMP_NAME = functions.sql.basics.get("COMPANY",{
            "COLUMNS": "Name",
            "CONDITION":f"WHERE id='{COMID}'"
        },True)[1][0]

        spocs = functions.sql.basics.get("SPOC",{
            "COLUMNS": "id,NAME,Mail,Comid",
            "CONDITION":f"WHERE Comid='{COMID}'"
        },True)[1:]

        AllUsers = functions.sql.basics.get("USERS",{
            "COLUMNS": "id,Name",
            "CONDITION": ""
        },True)[1:]

        return functions.sql.basics.js({
            "JOB_DETAIL": JOB_DETAIL,
            "COMID": COMID,
            "COMP_NAME": COMP_NAME,
            "spocs": spocs,
            "AllUsers": AllUsers
        })
    except Exception as e:
        return "Error : "+str(e)

