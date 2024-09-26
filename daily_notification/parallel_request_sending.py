# This code is used to send a message many times in parallel to simulate a certain number of user behavior in the application

import requests
import json
import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

# Function to prepare and send a single HTTP request
def send_http_request(url, headers, json_message):
    try:
        # Measure start time
        print(f"Message sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        start_time = time.time()
        
        # Send the POST request
        response = requests.post(url, headers=headers, json=json_message)
        
        # Measure end time
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Get the response details
        status_code = response.status_code
        response_json = response.json()

        return {
            "status_code": status_code,
            "elapsed_time": elapsed_time,
            "response_json": response_json
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Function to send multiple requests in parallel
def send_multiple_http_requests(url, headers, json_message, n):
    results = []
    
    # Use ThreadPoolExecutor to send requests in parallel
    with ThreadPoolExecutor(max_workers=n) as executor:
        # Submit multiple requests in parallel
        futures = [executor.submit(send_http_request, url, headers, json_message) for _ in range(n)]
        
        # Collect results as they complete
        for future in as_completed(futures):
            try: 
                # Get the result of the future (the HTTP response)
                result = future.result()
                # Check if the status code indicates an error (not 200)
                result['isAnError'] = result.get('status_code') != 200 
                # Append the result to the results list
                results.append(result)
            except Exception as e:
                # Handle the exception
                print(f"An error occurred: {e}")
                pass
            
    return results

if __name__ == "__main__":
    # Define the paths
    input_file_path = os.path.join("daily_notification", "input", "HUGE_daily_notification.json")    
    output_file_path = os.path.join("daily_notification", "output", "daily_notification_response.json")
    
    # Read the JSON message from the file
    with open(input_file_path, 'r') as file:
        json_message = json.load(file)
    
    # Convert JSON object to string for placeholder replacement
    json_message_str = json.dumps(json_message)
    
    # Replace placeholders
    json_message_str = json_message_str.replace("{{CodiceApplicativo}}", "1")
    json_message_str = json_message_str.replace("{{NomeSoftware}}", "Python-Script-Laboratory")
    json_message_str = json_message_str.replace("{{URL_Mock}}", "endpoint-placer-python-script")
    json_message_str = json_message_str.replace("{{OMRLabcode}}", "5072024")
    json_message_str = json_message_str.replace("{{L1code}}", "309672")
    json_message_str = json_message_str.replace("{{L2code}}", "1234")
    json_message_str = json_message_str.replace("{{L3code}}", "0801")
    json_message_str = json_message_str.replace("{{L4code}}", "121314")
    
    # Convert string back to JSON object
    json_message = json.loads(json_message_str)
    
    # URL to send the POST request to
    url = "http://localhost:8005/lombardia/retelaboratori/fhir/DailyNotificationService/?prova=prova&prova2=prova2"
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Number of parallel requests to send
    n = 100  # Adjust the number of parallel requests here
        
    # Measure start time
    print(f"Parallel sending started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")    
    start_time_parallel = time.time()
    
    # Send requests in parallel
    responses = send_multiple_http_requests(url, headers, json_message, n)

    # Measure end time
    end_time_parallel = time.time()
    elapsed_time_parallel = end_time_parallel - start_time_parallel

    # Create the output directory if it does not exist
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    # Save the response data
    with open(output_file_path, 'w') as file:
        json.dump(responses, file, indent=4)
    
    elapsed_times = []
    # Print the responses
    for i, response in enumerate(responses, 1):
        print(f"Response {i}: Status Code: {response.get('status_code')}, Elapsed Time: {response.get('elapsed_time', 'N/A')} seconds")
        elapsed_times.append(response.get('elapsed_time'))
        #if 'error' in response:
        #    print(f"Error: {response['error']}")
        #else:
        #    print(f"Response JSON: {response['response_json']}")
        
    # Calculate sum, mean, and standard deviation
    mean_time = np.mean(elapsed_times)
    std_dev_time = np.std(elapsed_times)

    # Print results
    print(f"Mean: {mean_time:.9f} seconds")
    print(f"Standard Deviation: {std_dev_time:.9f} seconds")
    print(f"{n} requests were processed in parallel in {elapsed_time_parallel:.9f} seconds")

    print(f"Responses saved to {output_file_path}")
