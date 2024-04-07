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


def cv_details_get(body):
    candidate_id = body["ID"]
    
    cv = functions.sql.basics.get(TABLE_NAME,{
        "COLUMNS":"*",
        "CONDITION": f"WHERE id = '{candidate_id}'"
    },True)
    Cv_Column_Names = cv[0]
    if(len(cv) == 1):
        return None
    Cv_Details = cv[1]

    Comid = Cv_Details[Cv_Column_Names.index("Comid")]
    Jobid = Cv_Details[Cv_Column_Names.index("Jobid")]
    Assigned_To_UID = Cv_Details[Cv_Column_Names.index("ASSIGNED_TO")]

    Company_Name = functions.sql.basics.get("COMPANY",{
        "COLUMNS":"Name",
        "CONDITION":f"WHERE id='{Comid}'"
    },True)[1][0]

    Job_Role_Name = ""
    try:
        Job_Role_Name = functions.sql.basics.get("JOBS",{
            "COLUMNS":"Name",
            "CONDITION":f"WHERE id='{Jobid}'"
        },True)[1][0]
    except:
        Job_Role_Name = "(Role Not Found)"

    Assigned_To_Detail = functions.sql.basics.get("USERS",{
        "COLUMNS":"Name,Mail",
        "CONDITION":f"WHERE id='{Assigned_To_UID}'"
    },True)

    Assigned_To_Name = None
    Assigned_To_Email = None

    try:
        Assigned_To_Detail = Assigned_To_Detail[1]
        Assigned_To_Name = Assigned_To_Detail[0]
        Assigned_To_Email = Assigned_To_Detail[1]
    except:
        pass

    Cv_Details_Dict = {}
    for i in range(len(Cv_Details)):
        Cv_Details_Dict[Cv_Column_Names[i]] = Cv_Details[i]

    return functions.sql.basics.js({
        "Company_Name":Company_Name,
        "Job_Role_Name":Job_Role_Name,
        "Assigned_To_Name":Assigned_To_Name,
        "Assigned_To_Email":Assigned_To_Email,
        "Cv_Column_Names":Cv_Column_Names,
        "Cv_Details":Cv_Details_Dict,
    })


