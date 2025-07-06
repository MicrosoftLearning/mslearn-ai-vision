from dotenv import load_dotenv
import os
import time
import sys
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# import namespaces



def main():

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Get image
        image_file = 'images/Lincoln.jpg'
        if len(sys.argv) > 1:
            image_file = sys.argv[1]


        # Authenticate Azure AI Vision client

        
        # Read text in image
        

        # Print the text
        


    except Exception as ex:
        print(ex)

def annotate_lines(image_file, detected_text):
    print(f'\nAnnotating lines of text in image...')

     # Prepare image for drawing
    image = Image.open(image_file)
    fig = plt.figure(figsize=(image.width/100, image.height/100))
    plt.axis('off')
    draw = ImageDraw.Draw(image)
    color = 'cyan'

    for line in detected_text.blocks[0].lines:
        # Draw line bounding polygon
        r = line.bounding_polygon
        rectangle = ((r[0].x, r[0].y),(r[1].x, r[1].y),(r[2].x, r[2].y),(r[3].x, r[3].y))
        draw.polygon(rectangle, outline=color, width=3)

    # Save image
    plt.imshow(image)
    plt.tight_layout(pad=0)
    textfile = 'lines.jpg'
    fig.savefig(textfile)
    print('  Results saved in', textfile)
    
def annotate_words(image_file, detected_text):
    print(f'\nAnnotating individual words in image...')

     # Prepare image for drawing
    image = Image.open(image_file)
    fig = plt.figure(figsize=(image.width/100, image.height/100))
    plt.axis('off')
    draw = ImageDraw.Draw(image)
    color = 'cyan'

    for line in detected_text.blocks[0].lines:
        for word in line.words:
            # Draw word bounding polygon
            r = word.bounding_polygon
            rectangle = ((r[0].x, r[0].y),(r[1].x, r[1].y),(r[2].x, r[2].y),(r[3].x, r[3].y))
            draw.polygon(rectangle, outline=color, width=3)

    # Save image
    plt.imshow(image)
    plt.tight_layout(pad=0)
    textfile = 'words.jpg'
    fig.savefig(textfile)
    print('  Results saved in', textfile)



if __name__ == "__main__":
    main()
