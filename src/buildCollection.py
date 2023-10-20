import json
import uuid

class Collection:
    def __init__(self, base_collection_path):
        self.base_collection_path = base_collection_path
        self.collection_content = None
        self.collection_data = None

    def load_collection_data(self):
        try:
            with open(self.base_collection_path, "r", encoding="utf-8") as json_file:
                self.collection_content = json.load(json_file)
                self.collection_data = self.collection_content["collection"]
        except FileNotFoundError:
            print("Collection file not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON in the collection file.")

    def build_collection(self, name, descriptionPath):
        if self.collection_data:
            try:
                # Open the description file
                with open(descriptionPath, "r", encoding="utf-8") as description_file:
                    description_content = description_file.read()
                # Insert the content of description.txt into the "description" field
                self.collection_data["info"]["description"] = description_content
                # Generate a collection UUID
                self.collection_data["info"]["_postman_id"] = str(uuid.uuid4())
                self.collection_data["info"]["name"] = name
            except FileNotFoundError:
                print(descriptionPath + " file not found.")
                
        else:
            print("No collection data loaded. Call load_collection_data first.")

    def load_variables(self):
        if self.collection_data:
            self.collection_data["variable"] = self.collection_content["variables"] 

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
            
    def add_item_to_collection(self, item_data):
        # add an item to the collection
        self.collection_data["item"].append(item_data)