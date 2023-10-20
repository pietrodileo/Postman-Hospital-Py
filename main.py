from src.exploreJSONcontent import explore_and_save_keys
from src.buildCollection import Collection
import json

# Define the input JSON file path and the output file path for structured keys
#json_file_path = "Postman Hospital Base Model New.postman_collection.json"
#output_file_path = "structured_keys.txt"
# Call the explore_and_save_keys function to explore JSON keys and save them to the output file
#explore_and_save_keys(json_file_path, output_file_path)

base_collection_path = "./models/collection/collectionContent.json"
ouput_collection_path = "./output/collection.json"
collection = Collection(base_collection_path)
collection.load_collection_data()
collection.build_collection(name="Postman Hospital", descriptionPath= "./models/collection/description.txt")
collection.load_variables()
collection.save_collection(ouput_collection_path)