import json

# Function to explore and visualize JSON key structure
def explore_json(json_data, prefix="", level=0):
    keys = []

    if isinstance(json_data, dict):
        for key, value in json_data.items():
            # Create a formatted key with appropriate indentation
            formatted_key = f"{'  ' * level}* {prefix}.{key}" if prefix else f"{'  ' * level}* {key}"
            keys.append(formatted_key)
            # Recursively explore sub-keys
            keys.extend(explore_json(value, formatted_key, level + 1))
    elif isinstance(json_data, list):
        for i, item in enumerate(json_data):
            # Include index in the key for list elements
            keys.extend(explore_json(item, f"{prefix}[{i}]", level))
            
    return keys

# Function to explore JSON and save keys to a file
def explore_and_save_keys(json_file_path, output_file_path):
    try:
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

            # Call the explore_json function to get structured keys
            structured_keys = explore_json(data)

            if structured_keys:
                with open(output_file_path, "w") as output_file:
                    for key in structured_keys:
                        print(key)
                        output_file.write(key + '\n')
                print(f"Structured keys saved to '{output_file_path}'.")
            else:
                print("No keys found in the JSON data.")
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Failed to decode the JSON file.")
