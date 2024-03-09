
def run():
    import json


    TABLE_NAME = "CVS"
    Db = "db/CVS.db"
    file_path = "G:/Python/Python-Server/jsons/outputCvs.json"

    # Read JSON data from the file
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    # Initialize an empty dictionary to store column names and their data types
    column_data_types = {
    "POSITION_SHARED_DATEMS": "int",
    "EXPERIENCE_IN_SAN": "int",
    "CV_SUBMISSION_DATEMS": "int",
    "BENEFITS": "str",
    "DETAIL_PEOPLE_REPORTING": "str",
    "PhaseMS2": "int",
    "ASSIGNED_TO": "str",
    "SelectedPhaseIndex": "int",
    "STATUS": "str",
    "PROFILE_URL": "str",
    "PhaseMS1": "int",
    "QUALIFICATION": "str",
    "PhaseMS8": "int",
    "CURRENTLY_WORKS_WITH": "str",
    "MONITORING_TOOLS": "str",
    "PEOPLE_MANAGEMENT_EXPERIENCE": "str",
    "CURRENT_COMPANY": "str",
    "MANAGERIAL_YEARS_OF_EXPERIENCE": "str",
    "KEY_SYSTEMS_EXPERIENCE": "str",
    "GRADE_FITMENT": "str",
    "EMPLOYMENT_GAP": "str",
    "Jobid": "str",
    "Phase2": "str",
    "RESPONSIBILITY": "str",
    "TIME_SLOT": "str",
    "GRADE": "str",
    "HIRING_LOCATION": "str",
    "REMARKS": "str",
    "WINDOWS_AND_VMWARE": "str",
    "id": "str",
    "C_CTC_BREAKUPS": "str",
    "Phase6": "str",
    "REASON_FOR_CHANGE": "str",
    "OUR_OFFERS": "str",
    "SCRIPTING": "str",
    "FeildType": "str",
    "SelectedPhaseIndex0": "int",
    "Phase1": "str",
    "PhaseMS6": "int",
    "NO_PEOPLE_REPORTING": "str",
    "RELEVANT_YEARS_OF_EXPERIENCE": "int",
    "CONFIGURATION": "str",
    "YEAR_OF_EXPERIENCE": "int",
    "DATE_OF_SHARINGMS": "int",
    "GENDER": "str",
    "SERVER": "str",
    "E_CTC": "int",
    "CURRENT_COMPANY_AND_WORKING_SINCE": "str",
    "LINUX": "str",
    "CERTIFICATION": "str",
    "PhaseMS00": "int",
    "Comid": "str",
    "YEAR_OF_PASSING": "int",
    "E_CTC_BREAKUPS": "str",
    "SKILLS": "str",
    "CAREER_GAP": "str",
    "TEAM": "str",
    "C_CTC": "int",
    "DIVERSITY": "str",
    "CBSI_POSITION_ID": "str",
    "POSITION_SHARED_DATE": "str",
    "CANDIDATE_ID": "str",
    "CLOUD": "str",
    "Phase00": "str",
    "TICKETING_TOOL": "str",
    "CV_SUBMISSION_DATE": "str",
    "TOWER_LEAD": "str",
    "COUNTER_OFFER": "str",
    "OFFER_BREAKUPS": "str",
    "AUTOMATION": "str",
    "RESUME_URL": "str",
    "DATE_OF_SHARING": "str",
    "PhaseMS0": "int",
    "VARIABLE_PAY": "str",
    "CANDIDATE_NAME": "str",
    "COMMENTS": "str",
    "TECHNOLOGIES_WORKED_ON": "str",
    "WINDOWS": "str",
    "ORG_WORKED_WITH": "str",
    "Phase0": "str",
    "CURRENT_DESIGNATION": "str",
    "REQ_ID": "str",
    "CONTACT_NO": "str",
    "CURRENT_FIXED": "str",
    "NOTICE_PERIOD": "str",
    "DATABASE": "str",
    "POSITION_CODE": "str",
    "DATACENTRE_MANAGEMENT": "str",
    "VENDOR_NAME": "str",
    "TOTAL_JOB_CHANGES": "int",
    "Phase8": "str",
    "CURRENT_LOCATION": "str",
    "EMAIL_ID": "str",
    "STORAGE": "str",
    "CATEGORY": "str",
    "Phase5": "str",
    "PhaseMS5": "int",
    "PhaseMS7": "int",
    "Phase7": "str",
    "PhaseMS21": "int",
    "SelectedPhaseIndex2": "int",
    "Phase21": "str",
    "Phase4": "str",
    "PhaseMS4": "int",
    "CURRENT_EMPLOYER": "str",
    "PhaseMS22": "int",
    "Phase22": "str",
    "Phase20": "str",
    "PhaseMS20": "int",
    "ResonForDeclined": "str",
    "Phase3": "str",
    "PhaseMS3": "int",
    "Phase23": "str",
    "PhaseMS23": "int",
    "PhaseMS12": "int",
    "SelectedPhaseIndex1": "int",
    "Phase12": "str",
    "PhaseMS10": "int",
    "Phase10": "str",
    "SOURCED_DATEMS": "int",
    "SOURCED_DATE": "str",
    "Phase11": "str",
    "PhaseMS11": "int",
    "PhaseMS24": "int",
    "Phase24": "str",
    "CREATED_BY": "str",
    "WE_OFFERED": "str",
    "Phase04": "str",
    "PhaseMS04": "int",
    "PhaseMS02": "int",
    "Phase02": "str",
    "PhaseMS01": "int",
    "Phase01": "str",
    "PhaseMS03": "int",
    "Phase03": "str",
    "PhaseMS13": "int",
    "Phase13": "str"
    }

            

    import sqlite3

    import os

    # Check if the file exists
    if os.path.exists(Db):
        os.remove(Db)
        print("File "+Db+" has been removed.")
    else:
        print("File "+Db+" does not exist.")
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(Db)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    qry = "("
    insqry = "("
    inp = ""

    for key,typ in column_data_types.items():
        insqry += key+","

        if(typ == "int"):
            qry += f"{key} INTEGER,"
        else:
            qry += f"{key} TEXT,"
        inp += ",?"

    inp = "("+inp[1:]+")"

    insqry = insqry[:-1]+")"

    qry += "PRIMARY KEY (id))"
    # print(qry)
    # Create a table if it doesn't already exist
    q = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} "+qry+";"
    cursor.execute(q)

    i = 0
    for item in data:
        row = []
        for col,typ in column_data_types.items():
            value = None
            try:
                value = item[col]
            except:
                pass
            row.append(value)
        try:
            q1 = f"INSERT INTO {TABLE_NAME} {insqry} VALUES {inp}"
            cursor.execute(q1,row)
        except Exception as e:
            print(row)
        i+=1

    cursor.close()
    conn.commit()
    conn.close()
