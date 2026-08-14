"""
Task 3 - Wide World Importers: animate a reference image, then remix it.

Use a product photograph as the first frame of a generated video, then remix that
video with a new creative direction. Fill in each blank below, then run:

    python video_from_image.py

The polling and download helpers are already written for you - this task focuses on
the reference-image and remix calls. Video generation typically takes 1 to 5 minutes
per video, and this script generates two.
"""

import os
import time
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

        print("Step 1: Generating a video from a reference image...")
        # Generate a video from a reference image

        if video.status == "completed":
            download_video(video.id, "image_based_video.mp4")

            print("\nStep 2: Remixing the video with a new color palette...")
            remixed = remix_video(
                video.id,
                "Shift the color palette to warm sunset tones with golden light"
            )

            if remixed.status == "completed":
                download_video(remixed.id, "remixed_video.mp4")

        print("\n=== Video generation complete ===")

    except Exception as ex:
        print(ex)


def generate_video_from_image(image_path, prompt, size="1280x720", seconds=4):
    """Generate a video using a reference image as the starting frame."""
    print(f"Starting video generation from image: {image_path}")

    # Create the video with an image reference


    print(f"Video creation started. ID: {video.id}")
    print(f"Initial status: {video.status}")

    # Poll for completion
    video = poll_video_status(video.id)
    return video


def remix_video(video_id, prompt):
    """Create a remix of an existing video with a new prompt."""
    print(f"Starting video remix for: {video_id}")

    # Remix an existing video


def poll_video_status(video_id):
    """Poll the video status every 20 seconds until it completes or fails."""
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
    print(f"Downloading video {video_id}...")
    content = client.videos.download_content(video_id, variant="video")
    content.write_to_file(output_filename)
    print(f"Saved video to {output_filename}")


if __name__ == '__main__':
    main()
