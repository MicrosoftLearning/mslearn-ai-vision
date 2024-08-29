

from azure_image_analysis import AzureImageAnalyzer

# Replace with your Computer Vision subscription key and endpoint
subscription_key = "2387621a525946d482d1af7deca0f666"
endpoint = "https://k21azureaiservices.cognitiveservices.azure.com/"

# Create an instance of the analyzer
analyzer = AzureImageAnalyzer(subscription_key, endpoint)

# Analyze an image
image_path = fr'C:\Users\Ramon Aldana\mslearn\mslearn-ai-vision\Labfiles\01-analyze-images\Python\image-analysis\images\street.jpg'
analysis = analyzer.analyze_image(image_path)
print("Analysis Results:", analysis)

# Describe an image
description = analyzer.describe_image(image_path)
print("Image Description:", description)

# Detect objects in an image
objects = analyzer.detect_objects(image_path)
print("Detected Objects:", objects)
