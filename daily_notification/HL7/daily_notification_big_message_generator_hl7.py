import uuid
import random
from datetime import datetime, timedelta
import time 
import math
import os
import argparse

def generate_hl7_message(num_service_requests):

    def generate_message_header():
        current_date = datetime.now().strftime('%Y%m%d')
        current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
        msh_segment = f"MSH|^~\\&|LIS|LIS|OMR|OMR|{current_datetime}||OML^O21^OML_O21|{current_date}|P|2.5"
        return msh_segment

    def generate_orc_segment(request_id, placer_order_number):
        current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
        order_status = random.choice(["A", "R", "D"])
        orc_segment = (
            f"ORC|SC|{placer_order_number}||{request_id}|CM||1^^^^^{order_status}||{current_datetime}|"
        )
        return orc_segment

    def generate_obr_segment(placer_order_number, A1, patient, oo, exam_code, exam_description, org_info):
        current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
        obr_segment = (
            f"OBR|1|{placer_order_number}|{A1}|{exam_code}^{exam_description}||{current_datetime}|{current_datetime}|||||{patient}||||||||||||{oo}||||||||||||{current_datetime}||||||||||{org_info}"
        )
        return obr_segment

    def generate_organization_info(codiceLaboratorioOMR, L1, L2, L3, L4):
        return f"{L1}^^99OSP~{L3}^^99REP~{L2}^^99PRE~{L4}^^99UER~{codiceLaboratorioOMR}^^99CLO"

    # Generate MSH segment for the message
    msh = generate_message_header()
        
    # Define a list of random requisition numbers 
    min_length = 1  
    n = num_service_requests
    requisition_numbers = [str(uuid.uuid4()) for _ in range(random.randint(min_length, math.ceil(n / 10)))]
    print(f"number of requisition numbers: {len(requisition_numbers)}")
    
    # Define organization info
    org_info = generate_organization_info('5072024', '309672', '1234', '0801', '121314')
    
    # Generate the HL7 message
    segments = []
    for i in range(n):
        # Choose one number randomly
        requisition_number = random.choice(requisition_numbers)
        used_codes = []
        # Create a random code
        code = f"examCode-{random.randint(1, 99999)}"
        # check if code was already being used
        while code in used_codes:
            code = f"examCode-{random.randint(1, 99999)}"
        # save the code in a list 
        used_codes.append(code)
        # Create the A1 for the obr segment
        A1 = ""
        patient = "" 
        oo = ""
        if i == 0 or i == n - 1:
            A1 = "A1"
            patient = "BNCMRC77E09H264L^Bianchi^Marco"
            oo = "00"
        # Generate ORC and OBR segments
        segments.append(generate_orc_segment(code, requisition_number))
        segments.append(generate_obr_segment(requisition_number, A1, patient, oo, f"Esame-{i}", f"DescrizioneEsame-{i}",org_info))

    # Combine all segments into one HL7 message
    hl7_message = "\r".join([msh] + segments)
    
    return hl7_message    

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate HL7 message with a specified number of service requests.')
    parser.add_argument('num_service_requests', type=int, nargs='?', default=100, help='Number of service requests to generate (default: 100)')
    args = parser.parse_args()
    
    # Get the number of requests to generate by the command-line argument or default to 100
    num_service_requests = args.num_service_requests    

    # Measure start time
    start_time = time.time()
    
    # Generate HL7 message
    hl7_message = generate_hl7_message(num_service_requests)
    
    # Get the current working directory
    current_directory = os.getcwd()
    #print(f"Current directory: {current_directory}")
    # Define file paths based on the current directory
    if "daily_notification\HL7" in current_directory:
        output_path = os.path.join("generated_messages", "HL7_message.txt")
    else:
        output_path = os.path.join("daily_notification", "HL7", "generated_messages", "HL7_message.txt")

    # Write the HL7 message to a file
    with open(output_path, 'w') as f:
        f.write(hl7_message)

    print(f"HL7 message saved to {output_path}")
    print(f"A request containing {num_service_requests} exams has been generated")
    
    # Measure end time
    end_time = time.time()
    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print(f"Elapsed Time to build the message: {elapsed_time:.9f} seconds ({elapsed_time / 60:.9f} minutes)")