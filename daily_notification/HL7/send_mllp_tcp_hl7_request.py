# MLLP (Minimal Lower Layer Protocol):
# Is the most common protocol used for sending HL7 messages. MLLP encapsulates the HL7 message and handles the 
# transmission over a TCP/IP connection.

import socket

def send_hl7_message(host, port, message):
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
        print(f"Received response: {response}")

# Example usage
host = '127.0.0.1'
port = 2575
message = 'MSH|^~\\&|SENDING_APP|SENDING_FAC|RECEIVING_APP|RECEIVING_FAC|202308251030||ADT^A01|MSG00001|P|2.5\rPID|||123456||DOE^JOHN'

send_hl7_message(host, port, message)
