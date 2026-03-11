---
lab:
  title: Analyze images with Azure Content Understanding
  description: Learn how to use Azure Content Understanding to analyze images and generate descriptive metadata.
  level: 300
  duration: 30
  islab: true
  primarytopics:
    - Azure
    - Azure Content Understanding
---

# Analyze images with Azure Content Understanding

Azure Content Understanding is a capability available in Microsoft Azure AI Foundry that uses generative AI to analyze and interpret different types of unstructured content, including documents, images, audio, and video. By applying AI models to this content, the service can generate structured outputs that follow a user-defined schema. These structured outputs make it easier to integrate extracted information into automation, analytics, and search workflows.

One common challenge organizations face is managing large collections of visual content. Images often contain valuable information, but that information can be difficult to search or organize without descriptive metadata. Azure Content Understanding can analyze images and generate structured descriptions that help classify and index visual content, making it easier to locate relevant images and integrate them into search systems.

In this exercise, you'll explore how to create and use an image analyzer in the Microsoft Azure Portal. You'll run the analyzer on sample images and review the generated descriptions that can be used as metadata for indexing and search. By the end of this lab, you'll understand how AI-generated image descriptions can help make visual content more searchable and useful in data-driven applications.

This exercise will take approximately **30** minutes.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors. Video generation can take 1 to 5 minutes to complete depending on your settings.

## Prerequisites

To complete this exercise, you need:

