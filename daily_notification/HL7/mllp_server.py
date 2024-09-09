# This code is used to create a simple MLLP server in Python that will listen for incoming HL7 messages on the specified host and port
# It is used to test the sending of HL7 messages over MLLP
 
import socket

def start_mllp_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"MLLP server listening on {host}:{port}...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if not data:
                    break

                # Print received HL7 message
                message = data.decode('utf-8').strip('\x0b\x1c\r')
                print(f"Received HL7 message:\n{message}")

                # Send an acknowledgment (ACK)
                ack_message = '\x0bMSH|^~\\&|ACK|...|ACK^A01|ACK001|P|2.5\x1c\r'
                conn.sendall(ack_message.encode('utf-8'))
                print(f"Sent ACK message")

# Example usage
host = '127.0.0.1'
port = 2575
start_mllp_server(host, port)
