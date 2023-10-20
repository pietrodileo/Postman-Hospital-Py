import json

class CollectionItem:
    def __init__(self, base_collection_path):
        self.base_collection_path = base_collection_path
        self.itemFolder = None
        try:
            with open(self.base_collection_path, "r", encoding="utf-8") as json_file:
                self.collection_content = json.load(json_file)
                self.item_data = self.collection_content["folder"]
        except FileNotFoundError:
            print("Collection file not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON in the collection file.")
            
    def add_info(self, folderPath, itemName):
        self.itemFolder = folderPath
        if self.item_data:
            try:
                # Open and read the description.txt file
                description_file_path = folderPath + "/description.txt"
                with open(description_file_path, "r", encoding="utf-8") as description_file:
                    description_content = description_file.read()
                    self.item_data["description"] = description_content
            except FileNotFoundError:
                print(description_file_path + " file not found.")
            
            # Add an item name
            self.item_data["name"] = itemName
        else:
            print("No item data loaded. Create a CollectionItem object first.")
            
    def add_request_to_item(self, item_data):
        # add an item (request) to the folder:
        self.item_data["item"].append(item_data)