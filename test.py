DATABASE_URL="postgresql://AllData_owner:o8FXzqEfLvB9@ep-divine-bird-a1cvtabe.ap-southeast-1.aws.neon.tech/AllData?sslmode=require"


import os

import psycopg2


# Get the connection string from the environment variable

connection_string = DATABASE_URL



# Connect to the Postgres database

conn = psycopg2.connect(connection_string)



# Create a cursor object

cur = conn.cursor()



# Execute SQL commands to retrieve the current time and version from PostgreSQL

cur.execute('SELECT * from playing_with_neon')

time = cur.fetchall()



# cur.execute('SELECT version();')

# version = cur.fetchone()[0]



# Close the cursor and connection

cur.close()

conn.close()



# Print the results

print('Current time:', time)

# print('PostgreSQL version:', version)