- An [Azure subscription](https://azure.microsoft.com/free/) with permissions to create AI resources.
- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine.
- [Python 3.13](https://www.python.org/downloads/) or later installed on your local machine.
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed on your local machine.

## Create a Foundry resource

Let's start by creating a Foundry resource.

1. In a web browser, open the [Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials.

1. Ensure the **New Foundry** toggle is set to *On*.

1. You may be prompted to create a new project before continuing to the New Foundry experience. Select **Create a new project**.

    <img src="../media/foundry-new-project.png" alt="Screenshot of the Create project pane." width="600">

    If you're not prompted, select the projects drop down menu on the upper left, and then select **Create new project**.

1. Enter a name for your Foundry project in the textbox and select **Create**.

    Wait a few moments for the project to be created. The new Foundry portal home page should appear with your project selected.

Creating a Foundry project also creates a Foundry resource group in Azure that is linked to your project. This resource group will connect to the Azure Content Understanding service and any other AI services you choose to deploy for use in your Foundry project.

## Deploy required models for Content Understanding

Now that you have a Foundry project, you can deploy the AI models needed for content understanding.

1. Navigate to the [Content Understanding settings page](https://contentunderstanding.ai.azure.com/settings) at `https://contentunderstanding.ai.azure.com/settings`.

1. Select the **Add resource** button.

1. Select your subscription and the Foundry resources that match your Foundry project name. 

1. Check the box for **Enable auto-deployment for required models if no default deployment available**. 

1. Select **Next**, then select **Save** to deploy the required models.

    The deployment process can take several minutes. Once the models are deployed, the resource will appear under **Connected Azure AI Foundry Resources**. Note the name of the resource.

## Try a pre-built image analyzer in the Content Understanding Studio

1. Select **Home** from the upper-right of the page to navigate to the homepage.

    The **Get started with Content Understanding** page will appear with options to analyze different types of content.

1. Select **Explore all pre-built analyzers**.

    A list of pre-built analyzers will appear. These analyzers are designed to extract structured information from different types of content, such as documents, images, audio, and video.

1. Select **Modality** from the filter options, and then select **Image**.

1. Select **Try it** on the **Image search** analyzer.

    Observe the sample image analysis results. The analyzer generates a summary of the image content, identifying objects and concepts in the image. The JSON result is also available. You can also try uploading your own images to see the generated descriptions.

## Create an image analyzer application

Now that you've explored the playground, let's build a Python application that programmatically analyzes images using the Content Understanding analyzers.

### Prepare the application configuration

1. Open **Visual Studio Code** on your local computer. If you don't have it installed, download it from [https://code.visualstudio.com](https://code.visualstudio.com).

1. Open a terminal in VS Code (**Terminal > New Terminal**) and clone the GitHub repo containing the code files for this exercise:

    ```
    git clone https://github.com/microsoftlearning/mslearn-ai-vision mslearn-ai-vision
    ```

1. After the repo has been cloned, open the folder in VS Code (**File > Open Folder**), and navigate to the `mslearn-ai-vision/labfiles/content-understanding/python` folder.

1. In the VS Code Explorer pane, review the files in the folder:

    - `.env` - A configuration file for application settings.
    - `image-app.py` - The Python code file for the image analyzer application.
    - `requirements.txt` - A file listing the package dependencies.

1. Open a terminal in VS Code and navigate to the project folder, then install the required libraries:

    ```
    cd mslearn-ai-vision/labfiles/content-understanding/python
    python -m venv labenv
    ```

1. Activate the virtual environment:

    ```
    labenv\Scripts\activate
    ```

1. Install the required packages:

    ```
    pip install -r requirements.txt
    ```

1. In VS Code, open the `.env` file and replace **{YOUR-RESOURCE-NAME}** with the name of your Foundry resource used for the content understanding (for example, `foundry-project-resource`).

1. Save the `.env` file.

### Write code to analyze images and generate descriptions

> **Tip**: As you add code, be sure to maintain the correct indentation.

1. In VS Code, open the `image-app.py` file.

1. Find the comment **Add references** and add the following code for the necessary imports:

    ```python
   # Add references
   import requests
   import time
   from azure.identity import DefaultAzureCredential
    ```

1. Find the comment **Get an access token for the Azure Cognitive Services resource** and add the following code:

    ```python
   # Get an access token for the Azure Cognitive Services resource
   credential = DefaultAzureCredential()
   token = credential.get_token("https://cognitiveservices.azure.com/.default")
   analyzer_url = f"{endpoint}/contentunderstanding/analyzers/prebuilt-imageSearch:analyze?api-version=2025-11-01"
   headers = {
       "Authorization": f"Bearer {token.token}",
       "Content-Type": "application/json"
   }
    ```

1. Find the comment **Send the image to the analyzer and get the initial response** and add the following code:

    ```python
   # Send the image to the analyzer and get the initial response
   payload = {
       "inputs": [
           {"url": image_url}
       ]
   }
   response = requests.post(analyzer_url, headers=headers, json=payload)
   print(f"Status Code: {response.status_code}")
   result = response.json()
    ```

1. Find the comment **Check the status of the analysis and poll if it's still running** and add the following code:

    ```python
   # Check the status of the analysis and poll if it's still running
   if result.get("status") in ("Running", "NotStarted"):
       request_id = result.get("id")
       results_url = f"{endpoint}/contentunderstanding/analyzerResults/{request_id}?api-version=2025-11-01"
       
       # Poll until complete
       while result.get("status") not in ("Succeeded", "Failed"):
           time.sleep(2)
           poll_response = requests.get(results_url, headers=headers)
           result = poll_response.json()
           print(f"Status: {result.get('status')}")
    ```

1. Save the file (**Ctrl+S**).

### Sign into Azure and run the app

1. In the VS Code terminal, sign into Azure:

    ```
    az login
    ```

    **<font color="red">You must sign into Azure to authenticate with your Azure OpenAI resource.</font>**

    > **Note**: In most scenarios, just using *az login* will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the *--tenant* parameter.

1. When prompted, follow the instructions to open the sign-in page in a new tab and enter the authentication code provided and your Azure credentials.

1. After you have signed in, run the application:

    ```
    python image-app.py
    ```

1. Observe the output, which should be similar to the following:

    ```output
    ==================================================
    Image Analysis Summaries:
    ==================================================

    Image 1 Summary:
    The image shows a single apple placed on a light-colored fabric surface. The apple has a mix of red and greenish-yellow hues with some natural blemishes and a slightly irregular shape. The background is plain and out of focus, highlighting the apple as the main subject.

    Image 2 Summary:
    The image shows a single ripe banana placed on a white textured surface. The banana is mostly yellow with some brown spots and a greenish stem, indicating it is fresh and ready to eat.

    Image 3 Summary:
    The image is a 3D pie chart showing the distribution of hours in four categories. The largest segment is '60+ hours' at 37.8%, followed closely by '50-60 hours' at 36.6%. The '40-50 hours' category accounts for 18.9%, and the smallest segment is '1-39 hours' at 6.7%.
    ```

    Image analysis typically takes a few seconds. Notice that the descriptions include details about the objects in the images, including text, numbers, and other visual features. These detailed descriptions can help make the images more searchable and easier to organize in a content management system or search index.

## Summary

In this exercise, you created a Foundry resource and deployed the necessary models for content understanding. You explored the pre-built image analyzer in the Content Understanding Studio, and then built a Python application that sends images to the analyzer and retrieves generated descriptions. Great work!

## Clean up

When you finish exploring content understanding in Foundry, you should delete the resources you've created to avoid unnecessary Azure costs.

- Navigate to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`.
- In the Azure portal, on the **Home** page, select **Resource groups**.
- Select the resource group that you created for this exercise.
- At the top of the **Overview** page for your resource group, select **Delete resource group**.
- Enter the resource group name to confirm you want to delete it, and select **Delete**.