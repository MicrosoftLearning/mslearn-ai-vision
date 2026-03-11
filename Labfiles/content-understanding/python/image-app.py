import os
from dotenv import load_dotenv

# Add references



load_dotenv()
endpoint = os.getenv("ENDPOINT")

# Helper function to extract the summary value from the analysis result
def getSummaryValue(result):
    return result["result"]["contents"][0]["fields"]["Summary"]["valueString"]

# Array of image URLs to process
image_urls = [
    "https://github.com/MicrosoftLearning/mslearn-ai-vision/raw/refs/heads/main/Labfiles/content-understanding/python/images/image-1.png",
    "https://github.com/MicrosoftLearning/mslearn-ai-vision/raw/refs/heads/main/Labfiles/content-understanding/python/images/image-2.png",
    "https://github.com/MicrosoftLearning/mslearn-ai-vision/raw/refs/heads/main/Labfiles/content-understanding/python/images/image-3.png"
]

# Store summaries for each image
summaries = []

# Get an access token for the Azure Cognitive Services resource



# Process each image and analyze the content
for i, image_url in enumerate(image_urls, 1):
    print(f"\n{'='*50}")
    print(f"Processing image {i}/{len(image_urls)}")
    print(f"URL: {image_url}")
    print(f"{'='*50}")
    
    # Send the image to the analyzer and get the initial response
    
    
    # Check the status of the analysis and poll if it's still running
    
    
    # Process the final result
    if result.get("status") == "Succeeded":
        summary = getSummaryValue(result)
        summaries.append({"image": i, "url": image_url, "summary": summary})
        print(f"Summary: {summary}")

    elif result.get("status") == "Failed":
        summaries.append({"image": i, "url": image_url, "summary": "FAILED"})
        print(f"Analysis failed: {result}")
        
    else:
        summaries.append({"image": i, "url": image_url, "summary": f"Error: {result}"})
        print(f"Error: {result}")

# Display all summaries when processing is complete
print(f"\n{'='*50}")
print("Image Analysis Summaries:")
print(f"{'='*50}")
for item in summaries:
    print(f"\nImage {item['image']} Summary:")
    print(f"{item['summary']}")