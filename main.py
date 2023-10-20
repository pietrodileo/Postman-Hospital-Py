import os
import json
from src.exploreJSONcontent import explore_and_save_keys
from src.buildCollection import Collection
from src.collectionItem import CollectionItem
from src.requestItem import RequestItem

# Define paths
base_collection_path = ".\models\collection\collectionContent.json"
output_collection_path = ".\output\collection.json"
messageModels_path = ".\models\messages"
collection_properties_path = ".\models\collection\properties.json"

def main():
    # Create an instance of the Collection class
    collection = Collection(base_collection_path)

    # Load collection data from the base file
    collection.load_collection_data()

    # Build the collection specifying a name and description from a text file
    collection.build_collection(name="Postman Hospital", descriptionPath="./models/collection/description.txt")

    # Load collection variables
    collection.load_variables()

    # Check if the messageModels_path exists and is a directory
    if os.path.exists(messageModels_path) and os.path.isdir(messageModels_path):
        # List all folders in the messageModels_path
        folders = [folder for folder in os.listdir(messageModels_path) if os.path.isdir(os.path.join(messageModels_path, folder))]

        # Loop over the folders
        for folder_name in folders:
            # Add a new item for each message model (for each folder)
            item = CollectionItem(base_collection_path)
            current_folder = os.path.join(messageModels_path, folder_name)
            item.add_info(folderPath=current_folder, itemName=folder_name)
            # List all the JSON file in the current folder
            json_files = [ x for x in os.listdir(current_folder) if x.endswith("json") ]
            for json_file in json_files:
                json_file_path = os.path.join(current_folder, json_file)
                request = RequestItem(base_collection_path, current_folder)
                json_name = json_file[:-5]  # Remove the last 5 characters (i.e., ".json")
                request.add_info(json_name, collection_properties_path)
                request.add_event()
                request.add_request_body(json_file_path)
                item.add_request_to_item(request.request_data)
            
            # Add the new folder to the collection
            collection.add_folder_to_collection(item.item_data)
    else:
        print("The messageModels_path is not a valid directory.")

    # Save the updated collection to the output file
    collection.save_collection(output_collection_path)

if __name__ == "__main__":
    main()
