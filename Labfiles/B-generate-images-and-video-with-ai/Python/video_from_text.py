"""
Task 2 - Wide World Importers promo video from a text prompt.

Create a video generation job from a text prompt, poll it until it finishes, and
download the result. Fill in each blank below, then run:

    python video_from_text.py

Video generation typically takes 1 to 5 minutes.
"""

import os
from dotenv import load_dotenv

# Add references

# Get configuration settings
load_dotenv()
endpoint = os.getenv("OPENAI_ENDPOINT")
model_deployment = os.getenv("VIDEO_MODEL_DEPLOYMENT_NAME")

# Get the token provider for Azure OpenAI authentication


def main():

    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        print("=== Wide World Importers video generation ===\n")

        print("Step 1: Generating video from text prompt...")
        # Generate a video from a text prompt

        if video.status == "completed":
            download_video(video.id, "original_video.mp4")

        print("\n=== Video generation complete ===")

    except Exception as ex:
        print(ex)


def poll_video_status(video_id):
    """Poll the video status every 20 seconds until it completes or fails."""

    # Poll video status until completion


def download_video(video_id, output_filename="output.mp4"):
    """Download the completed video to a local file."""

    # Download the completed video


if __name__ == '__main__':
    main()
