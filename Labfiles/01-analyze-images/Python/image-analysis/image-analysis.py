from dotenv import load_dotenv
import os
from array import array
from PIL import Image, ImageDraw
import sys
import time
from matplotlib import pyplot as plt
import numpy as np

# Import namespaces



def main():
    global cv_client

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
        AnalyzeImage(image_file, cv_client)

        # Generate thumbnail
        BackgroundForeground(image_file, cv_client)

    except Exception as ex:
        print(ex)


def AnalyzeImage(image_file, cv_client):
    print('\nAnalyzing', image_file)

    # Specify features to be retrieved


    # Get image analysis



def BackgroundForeground(image_file, cv_client):
    print('\n')
    
    # Remove the background from the image or generate a foreground matte



if __name__ == "__main__":
    main()
