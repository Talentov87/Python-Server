import requests
import time

# Endpoint URL
url = 'http://ec2-13-233-48-9.ap-south-1.compute.amazonaws.com:5000/sql/company/get'

# Headers
headers = {
    'X-Encrypted-Key': 'gAkhJbEBXzR5CVj2rngd9S1kL+FFAGeAGvkmbIx1CUpvshOXceq80P58/qAKAajz',
    'Content-Type': 'application/json'
}

# JSON data
data = {
    "COLUMNS": "NAME",
    "WHERE": ""
}

# Start time
start_time = time.time()

# Sending POST request
response = requests.post(url, headers=headers, json=data)

# End time
end_time = time.time()

# Checking response status
if response.status_code == 200:
    # Success
    print("Request successful.")
    print("Response:")
    print(response.text)
else:
    # Failure
    print("Request failed with status code:", response.status_code)
    print("Response:")
    print(response.text)

# Calculate time taken
time_taken = end_time - start_time
print("Time taken:", time_taken, "seconds")
