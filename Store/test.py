import requests
import concurrent.futures

def make_request(url, headers, payload):
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code, response.json()

def test_concurrent_requests(url, headers, payload, num_requests, num_concurrent):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
        futures = [executor.submit(make_request, url, headers, payload) for _ in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            status_code, json_response = future.result()
            print(f"Response Status Code: {status_code}")
            print("Response JSON:")
            print(len(json_response))
            print("=" * 50)

if __name__ == "__main__":
    url = "http://ec2-43-205-140-144.ap-south-1.compute.amazonaws.com:5000/sql/cvs/get"
    headers = {
        "X-Encrypted-Key": "gAkhJbEBXzR5CVj2rngd9S1kL+FFAGeAGvkmbIx1CUpvshOXceq80P58/qAKAajz",
        "Content-Type": "application/json"
    }
    payload = {
        "COLUMNS": "*",
        "CONDITION": ""
    }
    num_requests = 5
    num_concurrent = 5
    test_concurrent_requests(url, headers, payload, num_requests, num_concurrent)
