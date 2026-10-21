"""
Task 1 - Wide World Importers campaign image generator.

Turn a text prompt into a campaign image and save it to the images/ folder.
Complete reference implementation.

    python image_client.py
"""

import os
import json

# Add references
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI
import base64


def main():

    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:

        # Get configuration settings
        load_dotenv()
        endpoint = os.getenv("OPENAI_ENDPOINT")
        model_deployment = os.getenv("IMAGE_MODEL_DEPLOYMENT_NAME")

        # Initialize the client
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://ai.azure.com/.default"
        )

        client = OpenAI(
            base_url=endpoint,
            api_key=token_provider(),
        )

        img_no = 0
        # Loop until the user types 'quit'
        while True:
            # Get input text
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            # Generate an image
            img = client.images.generate(
                model=model_deployment,
                prompt=input_text,
                n=1
            )

            json_response = json.loads(img.model_dump_json())
            image_data = json_response["data"][0].get("b64_json")
            image_data_in_bytes = base64.b64decode(image_data)

            # Save the image
            img_no += 1
            file_name = f"image_{img_no}.png"
            save_image(image_data_in_bytes, file_name)

    except Exception as ex:
        print(ex)


def save_image(image_data, file_name):
    # Set the directory for the stored image
    image_dir = os.path.join(os.getcwd(), 'images')

    # If the directory doesn't exist, create it
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    # Initialize the image path (note the filetype should be png)
    image_path = os.path.join(image_dir, file_name)

    # Save the generated image
    with open(image_path, "wb") as image_file:
        image_file.write(image_data)
    print(f"Image saved as {image_path}")


if __name__ == '__main__':
    main()
