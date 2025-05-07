from dotenv import load_dotenv
import os
import sys
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# Import namespaces


def main():

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        cog_key = os.getenv('AI_SERVICE_KEY')

        # Get image
        image_file = 'images/face1.jpg'
        if len(sys.argv) > 1:
            image_file = sys.argv[1]


        # Authenticate Face client



        # Specify facial features to be retrieved


        # Get faces
 
 

    except Exception as ex:
        print(ex)

def annotate_faces(image_file, detected_faces):
    print('\nAnnotating faces in image...')

    # Prepare image for drawing
    fig = plt.figure(figsize=(8, 6))
    plt.axis('off')
    image = Image.open(image_file)
    draw = ImageDraw.Draw(image)
    color = 'lightgreen'

    # Annotate each face in the image
    face_count = 0
    for face in detected_faces:
        face_count += 1
        r = face.face_rectangle
        bounding_box = ((r.left, r.top), (r.left + r.width, r.top + r.height))
        draw = ImageDraw.Draw(image)
        draw.rectangle(bounding_box, outline=color, width=5)
        annotation = 'Face number {}'.format(face_count)
        plt.annotate(annotation,(r.left, r.top), backgroundcolor=color)
    
    # Save annotated image
    plt.imshow(image)
    outputfile = 'detected_faces.jpg'
    fig.savefig(outputfile)
    print(f'  Results saved in {outputfile}\n')


if __name__ == "__main__":
    main()