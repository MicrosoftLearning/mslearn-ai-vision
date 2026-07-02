---
lab:
    title: 'Develop a vision-enabled chat app'
    description: 'Use Azure AI Foundry to build a generative AI app that supports image input.'
    level: 300
    duration: 30
    islab: true
    status: 'released'
---

# Develop a vision-enabled chat app

In this exercise, you use a generative AI model to generate responses to prompts that include images. You'll develop an app that provides AI assistance with fresh produce in a grocery store by using Microsoft Foundry and the OpenAI SDK.

While this exercise is based on the OpenAI Python SDK, you can develop AI chat applications using multiple language-specific SDKs; including:

* [OpenAI Projects for Microsoft .NET](https://www.nuget.org/packages/OpenAI)
* [OpenAI Projects for JavaScript](https://www.npmjs.com/package/openai)

This exercise takes approximately **30** minutes.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors.

## Prerequisites

Before starting this exercise, ensure you have:

* An active [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account)
* [Visual Studio Code](https://code.visualstudio.com/) installed
* [Python version **3.13.xx**](https://www.python.org/downloads/release/python-31312/) installed\*
* [Git](https://git-scm.com/install/) installed and configured
* [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli?view=azure-cli-latest) installed

> \* Python 3.14 is available, but some dependencies are not yet compiled for that release. The lab has been successfully tested with Python 3.13.12.

## Create a Microsoft Foundry project

Microsoft Foundry uses projects to organize models, resources, data, and other assets used to develop an AI solution.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` to start building; signing in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in.

1. If it is not already enabled, in the tool bar the top of the page, enable the **New Foundry** option. Then, if prompted, create a new project with a unique name; expanding the **Advanced options** area to specify the following settings for your project:
    * **Foundry resource**: *Use the default name for your resource (usually {project_name}-resource)*
    * **Subscription**: *Your Azure subscription*
    * **Resource group**: *Create or select a resource group*
    * **Region**: Select any available region

1. Wait for your project to be created. Then, on the home page for your project, note that the API key, project endpoint, and Azure OpenAI endpoint are displayed here.

    > **TIP**: You're going to need the Azure OpenAI endpoint later!

## Deploy a model

You'll need a model that can process image-based input.

1. Now you're ready to explore models. On the **Discover** page, select the **Models** tab to view the Microsoft Foundry model catalog.
1. Search for and deploy the `gpt-4.1` model using the default settings. Deployment may take a minute or so.

    > **Tip**: Model deployments are subject to regional quotas. If you don't have enough quota to deploy the model in your project's region, you can use a different model - such as gpt-4.1-mini, or gpt-4o. Alternatively, you can create a new project in a different region.

1. When the model has been deployed, view the model playground page that is opened, in which you can chat with the model.

    > **TIP**: Note the model deployment name (which by default should be *gpt-4.1*) - you'll need this later!

## Test the model in the playground

Now you can test your model deployment with an image-based prompt in the chat playground.

1. In a new browser tab, download [mango.jpeg](https://microsoftlearning.github.io/mslearn-ai-vision/Labfiles/gen-ai-vision/mango.jpeg) from `https://microsoftlearning.github.io/mslearn-ai-vision/Labfiles/gen-ai-vision/mango.jpeg` and save it to a folder on your local file system.

1. Navigate back to the chat playground page for your model deployment in the Foundry portal.

1. In the main chat session panel, under the chat input box, use the attach button (**&#128206;**) to upload the *mango.jpeg* image file, and then add the text `What desserts could I make with this fruit?` and submit the prompt.

    ![Screenshot of the chat playground page.](../media/chat-playground-image-new.png)

1. Review the response, which should hopefully provide relevant guidance for desserts you can make using a mango.

## Create a client application

Now that you've deployed the model, you can use the deployment in a client application.

### Get application files from GitHub

The initial application files you'll need to develop the translation application are provided in a GitHub repo.

1. Open Visual Studio Code.
1. Open the command palette (*Ctrl+Shift+P*) and use the `Git:clone` command to clone the `https://github.com/microsoftlearning/mslearn-ai-vision` repo to a local folder (it doesn't matter which one). Then open it.

    You may be prompted to confirm you trust the authors.

1. In Visual Studio Code, view the **Extensions** pane; and if it is not already installed, install the **Python** extension.
1. In the **Command Palette**, use the command `python:select interpreter`. Then select an existing environment if you have one, or create a new **Venv** environment based on your Python 3.13.x installation.

    > **Tip**: If you are prompted to install dependencies, you can install the ones in the *requirements.txt* file in the */labfiles/gen-ai-vision/python* folder; but it's OK if you don't - we'll install them later!

### Prepare the application configuration

1. After the repo has been cloned, open the folder in VS Code (**File > Open Folder**), and navigate to the `/labfiles/gen-ai-vision/python` folder.

1. In the VS Code Explorer pane, review the files in the folder:

    * `.env` - A configuration file for application settings.
    * `image-chat-app.py` - The Python code file for the image application.
    * `requirements.txt` - A file listing the package dependencies.
    * `mystery-fruit.jpeg` - An image of a fruit.

1. In the **Explorer** pane, in the **python** folder, select the **.env** file to open it. Then update the configuration values to include the **Azure OpenAI endpoint** for your Foundry resource, and the model deployment name for the generative AI model you deployed.

    > **Important**: Be sure to add the `https://{foundry-resource-name}.openai.azure.com/openai/v1/` Azure OpenAI endpoint, <u>not</u> the project endpoint!

    Save the modified configuration file.

1. In the **Explorer** pane, right-click the **python** folder containing the application files, and select **Open in integrated terminal** (or open a terminal in the **Terminal** menu and navigate to the */labfiles/gen-ai-vision/python* folder.)

    > **Note**: Opening the terminal in Visual Studio Code will automatically activate the Python environment. You may need to enable running scripts on your system.

1. Ensure that the terminal is open in the **/labfiles/gen-ai-vision/python** folder with the prefix **(.venv)** to indicate that the Python environment you created is active.
1. Install the required Python packages by running the following command:

    ```
    pip install -r requirements.txt
    ```

### Write code to get an OpenAI chat client for your model

> **Tip**: As you add code, be sure to maintain the correct indentation.

1. In VS Code, open the `image-chat-app.py` file.

1. In the code file, note the existing statements that have been added at the top of the file to import the necessary SDK namespaces. Then, Find the comment **Add references**, add the following code to reference the namespaces in the libraries you installed previously:

    ```python
   # Add references
   from openai import OpenAI
   from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    ```

1. In the **main** function, under the comment **Get configuration settings**, note that the code loads the project connection string and model deployment name values you defined in the configuration file.

1. Find the comment **Create an OpenAI client**, and add the following code to connect to your Azure AI Foundry project:

    > **Tip**: Be careful to maintain the correct indentation level for your code.

    ```python
   # Create an OpenAI client
   credential = DefaultAzureCredential()
   token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
   client = OpenAI(
       base_url=openai_endpoint,
       api_key=token_provider()
   )
    ```

### Write code to submit a URL-based image prompt

1. Note that the code includes a loop to allow a user to input a prompt until they enter "quit". Then in the loop section, find the comment **Get a response to image input**, add the following code to submit a prompt that includes the following image:

    ![A photo of an orange.](../media/orange.jpeg)

    ```python
   # Get a response to image input
   image_url = "https://microsoftlearning.github.io/mslearn-ai-vision/Labfiles/gen-ai-vision/orange.jpeg"
   response = client.responses.create(
        model=model_deployment,
        input=[
            {"role": "developer", "content": system_message},
            { "role": "user", "content": [  
                { "type": "input_text", "text": prompt},
                { "type": "input_image", "image_url": image_url}
            ]} 
        ]
   )
   print(response.output_text)
    ```

1. Save your changes to the code file.

## Sign into Azure and run the app

1. In the terminal pane, use the following command to sign into Azure.

    ```powershell
    az login
    ```

    > **Note**: In most scenarios, just using *az login* will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the *--tenant* parameter. See [Sign into Azure interactively using the Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) for details.

1. When prompted, follow the instructions to sign into Azure. Then complete the sign in process in the command line, viewing (and confirming if necessary) the details of the subscription containing your Foundry resource.
1. After you have signed in, enter the following command to run the application:

    ```
   python image-chat-app.py
    ```

1. When prompted, enter the following prompt:

    ```
   Suggest some recipes that include this fruit
    ```

1. Review the response. Then enter `quit` to exit the program.

### Modify the code to upload a local image file

1. In the code editor for your app code, in the loop section, find the code you added previously under the comment **Get a response to image input**. Then modify the code as follows, to upload this local image file:

    ![A photo of a dragon fruit.](../media/mystery-fruit.jpeg)

    ```python
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
            { "role": "user", "content": [  
                { "type": "input_text", "text": prompt},
                { "type": "input_image", "image_url": data_url}
            ]} 
        ]
   )
    print(response.output_text)
    ```

1. Use the **CTRL+S** command to save your changes to the code file.

1. In the terminal, enter the following command to run the app:

    ```
   python image-chat-app.py
    ```

1. When prompted, enter the following prompt:

    ```
   What is this fruit? What recipes could I use it in?
    ```

1. Review the response. Then enter `quit` to exit the program.

    > **Note**: In this simple app, we haven't implemented logic to retain conversation history; so the model will treat each prompt as a new request with no context of the previous prompt.

## Clean up

If you've finished exploring Azure AI Foundry portal, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Open the [Azure portal](https://portal.azure.com) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
