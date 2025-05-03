from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw
import sys
from matplotlib import pyplot as plt
from azure.core.exceptions import HttpResponseError
import requests

# Import namespaces


def main():

    # Declare variable for Azure AI Vision client


    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Get image
        image_file = 'images/street.jpg'
        if len(sys.argv) > 1:
            image_file = sys.argv[1]


        # Authenticate Azure AI Vision client

        
        # Analyze image
        AnalyzeImage(image_file)
        
    except Exception as ex:
        print(ex)


def AnalyzeImage(image_filename):
    print(f'\nAnalyzing {image_filename}\n')

    # Use the binary file contents to pass the image data to the analyze call
    with open(image_filename, "rb") as f:
            image_data = f.read()


    # Get result with specified features to be retrieved
        

    # Display analysis results
    


if __name__ == "__main__":
    main()
