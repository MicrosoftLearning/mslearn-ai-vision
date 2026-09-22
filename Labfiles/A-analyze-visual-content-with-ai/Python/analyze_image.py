"""
Task 3 - Wide World Importers media library tagger.

Send an image from the campaign asset library to your Azure AI Content Understanding
analyzer and print the structured Description and Tags it returns. Fill in each blank
below, then run:

    python analyze_image.py
"""

import sys
import os
from dotenv import load_dotenv

# Add references


def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    # Get configuration settings
    load_dotenv()
    endpoint = os.getenv("CONTENT_UNDERSTANDING_ENDPOINT")
    analyzer_id = os.getenv("ANALYZER_ID")
    api_version = "2025-11-01"

    # Set up Content Understanding client


    while True:
        file_no = input('\nChoose a file (1, 2, or 3), or anything else to exit: ')
        if file_no not in ["1", "2", "3"]:
            break

        file_path = f"images/image{file_no}.jpg"

        with open(file_path, "rb") as f:
            file_bytes = f.read()

        print(f"Analyzing with {analyzer_id} analyzer...")
        print(f"  File: {file_path}\n")

        # Analyze the file


if __name__ == "__main__":
    main()
