from dotenv import load_dotenv
import os
import time
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# Import namespaces


def main():

    global cv_client

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Authenticate Azure AI Vision client
        

        # Menu for text reading functions
        print('\nChoose an image to read (or press any other key to quit):\n\n1: Lincoln.jpg\n2: Business-card.jpg\n3: Note.jpg\n\n')
        command = input('Enter a number:')
        if command == '1':
            image_file = os.path.join('images','Lincoln.jpg')
            GetTextRead(image_file)
        elif command =='2':
            image_file = os.path.join('images','Business-card.jpg')
            GetTextRead(image_file)
        elif command =='3':
            image_file = os.path.join('images','Note.jpg')
            GetTextRead(image_file)
                

    except Exception as ex:
        print(ex)

def GetTextRead(image_file):
    print('\n')

    # Open image file
    with open(image_file, "rb") as f:
            image_data = f.read()

    # Use Analyze image function to read text in image
    
    



if __name__ == "__main__":
    main()
