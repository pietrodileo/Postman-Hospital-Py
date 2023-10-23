import os
import sys
import json
from src.exploreJSONcontent import explore_and_save_keys
from src.buildCollection import Collection
from src.collectionItem import CollectionItem
from src.requestItem import RequestItem

# Define paths
base_collection_path = ".\models\collection\collectionContent.json"
output_collection_path = ".\output\PyHospital.postman_collection.json"
messageModels_path = ".\models\messages"
collection_properties_path = ".\models\collection\properties.json"

# If save_to_log_file=True all the log will be saved in .\output\log.txt, otherwise they will be printed in the terminal
def main(save_to_log_file=True):
    collectionName = "Postman Hospital"
    L1 = "1"
    L2 = "2"
    codAppl = "3"
    nomeSoftware = "prova"
    applName = "applName"

    if save_to_log_file:
        log_file_path = os.path.join(".\output", "log.txt")
        with open(log_file_path, "w") as log_file:
            sys.stdout = log_file
            _run_main(collectionName, L1, L2, codAppl, nomeSoftware, applName)
            sys.stdout = sys.__stdout__
            log_file.close()
    else:
        _run_main(collectionName, L1, L2, codAppl, nomeSoftware, applName)

def _run_main(collectionName, L1, L2, codAppl, nomeSoftware, applName):
    # Create an instance of the Collection class
    collection = Collection(base_collection_path, collection_properties_path)

    # Load collection data from the base file
    collection.load_collection_data()

    # Build the collection specifying a name and description from a text file
    collection.build_collection(CollectionName=collectionName, descriptionPath="./models/collection/description.txt",
                                L1=L1, L2=L2, CodAppl=codAppl, NomeSoftware=nomeSoftware, ApplName=applName)

    # Load collection variables
    collection.load_variables()

    # Check if the messageModels_path exists and is a directory
    if os.path.exists(messageModels_path) and os.path.isdir(messageModels_path):
        print("* " * 5 + " Adding data to the collection " + collectionName + " * " * 5)
        print("-" * 100)
        # List all folders in the messageModels_path
        folders = [folder for folder in os.listdir(messageModels_path) if os.path.isdir(os.path.join(messageModels_path, folder))]

        # Loop over the folders
        for folder_name in folders:
            print("- " * 5 + " Working on folder: " + folder_name + " -" * 5)
            # Add a new item for each message model (for each folder)
            item = CollectionItem(base_collection_path)
            current_folder = os.path.join(messageModels_path, folder_name)
            item.add_info(folderPath=current_folder, itemName=folder_name)
            # List all the JSON files in the current folder
            json_files = [x for x in os.listdir(current_folder) if x.endswith("json")]
            for json_file in json_files:
                json_file_path = os.path.join(current_folder, json_file)
                request = RequestItem(base_collection_path, current_folder)
                json_name = json_file[:-5]  # Remove the last 5 characters (i.e., ".json")
                request.add_info(json_name, collection_properties_path)
                request.add_event(L1=L1, L2=L2, CodAppl=codAppl, NomeSoftware=nomeSoftware,
                                  CollectionName=collectionName, ApplName=applName)
                request.add_request_body(json_file_path=json_file_path, L1=L1, L2=L2, CodAppl=codAppl,
                                         NomeSoftware=nomeSoftware, CollectionName=collectionName, ApplName=applName)
                item.add_request_to_item(request.request_data)

            print("_" * 100)
            # Add the new folder to the collection
            collection.add_folder_to_collection(item.item_data)
    else:
        print("The messageModels_path is not a valid directory.")

    # Save the updated collection to the output file
    collection.save_collection(output_collection_path)

if __name__ == "__main__":
    main(save_to_log_file=True)  # Save the log to "log.txt" (or False to display on terminal)
