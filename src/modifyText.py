import uuid
from datetime import datetime

class TextModifier:
    def __init__(self, text):
        self.text = text

    def replace_placeholders(self, L1, L2, CodAppl, NomeSoftware, CollectionName, ApplName):
        # Generate unique IDs
        UID1 = str(uuid.uuid4())
        UID2 = str(uuid.uuid4())
        # Get the current date and time
        now = datetime.now()

        # Format the date and time as a string
        current_date = now.strftime("%m/%d/%Y, %H:%M:%S")

        # Define replacements for placeholders
        replacements = {
            'L1code_VSC': L1,
            'L2code_VSC': L2,
            'CodiceApplicativo_VSC': CodAppl,
            'NomeSoftware_VSC': NomeSoftware,
            'NomeOspedale_VSC': NomeSoftware,
            'UID_VSC': UID1,
            'UID_VSC2': UID2,
            'NomeCollection_VSC': CollectionName,
            'ApplName_VSC': ApplName,
            'currentDate_VSC': current_date
        }

        # Replace placeholders in the text
        for old_word, new_word in replacements.items():
            self.text = self.text.replace(old_word, new_word)
