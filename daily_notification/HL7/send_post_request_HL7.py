import requests
import json
import os
import time 
from datetime import datetime

# Define the paths
input_file_path = "HL7_message.txt"
output_file_path = os.path.join("daily_notification", "HL7", "output", "daily_notification_response.json")

# Read the JSON message from the file
with open(input_file_path, 'r') as file:
    hl7_message = file.read()

# URL to send the POST request to
url = "http://localhost:8002/lombardia/retelaboratori/fhir/HTTP_To_HL7_Converter/?prova=prova&prova2=prova2"

# Headers
headers = {
    "Content-Type": "application/hl7-v2",  
    "Accept": "application/hl7-v2"
}

# Measure start time
start_time = time.time()

# print datetime with millisecond precision when message is sent
print(f"Message sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")

# Send the POST request
response = requests.post(url, headers=headers, data=hl7_message)

# Measure end time
end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time

# Get the response status code
status_code = response.status_code

# Get the response
response_text = response.text

# Print the response
print(f"HTTP Status Code: {status_code}")
print(f"Elapsed Time: {elapsed_time:.9f} seconds ({elapsed_time / 60:.9f} minutes)")
#print("Response Text:")
#print(response_text)

# Create the output directory if it does not exist
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Save the response to the output file
with open(output_file_path, 'w') as file:
    json.dump(response_text, file, indent=4)

print(f"Response saved to {output_file_path}")