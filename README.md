# Postman Hospital Automation

**Note: This project is a private project of Healthy Reply.**

The **Postman Hospital Automation** project is a Python application for automating the creation of Postman collections based on data from an XLSX file. It generates Postman collections with requests, pre-request scripts, test scripts, and variables for multiple hospital laboratory entities. This code automatically creates a series of collections that can be imported into Postman and used to send clinical performance requests (*ServiceRequest*) to the OMR (*Order Manager Regionale*) through a FHIR message.

## Table of Contents

- **Prerequisites**
- **Running the Project**
- **File Descriptions**
- **Logging**

## Prerequisites

Before using this application, you'll need to have the following:

- **Python 3** installed on your system.

* It is recommended to use a Python virtual environment for managing project dependencies. You can find instructions on what a virtual environment is and how to use it in the `./utils` folder.

- Required Python packages are listed in the `requirements.txt` file. You can install them using `pip`:
- ```bash
  pip install -r requirements.txt
  ```

## Running the Project

To use the **Postman Hospital Automation** project, follow these steps:

1. Ensure you have the prerequisites installed, as mentioned in the **Prerequisites** section.
2. Place the necessary data files in the project directory:
   * `CensimentoEnti.xlsx`: Excel file containing data for generating collections.
   * Message models in the `models/messages` directory.
   * Collection properties in the `models/collection` directory.
   * Any other related data files.
3. You can execute the project by running `main.py`. It provides two options:
   * `save_to_log_file`: Set this to `True` to save the log to `log.txt`. Set to `False` to display logs in the terminal.
   * `delete_old_log`: Set this to `True` to delete the old log file if it exists.

For example:

```
python main.py --save_to_log_file True --delete_old_log True
```

By default, the generated Postman collections will be saved in the `output/` directory.

## File Descriptions

* `utils/githubCommands.md`: Contains useful GitHub commands.
* `utils/virtualEnvironmentCommands.md`: Contains useful Python virtual environment commands.
* `output/log.txt`: The log file where execution logs are saved.
* `output/*.postman_collection.json`: Generated Postman collections.
* `models/collection/`: Contains collection data and properties files.
* `models/messages/`: Contains JSON message models used to populate the Postman collection.
* `main.py`: The main script that orchestrates the collection generation process.
* `collectionItem.py`: Handles the creation of Postman collection items and folders.
* `buildCollection.py`: Manages the creation and modification of Postman collections.
* `modifyText.py`: Provides text modification capabilities, replacing placeholders in text.
* `requestItem.py`: Manages individual requests and their properties within Postman collections.
* `urlParser.py`: Parses URL information from a given URL.
* `exploreJSONcontent.py`: Provides utilities for exploring and visualizing the structure of JSON data.

## Logging

The project supports logging of the collection generation process. The log is stored in the `output/log.txt` file. You can control logging using the `save_to_log_file` and `delete_old_log` parameters in the `main.py` script.
