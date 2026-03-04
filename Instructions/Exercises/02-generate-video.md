---
lab:
    title: 'Generate video with Sora in Microsoft Foundry'
    description: 'Learn how to generate AI-powered video content using the Sora model in Microsoft Foundry.'
    level: 300
    duration: 45
---

# Generate video with Sora in Microsoft Foundry

Sora is an AI model from OpenAI that creates realistic and imaginative video scenes from text instructions. The model can generate a wide range of video content, including realistic scenes, animations, and special effects. It supports several video resolutions and durations, and can also use reference images and remix existing videos.

In this exercise, you'll explore how to deploy the Sora model and generate video content using the Microsoft Foundry portal. You'll also build an application that generates videos from images, polls for completion status, and remixes existing videos.

This exercise will take approximately **45** minutes.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors. Video generation can take 1 to 5 minutes to complete depending on your settings.

## Understand responsible AI considerations

Azure OpenAI's video generation models include built-in Responsible AI (RAI) protections to help ensure safe and compliant use.

The Sora 2 model enforces several content restrictions:

- Only content suitable for audiences under 18
- Copyrighted characters and copyrighted music are rejected
- Real people—including public figures—cannot be generated
- Input images with faces of humans are currently rejected

Azure provides input and output moderation across all image generation models, along with Azure-specific safeguards such as content filtering and abuse monitoring. These systems help detect and prevent the generation or misuse of harmful, unsafe, or policy-violating content.

## Prerequisites

To complete this exercise, you need:

