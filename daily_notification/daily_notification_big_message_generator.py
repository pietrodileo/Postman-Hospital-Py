import json
import uuid
import random
import math
from datetime import datetime, timedelta
import time 

def generate_message_header():
    message_header_id = str(uuid.uuid4())
    message_header = {
        "fullUrl": "MessageHeader/"+message_header_id,
        "resource": {
            "resourceType": "MessageHeader",
            "id": message_header_id,
            "meta": {
                "versionId": "1",
                "profile": [
                    "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabMessageHeader"
                ],
                "lastUpdated": datetime.now().isoformat()
            },
            "eventCoding": {
                "system": "https://fhir.siss.regione.lombardia.it/ValueSet/CodiceEventoMessageHeader",
                "code": "OML^O21",
                "display": "OML^O21^OML_O21"
            },
            "destination": [
                {
                    "name": "OMR",
                    "endpoint": "localhost:52773/fhir/retilab/Omr"
                }
            ],
            "source": {
                "name": "{{CodiceApplicativo}}",
                "software": "{{NomeSoftware}}",
                "endpoint": "{{URL_Mock}}"
            },
            "focus": []
        }
    }
    return message_header

def generate_organization(code, system, profile, partOf=None):  
    organization_url = str(uuid.uuid4())
    code_name = f"{code}code"
    organization = {
        "fullUrl": "Organization/" + organization_url,
        "resource": {
            "resourceType": "Organization",
            "id": organization_url,
            "meta": {
                "versionId": "1",
                "profile": [
                    profile
                ]
            },
            "identifier": [
                {
                    "value": f"{{{{{code_name}}}}}",
                    "system": system
                }
            ]
        }
    }
    if partOf is not None:
        organization["resource"]["partOf"] = []
        organization["resource"]["partOf"].append(partOf) 
    return organization

def generate_service_request(code, requisition_number, l4_code):
    random_uuid = str(uuid.uuid4())
    start_date = datetime.now().isoformat()
    end_date = (datetime.now() + timedelta(days=30)).isoformat()
    categoria_ordine = random.choice(["1", "2"])
    categoria_display = "Impegnativa proveniente dal CUP" if categoria_ordine == "2" else "Richiesta"
    service_request = {
        "fullUrl": f"ServiceRequest/{random_uuid}",
        "resource": {
            "resourceType": "ServiceRequest",
            "id": random_uuid,
            "meta": {
                "versionId": "1",
                "profile": [
                    "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabServiceRequestRichiestaEsamiLab"
                ]
            },
            "identifier": [
                {
                    "system": "https://fhir.siss.regione.lombardia.it/sid/PlacerOrderNumber",
                    "value": str(uuid.uuid4())
                }
            ],
            "requisition": {
                "system": "https://fhir.siss.regione.lombardia.it/sid/PlacerRequisitionNumber",
                "value": requisition_number 
            },
            "status": "completed",
            "intent": "order",
            "category": [
                {
                    "coding": [
                        {
                            "system": "https://fhir.siss.regione.lombardia.it/Valueset/CategoriaOrdine",
                            "code": categoria_ordine,
                            "display": categoria_display
                        }
                    ]
                }
            ],
            "priority": "urgent",
            "code": {
                "coding": [
                    {
                        "display": "E00777009",
                        "code": code,
                        "system": "https://fhir.siss.regione.lombardia.it/ValueSet/CodificaPrestazioniLaboratorioRegionale"
                    },
                    {
                        "display": "11221",
                        "code": code,
                        "system": "https://fhir.siss.regione.lombardia.it/ValueSet/CodificaLocale"
                    }
                ]
            },
            "quantityQuantity": {
                "value": 1
            },
            "occurrencePeriod": {
                "start": start_date,
                "end": end_date
            },
            "subject": {
                "type": "Patient"
            },
            "authoredOn": start_date,
            "performer": [
                {
                    "reference": l4_code
                }
            ]
        }
    }
    return service_request

def generate_bundle(n):
    bundle = {
        "resourceType": "Bundle",
        "id": str(uuid.uuid4()),
        "type": "message",
        "timestamp": datetime.now().isoformat(),
        "meta": {
            "versionId": "1",
            "profile": [
                "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabBundleNotificaGiornaliera"
            ]
        },
        "entry": []
    }
    
    # Generate MessageHeader
    message_header = generate_message_header()
    bundle["entry"].append({
        "fullUrl": message_header["fullUrl"],
        "resource": message_header["resource"]
    })
    
    # Generate Organizations
    organization_profile = "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabOrganization"
    organization_l1 = generate_organization("L1", "https://fhir.siss.regione.lombardia.it/sid/codiceIdentificativoEnte", organization_profile+"L1")
    bundle["entry"].append({
        "fullUrl": organization_l1["fullUrl"],
        "resource": organization_l1["resource"]
    })
    organization_l2 = generate_organization("L2", "https://fhir.siss.regione.lombardia.it/sid/codiceMinisterialePresidio", organization_profile+"L2", organization_l1["fullUrl"])
    bundle["entry"].append({
        "fullUrl": organization_l2["fullUrl"],
        "resource": organization_l2["resource"]
    })
    organization_l3 = generate_organization("L3", "https://fhir.siss.regione.lombardia.it/sid/codiceMinisterialeReparto", organization_profile+"L3", organization_l2["fullUrl"])
    bundle["entry"].append({
        "fullUrl": organization_l3["fullUrl"],
        "resource": organization_l3["resource"]
    })
    organization_l4 = generate_organization("L4", "https://fhir.siss.regione.lombardia.it/sid/codiceMinisterialeAmbulatorio", organization_profile+"L4", organization_l3["fullUrl"])
    bundle["entry"].append({
        "fullUrl": organization_l4["fullUrl"],
        "resource": organization_l4["resource"]
    })
    
    # Define a list of random requisition numbers 
    min_length = 1  
    
    requisition_numbers = [str(uuid.uuid4()) for _ in range(random.randint(min_length, math.ceil(n / 10)))]
    print(f"number of requisition numbers: {len(requisition_numbers)}")
    
    # Generate ServiceRequests
    for i in range(n):
        # Choose one number randomly
        requisition_number = random.choice(requisition_numbers)
        used_codes = []
        # Create a random code
        code = f"code-{random.randint(1, 99999)}"
        # check if code was already being used
        while code in used_codes:
            code = f"code-{random.randint(1, 99999)}"
        # save the code in a list 
        used_codes.append(code)
        # Generate ServiceRequest
        service_request = generate_service_request(code, requisition_number, organization_l4["fullUrl"])
        # Append the ServiceRequest to the bundle
        bundle["entry"].append({
            "fullUrl": service_request["fullUrl"],
            "resource": service_request["resource"]
        })
        # append the service request url to the MessageHeader focus property
        bundle["entry"][0]["resource"]["focus"].append({"reference":service_request["fullUrl"]})
    
    return bundle

if __name__ == "__main__":
    # Measure start time
    start_time = time.time()

    num_service_requests = 40000 # Change this to the desired number of ServiceRequests
    bundle = generate_bundle(num_service_requests)
    # Write the JSON to a file
    with open('HUGE_daily_notification.json', 'w') as f:
        json.dump(bundle, f, indent=4)

    print("JSON saved to 'HUGE_daily_notification.json'")
    print(f"A request containing {num_service_requests} ServiceRequests has been generated")
    # Measure end time
    end_time = time.time()
    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print(f"Elapsed Time to build the message: {elapsed_time:.9f} seconds ({elapsed_time / 60:.9f} minutes)")