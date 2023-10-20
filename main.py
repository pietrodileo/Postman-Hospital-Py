from src.exploreJSONcontent import explore_and_save_keys
import json

# Define the input JSON file path and the output file path for structured keys
json_file_path = "Postman Hospital Base Model New.postman_collection.json"
output_file_path = "structured_keys.txt"
# Call the explore_and_save_keys function to explore JSON keys and save them to the output file
explore_and_save_keys(json_file_path, output_file_path)