- An [Azure subscription](https://azure.microsoft.com/free/) with permissions to create AI resources.
- Access to the Sora model in Azure OpenAI (available in supported regions).
- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine.
- [Python 3.13](https://www.python.org/downloads/) or later installed on your local machine.
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed on your local machine.

## Deploy the Sora model in a Foundry project

Let's start by creating a project and deploying the Sora video generation model.

1. In a web browser, open the [Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials.

1. Ensure the **New Foundry** toggle is set to *On*.

1. You may be prompted to create a new project before continuing to the New Foundry experience. Select **Create a new project**.

    <img src="../Media/ai-foundry-new-project.png" alt="Screenshot of the Create project pane." width="600">

    If you're not prompted, select the projects drop down menu on the upper left, and then select **Create new project**.

1. Enter a name for your Foundry project in the textbox and select **Create**.

    Wait a few moments for the project to be created. The new Foundry portal home page should appear with your project selected.

1. On the Foundry portal home page, select **Build** from the toolbar menu.

1. On the left-hand menu, select **Models**.

1. Select **Deploy a base model** and then choose the **Sora-2** video generation model from the list.

1. Select **Deploy** and choose the default settings.

    The deployment process may take a few minutes. Once the deployment is complete, the model playground will open.

## Generate a video from a text prompt

Now let's use the playground to generate your first AI-powered video.

1. In the playground, enter the following prompt into the text box:

    ```
    A director giving a presentation in a modern conference room.
    ```

1. Set the video duration to 4 seconds.

1. Select **Generate** to start the video generation process.

    > **Note**: Video generation typically takes 1 to 5 minutes depending on your settings. The content generation APIs include content moderation filters. If Azure OpenAI recognizes your prompt as harmful content, it won't return a generated video.

1. When the AI-generated video is ready, it will appear on the page. Review the generated video.

1. In the video details pane text box, edit the video by submitting the following instructions:

    ```
    Use an inviting instrumental as the background music.
    ```

## Create a video generation application

Now that you've explored the playground, let's build a Python application that programmatically generates videos using the Sora 2 API.

### Prepare the application configuration

1. Open **Visual Studio Code** on your local computer. If you don't have it installed, download it from [https://code.visualstudio.com](https://code.visualstudio.com).

1. Open a terminal in VS Code (**Terminal > New Terminal**) and clone the GitHub repo containing the code files for this exercise:

    ```
    git clone https://github.com/microsoftlearning/mslearn-ai-vision mslearn-ai-vision
    ```

1. After the repo has been cloned, open the folder in VS Code (**File > Open Folder**), and navigate to the `mslearn-ai-vision/labfiles/video-generation/python` folder.

1. In the VS Code Explorer pane, review the files in the folder:

    - `.env` - A configuration file for application settings.
    - `video-app.py` - The Python code file for the video application.
    - `requirements.txt` - A file listing the package dependencies.

1. Open a terminal in VS Code and navigate to the project folder, then install the required libraries:

    ```
    cd mslearn-ai-vision/labfiles/video-generation/python
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

1. In VS Code, open the `.env` file and replace the placeholders:
    - Replace **YOUR-RESOURCE-NAME** with the name of your Foundry resource where you deployed the Sora model (for example, `foundry-project-resource`).
    - Replace the **MODEL_DEPLOYMENT** value with the name of your model deployment (for example, `sora-2`).

1. Save the `.env` file.

### Write code to generate videos from an image reference

> **Tip**: As you add code, be sure to maintain the correct indentation.

1. In VS Code, open the `video-app.py` file.

1. Find the comment **Add references** and add the following code for the necessary imports:

    ```python
    # Add references
    import time
    from dotenv import load_dotenv
    from openai import OpenAI
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    ```

1. Find the comment **Get the token provider for Azure OpenAI authentication** and add the following code:

    ```python
    
    # Get the token provider for Azure OpenAI authentication
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )

    #Initialize the OpenAI client with the endpoint and token provider
    client = OpenAI(
        base_url=endpoint,
        api_key=token_provider,
    )
    ```

1. In the main function, find the comment **Generate a video from a text prompt** and add the following code:

    ```python
    # Generate a video from a text prompt
    video = client.videos.create(
        model=model_deployment,
        prompt="A peaceful mountain lake at sunrise with mist rising from the water",
        size="1280x720",
        seconds='4',
    )
    video = poll_video_status(video.id)
    ```

1. In the main function, find the comment **Generate a video from a reference image** and add the following code:

    ```python
    # Generate a video from a reference image
    video = generate_video_from_image(
        image_path="reference.png",
        prompt="The scene comes to life with gentle movement and ambient lighting",
        size="720x1280",
        seconds='4'
    )
    if video.status == "completed":
        download_video(video.id, "image_based_video.mp4")
    ```

1. Find the comment **Poll video status until completion** and add the following code to complete the `poll_video_status` function:

    ```python
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
    ```

1. Find the comment **Remix an existing video** and add the following code to complete the `remix_video` function:

    ```python
    # Remix an existing video
    video = client.videos.remix(
        video_id=video_id,
        prompt=prompt,
    )
    
    print(f"Remix started. New video ID: {video.id}")
    print(f"Initial status: {video.status}")
    
    # Poll for completion
    video = poll_video_status(video.id)
    return video
    ```

1. Find the comment **Download the completed video** and add the following code to complete the `download_video` function:

    ```python
    # Download the completed video
    print(f"Downloading video {video_id}...")
    content = client.videos.download_content(video_id, variant="video")
    content.write_to_file(output_filename)
    print(f"Saved video to {output_filename}")
    ``` 

1. Find the comment **Create the video with an image reference** and add the following code to complete the `generate_video_from_image` function:

    ```python
    # Create the video with an image reference
    video = client.videos.create(
        model=model_deployment,
        prompt=prompt,
        size=size,
        seconds=seconds,
        input_reference=open(image_path, "rb"),
    )
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
    python video-app.py
    ```

1. Observe the output as the application:
    - Creates a video from a text prompt
    - Polls for the video status until completion
    - Downloads the completed video
    - Remixes the video with a new style
    - Downloads the remixed video

    > **Note**: Video generation typically takes 1-5 minutes per video. Be patient while waiting for the status to change to "completed".

1. When the application finishes, check your project folder for `original_video.mp4`, `remixed_video.mp4`, and `image_based_video.mp4`.

## Summary

In this exercise, you used the Microsoft Foundry portal to explore video generation with the Sora model, and built a Python application that programmatically generates videos. You learned how to:

- Generate videos from text prompts and reference images
- Poll for video generation status until completion
- Download completed videos
- Remix existing videos with new prompts

The Sora 2 API provides powerful video generation capabilities through a simple asynchronous workflow: create a job, poll for status, and download the result.

## Clean up

When you finish exploring video generation in Foundry, you should delete the resources you've created to avoid unnecessary Azure costs.

- Navigate to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`.
- In the Azure portal, on the **Home** page, select **Resource groups**.
- Select the resource group that you created for this exercise.
- At the top of the **Overview** page for your resource group, select **Delete resource group**.
- Enter the resource group name to confirm you want to delete it, and select **Delete**.