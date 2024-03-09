
def run():
    import json


    TABLE_NAME = "USERS"
    Db = "db/USERS.db"
    file_path = "G:/Python/Python-Server/jsons/outputUsers.json"

    # Read JSON data from the file
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    # Initialize an empty dictionary to store column names and their data types
    column_data_types = {'id': 'str', 'Cat': 'str', 'Type': 'str', 'Mail': 'str', 'Name': 'str', 'ProfileUrl': 'str', 'Password': 'str', 'ASSIGNED_TO': 'str'}
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
