import requests
import json
import os
import time 
from datetime import datetime

# Define the paths
input_file_path = "HUGE_daily_notification.json"
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

# Measure start time
start_time = time.time()

# print datetime with millisecond precision when message is sent
print(f"Message sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")

# Send the POST request
response = requests.post(url, headers=headers, json=json_message)

# Measure end time
end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time

# Get the response status code
status_code = response.status_code

# Get the response JSON
response_json = response.json()

# Print the response
print(f"HTTP Status Code: {status_code}")
print(f"Elapsed Time: {elapsed_time:.9f} seconds ({elapsed_time / 60:.9f} minutes)")

# Create the output directory if it does not exist
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Save the response JSON to the output file
with open(output_file_path, 'w') as file:
    json.dump(response_json, file, indent=4)

print(f"Response JSON saved to {output_file_path}")