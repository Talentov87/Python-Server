def run():
    import json
    
    TABLE_NAME = "COMPANY"
    Db = "db/company.db"
    file_path = "G:/Python/Python-Server/jsons/outputCompanies.json"

    # Read JSON data from the file
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    def get(item,key):
        try:
            return item[key]
        except:
            return "NULL"

        

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

    # cursor.execute(f"select * from {TABLE_NAME}")

    # recs = cursor.fetchall()

    # for rec in recs:
    #     print(rec)


    cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (NAME VARCHAR(255),id VARCHAR(255) PRIMARY KEY);")

    for item in data:
        try:
            cursor.execute(f"INSERT INTO {TABLE_NAME} (NAME, id) VALUES (?, ?)", (item["NAME"], item["id"]))
        except:
            print(item)

    cursor.close()
    conn.commit()
    conn.close()
