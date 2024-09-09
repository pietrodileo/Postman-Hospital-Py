# MLLP (Minimal Lower Layer Protocol):
# Is the most common protocol used for sending HL7 messages. MLLP encapsulates the HL7 message and handles the 
# transmission over a TCP/IP connection.

import socket
import os 
import time 
from datetime import datetime

def send_hl7_message(host, port, message):
    # Ensure segments are separated by '\r' instead of '\n' or '\r\n'
    message = message.replace('\n', '\r').replace('\r\r', '\r')

    # Prepare the MLLP envelope
    start_block = '\x0b'  # <VT>
    end_block = '\x1c'    # <FS>
    carriage_return = '\x0d'  # <CR>

    # Encapsulate the message
    hl7_message = f"{start_block}{message}{end_block}{carriage_return}"

    # Open a socket connection to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(hl7_message.encode('utf-8'))

        # Receive acknowledgment from the server
        response = s.recv(1024).decode('utf-8')
        
        # Remove the MLLP envelope from the received response
        response = response.strip(start_block + end_block + carriage_return)
        
        return response

if __name__ == "__main__":
    # Get the current working directory
    current_directory = os.getcwd()
    #print(f"Current directory: {current_directory}")
    # Define file paths based on the current directory
    if "daily_notification\HL7" in current_directory:
        input_file_path = os.path.join("generated_messages", "HL7_message.txt")
        output_file_path = os.path.join("output", "hl7_daily_notification_response.txt")
    else:
        input_file_path = os.path.join("daily_notification", "HL7", "generated_messages", "HL7_message.txt")
        output_file_path = os.path.join("daily_notification", "HL7", "output", "hl7_daily_notification_response.txt")

    # Read the JSON message from the file
    with open(input_file_path, 'r') as file:
        hl7_message = file.read()

    # Measure start time
    start_time = time.time()

    # print datetime with millisecond precision when message is sent
    print(f"Message sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")

    # Example usage
    host = 'localhost'
    port = 8006
    # Sending to the BS "BARNUM_HL7_Service"
    response = send_hl7_message(host, port, hl7_message)

    # Measure end time
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time

    # Get the response status code
    response_status = "error" if "ERR" in response else "ok"

    # Print the response
    #print(f"Received response: \n{response}")
    print(f"Responde Status: {response_status}")
    print(f"Elapsed Time: {elapsed_time:.9f} seconds ({elapsed_time / 60:.9f} minutes)")

    # Create the output directory if it does not exist
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Write the HL7 message to a file
    with open(output_file_path, 'w') as f:
        f.write(response)

    print(f"Response saved to {output_file_path}")