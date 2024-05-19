import uuid
from datetime import datetime

class TextModifier:
    def __init__(self, text):
        self.text = text

    def append_texts(self, additional_text):
        self.text += additional_text

    def replace_placeholders(self, L1, L2, L3, L4, CodAppl, NomeSoftware, CollectionName, ApplName):
        """
        Replaces placeholders in the text with the provided values.

        Args:
            L1 (str): The value to replace the 'L1code_VSC' placeholder.
            L2 (str): The value to replace the 'L2code_VSC' placeholder.
            L3 (str): The value to replace the 'L3code_VSC' placeholder.
            L4 (str): The value to replace the 'L4code_VSC' placeholder.
            CodAppl (str): The value to replace the 'CodiceApplicativo_VSC' placeholder.
            NomeSoftware (str): The value to replace the 'NomeSoftware_VSC' and 'NomeOspedale_VSC' placeholders.
            CollectionName (str): The value to replace the 'NomeCollection_VSC' placeholder.
            ApplName (str): The value to replace the 'ApplName_VSC' placeholder.

        Returns:
            None
        """
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
            'L3code_VSC': L3,
            'L4code_VSC': L4,
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
