
def run():
    import json

    Db = "db/SPOC.db"
    TABLE_NAME = "SPOC"
    file_path = "G:/Python/Python-Server/jsons/outputSpocs.json"

    # Read JSON data from the file
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    # Initialize an empty dictionary to store column names and their data types
    column_data_types = {}

    # Iterate over each item in the JSON data
    for item in data:
        # Iterate over each key-value pair in the item
        for key, value in item.items():
            # Check if the column name already exists in the dictionary
            if key not in column_data_types:
                # If not, add the column name with its data type
                column_data_types[key] = type(value).__name__
            else:
                # If it exists, compare the data type and update if necessary
                current_type = type(value).__name__
                if current_type != column_data_types[key]:
                    column_data_types[key] = "Mixed"

    def get(item,key):
        try:
            return item[key]
        except:
            return None

        

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

    # Create a table if it doesn't already exist
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (Mail VARCHAR(255),Name VARCHAR(255),Comid VARCHAR(255),id VARCHAR(255) PRIMARY KEY);")




    for item in data:
        row = tuple()
        # Print the column names along with their data types
        for column, data_type in column_data_types.items():
            row += (get(item,column),)
            # print(f"{column} - {get(item,column)}: {data_type}")

        #('Shama.Anjum@transunion.com', 'Shama', '1691142826905', '1704533134284')
        try:
            cursor.execute(f"INSERT INTO {TABLE_NAME} (Mail, Name, Comid, id) VALUES (?, ?, ?, ?)", (row[0], row[1], row[2], row[3]))
        except:
            print(row)

    cursor.close()
    conn.commit()
    conn.close()
