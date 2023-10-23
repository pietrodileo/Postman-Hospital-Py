import json
import uuid
from .modifyText import TextModifier

class Collection:
    def __init__(self, base_collection_path, collection_properties_path):
        self.base_collection_path = base_collection_path
        self.collection_properties_path = collection_properties_path
        self.collection_content = None
        self.collection_data = None

    def load_collection_data(self):
        try:
            with open(self.base_collection_path, "r", encoding="utf-8") as json_file:
                self.collection_content = json.load(json_file)
                self.collection_data = self.collection_content.get("collection", {})
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error loading collection data.")

    def build_collection(self, CollectionName, descriptionPath, L1, L2, 
                         CodAppl, NomeSoftware, ApplName):
        if self.collection_data:
            try:
                # Open the description file
                with open(descriptionPath, "r", encoding="utf-8") as description_file:
                    description_content = description_file.read()
                # Modify text
                textMod = TextModifier(description_content)
                textMod.replace_placeholders(L1, L2, CodAppl, NomeSoftware, CollectionName, ApplName)
                # Insert the content of description.txt into the "description" field
                self.collection_data["info"]["description"] = textMod.text
                # Generate a collection UUID
                self.collection_data["info"]["_postman_id"] = str(uuid.uuid4())
                self.collection_data["info"]["name"] = CollectionName
            except FileNotFoundError:
                print(f"{descriptionPath} file not found.")

    def load_variables(self):
        if self.collection_data:
            self.collection_data["variable"] = self.collection_content.get("variables", {})
            # Set the URL of the Mock service
            with open(self.collection_properties_path, "r", encoding="utf-8") as json_file:
                collection_properties = json.load(json_file)
                index = self.find_key(self.collection_data["variable"], "URL_Mock")
                self.collection_data["variable"][index]["value"] = collection_properties["URL_Mock"]                
    
    def find_key(self, data, expected_key):
        for index, item in enumerate(data):
            if item.get("key") == expected_key:
                return index
        return None

    def save_collection(self, output_file_path):
        if self.collection_data:
            try:
                with open(output_file_path, "w", encoding="utf-8") as json_file:
                    json.dump(self.collection_data, json_file, indent=4)
                print(f"Collection data saved to {output_file_path}")
            except Exception as e:
                print(f"Error saving collection data: {str(e)}")
        else:
            print("No collection data to save. Call load_collection and build_collection first.")

    def add_folder_to_collection(self, item_data):
        if "item" in self.collection_data:
            # Add an item (a folder) to the collection
            self.collection_data["item"].append(item_data)
        else:
            print("Collection data is missing the 'item' key.")