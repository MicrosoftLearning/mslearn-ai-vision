#pip install azure-cognitiveservices-vision-computervision
#pip install pillow  # For image processing

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import os
from PIL import Image

class AzureImageAnalyzer:
    def __init__(self, subscription_key, endpoint):
        self.client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    def analyze_image(self, image_path):
        """
        Analyzes an image and returns the analysis results.
        """
        # Open the image
        with open(image_path, "rb") as image:
            analysis = self.client.analyze_image_in_stream(image, visual_features=["Categories", "Description", "Color"])
        
        return analysis

    def describe_image(self, image_path):
        """
        Describes the contents of an image.
        """
        with open(image_path, "rb") as image:
            description = self.client.describe_image_in_stream(image)
        
        return description

    def detect_objects(self, image_path):
        """
        Detects objects in an image.
        """
        with open(image_path, "rb") as image:
            objects = self.client.detect_objects_in_stream(image)
        
        return objects

if __name__ == "__main__":
    # Replace with your Computer Vision subscription key and endpoint
    subscription_key = "YOUR_SUBSCRIPTION_KEY"
    endpoint = "YOUR_ENDPOINT"

    # Create an instance of the analyzer
    analyzer = AzureImageAnalyzer(subscription_key, endpoint)

    # Analyze an image
    image_path = "path_to_your_image.jpg"
    analysis = analyzer.analyze_image(image_path)
    print("Analysis Results:", analysis)

    # Describe an image
    description = analyzer.describe_image(image_path)
    print("Image Description:", description)

    # Detect objects in an image
    objects = analyzer.detect_objects(image_path)
    print("Detected Objects:", objects)
