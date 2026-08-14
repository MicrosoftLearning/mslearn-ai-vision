"""
Task 3 - Wide World Importers media library tagger.

Send an image from the campaign asset library to your Azure AI Content Understanding
analyzer and print the structured Description and Tags it returns.
Complete reference implementation.

    python analyze_image.py
"""

import sys
import os
from dotenv import load_dotenv

# Add references
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.ai.contentunderstanding.models import AnalysisResult
from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential


def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    # Get configuration settings
    load_dotenv()
    endpoint = os.getenv("CONTENT_UNDERSTANDING_ENDPOINT")
    analyzer_id = os.getenv("ANALYZER_ID")
    api_version = "2025-11-01"

    # Set up Content Understanding client
    credential = DefaultAzureCredential()
    client = ContentUnderstandingClient(
        endpoint=endpoint,
        credential=credential,
        api_version=api_version)

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
        try:
            poller = client.begin_analyze_binary(
                analyzer_id=analyzer_id,
                binary_input=file_bytes,
            )
            result: AnalysisResult = poller.result()
        except AzureError as err:
            print(f"[Azure Error]: {err.message}")
            sys.exit(1)
        except Exception as ex:
            print(f"[Unexpected Error]: {ex}")
            sys.exit(1)

        for field_name, field in result.contents[0].fields.items():
            if field_name == "Description":
                print(f"{field_name}:\n{field.value}\n")
            elif field_name == "Tags":
                print(f"{field_name}:")
                for tag in field.value:
                    print("  -", tag.value)


if __name__ == "__main__":
    main()
