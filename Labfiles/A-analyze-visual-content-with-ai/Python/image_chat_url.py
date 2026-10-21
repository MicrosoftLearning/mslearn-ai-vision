"""
Task 1 - Wide World Importers produce assistant (image from a URL).

Ask questions about an image that the model reads from a public URL.
Fill in each "# Add ..." / "# Get ..." blank below, then run:

    python image_chat_url.py
"""

import os
from dotenv import load_dotenv

# Add references


def main():

    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:

        # Get configuration settings
        load_dotenv()
        openai_endpoint = os.getenv("OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

        # Create an OpenAI client


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


    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
