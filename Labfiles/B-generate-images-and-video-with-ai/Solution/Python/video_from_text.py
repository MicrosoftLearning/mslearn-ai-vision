"""
Task 2 - Wide World Importers promo video from a text prompt.

Create a video generation job from a text prompt, poll it until it finishes, and
download the result. Complete reference implementation.

    python video_from_text.py

Video generation typically takes 1 to 5 minutes.
"""

import os
from dotenv import load_dotenv

# Add references
import time
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Get configuration settings
load_dotenv()
endpoint = os.getenv("OPENAI_ENDPOINT")
model_deployment = os.getenv("VIDEO_MODEL_DEPLOYMENT_NAME")

# Get the token provider for Azure OpenAI authentication
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

# Initialize the OpenAI client with the endpoint and token provider
client = OpenAI(
    base_url=endpoint,
    api_key=token_provider(),
)


def main():

    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        print("=== Wide World Importers video generation ===\n")

        print("Step 1: Generating video from text prompt...")
        # Generate a video from a text prompt
        video = client.videos.create(
            model=model_deployment,
            prompt="A crate of fresh citrus fruit on a sunlit market stall, gentle camera push in",
            size="1280x720",
            seconds=4,
        )
        video = poll_video_status(video.id)

        if video.status == "completed":
            download_video(video.id, "original_video.mp4")

        print("\n=== Video generation complete ===")

    except Exception as ex:
        print(ex)


def poll_video_status(video_id):
    """Poll the video status every 20 seconds until it completes or fails."""

    # Poll video status until completion
    video = client.videos.retrieve(video_id)

    while video.status not in ["completed", "failed", "cancelled"]:
        print(f"Status: {video.status}. Waiting 20 seconds...")
        time.sleep(20)
        video = client.videos.retrieve(video_id)

    if video.status == "completed":
        print("Video successfully completed!")
    else:
        print(f"Video creation ended with status: {video.status}")

    return video


def download_video(video_id, output_filename="output.mp4"):
    """Download the completed video to a local file."""

    # Download the completed video
    print(f"Downloading video {video_id}...")
    content = client.videos.download_content(video_id, variant="video")
    content.write_to_file(output_filename)
    print(f"Saved video to {output_filename}")


if __name__ == '__main__':
    main()
