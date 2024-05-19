import json
import os
from .urlParser import UrlParser
from .modifyText import TextModifier

class RequestItem:
    def __init__(self, base_collection_path, item_folder):
        self.base_collection_path = base_collection_path
        self.itemFolder = item_folder
        try:
            with open(self.base_collection_path, "r", encoding="utf-8") as json_file:
                self.collection_content = json.load(json_file)
            
            self.request_data = self.collection_content["request"]
        except FileNotFoundError:
            print("Collection file not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON in the collection file.")
            
    def add_info(self, itemName, collection_properties_path):
        if self.request_data:            
            # Add an item name
            self.request_data["name"] = itemName.replace("_", " ")

            # Open and read the collection properties JSON file
            try:
                with open(collection_properties_path, "r", encoding="utf-8") as properties_file:
                    collection_properties = json.load(properties_file)
                # Add HTTP method
                self.request_data["request"]["method"] = collection_properties["method"]
                # Add URL
                self.request_data["request"]["url"]["raw"] = collection_properties["URL"]
                # Extract information from the URL
                urlParser = UrlParser(collection_properties["URL"])
                # Add information from the URL
                self.request_data["request"]["url"]["host"].append(urlParser.url_info["host"])
                self.request_data["request"]["url"]["port"] = urlParser.url_info["port"]
                self.request_data["request"]["url"]["path"] = urlParser.url_info["path"]
                self.request_data["request"]["url"]["path"].append("")
                self.request_data["request"]["url"]["query"] = urlParser.url_info["query"]
                
            except FileNotFoundError:
                print(f"Collection properties file not found at '{collection_properties_path}'")
            except json.JSONDecodeError:
                print(f"Error decoding JSON in the collection properties file.")
        else:
            print("No item data loaded. Create a RequestItem object first.")
            
    def add_event(self, L1, L2, L3, L4, CodAppl, NomeSoftware, CollectionName, ApplName):
        # Define the paths for pre-request and test scripts
        pre_req_script_path = os.path.join(self.itemFolder, "preRequestScript.txt")
        test_script_path = os.path.join(self.itemFolder, "testScript.txt")
        generic_test_script_path = "models\\collection\\generic_test_script.txt"
        
        # Add the pre-request script
        if os.path.exists(pre_req_script_path):
            with open(pre_req_script_path, "r", encoding="utf-8") as pre_req:
                pre_req_content = pre_req.read()
            # Modify text
            textMod = TextModifier(pre_req_content)
            textMod.replace_placeholders(L1, L2, L3, L4, CodAppl, NomeSoftware, CollectionName, ApplName)
            self.request_data["event"][0]["script"]["exec"] = textMod.text
        else:
            print(f"Pre-request script not found at '"+pre_req_script_path)

        # Add the generic test script
        with open(generic_test_script_path, "r", encoding="utf-8") as test:
            generic_test_content = test.read()

        # Add custom test script
        if os.path.exists(test_script_path):
            with open(test_script_path, "r", encoding="utf-8") as test:
                custom_test_content = test.read()
            # Modify text
            textModTest = TextModifier(custom_test_content)
            textModTest.replace_placeholders(L1, L2, L3, L4, CodAppl, NomeSoftware, CollectionName, ApplName)
            # append the generic test content
            textModTest.append_texts(generic_test_content)
            self.request_data["event"][1]["script"]["exec"] = textModTest.text
        else:
            print(f"Custom test script not found at {test_script_path}. Generic test script will be used.")
            # Modify text
            textModTest = TextModifier(generic_test_content)
            textModTest.replace_placeholders(L1, L2, L3, L4, CodAppl, NomeSoftware, CollectionName, ApplName)
            self.request_data["event"][1]["script"]["exec"] = textModTest.text

    def add_request_body(self, json_file_path, L1, L2, L3, L4, CodAppl, NomeSoftware, CollectionName, ApplName):
        try:
            with open(json_file_path, "r", encoding="utf-8") as json_file:
                request_body = json.load(json_file)
                if isinstance(request_body, dict):
                    # If request_body is a dictionary, convert it to a JSON string (basically a string of text)
                    request_body = json.dumps(request_body, indent=4)
                # Modify text
                textMod = TextModifier(request_body)
                textMod.replace_placeholders(L1, L2, L3, L4, CodAppl, NomeSoftware, CollectionName, ApplName)
                self.request_data["request"]["body"]["raw"] = textMod.text
        except FileNotFoundError:
            print(f"JSON file not found at: {json_file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON in the file: {json_file_path}")
    
    def add_request_to_item(self, request_data):
        # add an item (request) to the folder:
        self.request_data["item"].append(request_data)