import os
import functions.sql.basics as base

from fastapi import Response
from fastapi.responses import JSONResponse
import requests

LOG_FILE = '/home/ubuntu/temp/response_log.txt'

# Define the endpoint
def on_receive(request_data: dict):
    try:
        # request_data = base.js(request_data)
        # Get the data from the request
        # Define headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Referer': 'https://nestle-mall.in.net',
            'Accept': 'application/json',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        # Forward the data to another server
        response = requests.post('https://nestle-mall.in.net/demo_on_payment_occur.php', json=request_data, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            try:
                log_response_content(request_data, response.text)
                return JSONResponse(content=response.json())  # Return JSON response
            except:
                log_response_content(request_data, response.text)
                return JSONResponse(content=response.text)
        else:
            log_failed_request(request_data, response.status_code, str(response.content))
            return JSONResponse(content={"status_code":response.status_code, "detail":'Failed to forward data'})
    except Exception as e:
        log_failed_request(request_data, 500, str(e))
        return JSONResponse(content={"status_code":500, "detail":'Error forwarding data: ' + str(e)})

# Function to log request and response content to a file
def log_response_content(request_data, response_content):
    with open(LOG_FILE, 'r+') as f:
        content = f.read()
        f.seek(0, 0)  # Move the file cursor to the beginning
        f.write("REQUEST :\n{}\nRESPONSE :\n{}\n---------------------------------\n".format(request_data, response_content))
        f.write(content)  # Write back the existing content after the new log

# Function to log failed request
def log_failed_request(request_data, status_code, error_message):
    with open(LOG_FILE, 'r+') as f:
        content = f.read()
        f.seek(0, 0)  # Move the file cursor to the beginning
        f.write("FAILED REQUEST :\n{}\nSTATUS CODE :\n{}\nERROR MESSAGE :\n{}\n---------------------------------\n".format(request_data, status_code, error_message))
        f.write(content)  # Write back the existing content after the new log

# Endpoint to retrieve the log file
def get_log_file():
    try:
        with open(LOG_FILE, 'r') as f:
            file_content = f.read()
        return Response(content=file_content, media_type='text/plain')
    except Exception as e:
        return JSONResponse(content={"status_code":500, "detail":'Error reading log file: ' + str(e)})

# Endpoint to reset the log file
def reset_log_file():
    try:
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        with open(LOG_FILE, 'w') as f:
            f.write('')
        return JSONResponse(content={"message": "Log file reset successfully"})
    except Exception as e:
        return JSONResponse(content={"status_code":500, "detail":'Error resetting log file: ' + str(e)})
