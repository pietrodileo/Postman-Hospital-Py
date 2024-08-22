import os
import sys
import json
import pandas as pd
from datetime import datetime as dt
from src.exploreJSONcontent import explore_and_save_keys
from src.buildCollection import Collection
from src.collectionItem import CollectionItem
from src.requestItem import RequestItem

# Define paths
base_collection_path = ".\models\collection\collectionContent.json"
messageModels_path = ".\models\messages"
collection_properties_path = ".\models\collection\properties.json"
censimento_xlsx = "CensimentoEnti.xlsx"

# If save_to_log_file=True, all the log will be saved in .\output\log.txt. Otherwise, they will be printed in the terminal.
def main(save_to_log_file=True, delete_old_log=True):
    # Define the log file path
    log_file_path = os.path.join(".\output", "log.txt")

    # If save_to_log_file is True and delete_old_log is True, delete the old log file if it exists
    if save_to_log_file and delete_old_log and os.path.exists(log_file_path):
        os.remove(log_file_path)
        print(f"An old log file was removed from {log_file_path}\n")

    # Read the XLSX file to obtain the data of the laboratory 
    try:
        df = pd.read_excel(censimento_xlsx, engine='openpyxl', dtype=str)
        for index, row in df.iterrows():
            row_data = row.to_dict()
            # Extract data from the XLSX file
            L1 = row_data['Codice L1']
            L2 = row_data['Codice L2']
            L3 = row_data['Codice L3']
            L4 = row_data['Codice L4']
            codAppl = str(row_data['Codice Applicativo'])
            OMRLabCode = str(row_data['Codice Laboratorio OMR'])
            collectionName = row_data['Nome Collection Postman'] + ' - ' + OMRLabCode
            nomeSoftware = str(row_data['Ospedale']) + ' - ' + str(row_data['Laboratorio'])
            applName = row_data['Nome applicativo']
            print(f"Building {collectionName} ...")
            # Define the path of the output collection
            outputCollectionName = collectionName.replace(" ", "")
            output_collection_path = f".\output\\{outputCollectionName}.postman_collection.json"
            # Run the main processing         
            if save_to_log_file:
                with open(log_file_path, "a") as log_file:  # Open the log file in append mode
                    sys.stdout = log_file
                    # Run the main function for the current collection
                    _run_main(collectionName, L1, L2,L3, L4, codAppl, OMRLabCode, nomeSoftware, applName, output_collection_path)
                    sys.stdout = sys.__stdout__
            # Build complete 
            print(f"Build Completed!\n")
    except Exception as e:
        print(f"Error reading XLSX: {e}")

def _run_main(collectionName, L1, L2, L3, L4, codAppl, OMRLabCode, nomeSoftware, applName, output_collection_path):
    # Create an instance of the Collection class
    collection = Collection(base_collection_path, collection_properties_path)

    # Load collection data from the base file
    collection.load_collection_data()

    # Build the collection specifying a name and description from a text file
    collection.build_collection(CollectionName=collectionName, descriptionPath="./models/collection/description.txt",
                                L1=L1, L2=L2, L3=L3, L4=L4, CodAppl=codAppl, OMRLabCode=OMRLabCode, 
                                NomeSoftware=nomeSoftware, ApplName=applName)

    # Load collection variables
    collection.load_variables()

    # Check if the messageModels_path exists and is a directory
    if os.path.exists(messageModels_path) and os.path.isdir(messageModels_path):
        # Insert local date and time in the log
        logTime = (f"\n\n{dt.now()} - {collectionName}\n")
        print("* " * 5 + logTime + " Adding data to the collection " + collectionName + " * " * 5)
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
                request.add_event(L1=L1, L2=L2, L3=L3, L4=L4, CodAppl=codAppl, NomeSoftware=nomeSoftware,
                                  OMRLabCode=OMRLabCode,CollectionName=collectionName, ApplName=applName)
                request.add_request_body(json_file_path=json_file_path, L1=L1, L2=L2, L3=L3, L4=L4, CodAppl=codAppl,
                                         NomeSoftware=nomeSoftware, OMRLabCode=OMRLabCode, 
                                         CollectionName=collectionName, ApplName=applName)
                item.add_request_to_item(request.request_data)

            create_daily_notification = True
            # Execute a routine for the daily notification message
            if "Daily_Notification" in folder_name:
                if create_daily_notification:
                    daily_notification_number = 10
                    print("adding a daily notification message of {daily_notification_number} requests") 
                    
                                    
            print("_" * 100)
            # Add the new folder to the collection
            collection.add_folder_to_collection(item.item_data)
    else:
        print("The messageModels_path is not a valid directory.")

    # Save the updated collection to the output file
    collection.save_collection(output_collection_path)

if __name__ == "__main__":
    main(save_to_log_file=True, delete_old_log=True)
    # save_to_log_file: Save the log to "log.txt" (or False to display on the terminal)
    # delete_old_log: Delete the old log file if True