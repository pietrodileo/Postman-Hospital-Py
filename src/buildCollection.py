import json
import uuid
from .modifyText import TextModifier

class Collection:
    '''
    Class 'Collection' contains the following methods:
    __init__: Initializes the class with the paths to the base collection file and the collection properties file.
    load_collection_data: Loads the base collection data from the base collection file.
    build_collection: Builds a new collection by modifying the description file and setting the collection name and UUID.
    load_variables: Loads the variables from the collection properties file and sets the URL of the Mock service.
    find_key: Finds the index of an item in a list of dictionaries based on the value of the "key" key.
    save_collection: Saves the collection data to the output file.
    add_folder_to_collection: Adds a folder to the collection.
    '''
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

    def build_collection(self, CollectionName, descriptionPath, L1, L2, L3, L4,
                         CodAppl, NomeSoftware, ApplName):
        """
        Builds a new collection by modifying the description file and setting the collection name and UUID.

        Args:
            CollectionName (str): The name of the collection.
            descriptionPath (str): The path to the description file.
            L1 (str): The first level identifier of the collection.
            L2 (str): The second level identifier of the collection.
            L3 (str): The third level identifier of the collection.
            L4 (str): The fourth level identifier of the collection.
            CodAppl (str): The application code.
            NomeSoftware (str): The name of the software.
            ApplName (str): The name of the application.

        Raises:
            FileNotFoundError: If the description file is not found.

        """
        if self.collection_data:
            try:
                # Open the description file
                with open(descriptionPath, "r", encoding="utf-8") as description_file:
                    description_content = description_file.read()
                # Modify text
                textMod = TextModifier(description_content)
                textMod.replace_placeholders(L1, L2, L3, L4, CodAppl, NomeSoftware, CollectionName, ApplName)
                # Insert the content of description.txt into the "description" field
                self.collection_data["info"]["description"] = textMod.text
                # Generate a collection UUID
                self.collection_data["info"]["_postman_id"] = str(uuid.uuid4())
                self.collection_data["info"]["name"] = CollectionName
            except FileNotFoundError:
                print(f"{descriptionPath} file not found.")

    def load_variables(self):
        """
        Loads the variables from the collection properties file and sets the URL of the Mock service.

        This function loads the variables from the collection properties file and sets the URL of the Mock service.
        It first checks if the collection data is available. If it is, it retrieves the variables from the collection content and assigns them to the `variable` key in the collection data.
        Then, it opens the collection properties file and loads the JSON content into the `collection_properties` variable.
        It finds the index of the variable with the key "URL_Mock" in the collection data and updates its value with the corresponding value from the `collection_properties` dictionary.

        """
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
        """
        Adds a folder to the collection.
        
        Parameters:
            item_data (dict): The data of the item (folder) to be added.
        """
        if "item" in self.collection_data:
            # Add an item (a folder) to the collection
            self.collection_data["item"].append(item_data)
        else:
            print("Collection data is missing the 'item' key.")