"""
Task 2 - Wide World Importers produce assistant (local image file).

Same assistant as Task 1, but the image is read from disk and sent to the model
as a base64 data URL instead of a public link. Complete reference implementation.

    python image_chat_local.py
"""

import os
import base64
from pathlib import Path
from dotenv import load_dotenv

# Add references
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


def main():

    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:

        # Get configuration settings
        load_dotenv()
        openai_endpoint = os.getenv("OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

        # Create an OpenAI client
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
        client = OpenAI(
            base_url=openai_endpoint,
            api_key=token_provider()
        )

        # Initialize prompts
        system_message = (
            "You are an AI assistant for Wide World Importers, a specialty grocery "
            "importer. You provide detailed answers to questions about imported produce."
        )
        prompt = ""

        # Loop until the user types 'quit'
        while True:
            prompt = input("\nAsk a question about the image\n(or type 'quit' to exit)\n")
            if prompt.lower() == "quit":
                break
            elif len(prompt) == 0:
                print("Please enter a question.\n")
            else:
                print("Getting a response ...\n")

                # Get a response to image input
                image_path = Path("mystery-fruit.jpeg")
                image_format = "jpeg"
                with open(image_path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode("utf-8")

                data_url = f"data:image/{image_format};base64,{image_data}"

                response = client.responses.create(
                    model=model_deployment,
                    input=[
                        {"role": "developer", "content": system_message},
                        {"role": "user", "content": [
                            {"type": "input_text", "text": prompt},
                            {"type": "input_image", "image_url": data_url}
                        ]}
                    ]
                )
                print(response.output_text)

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
