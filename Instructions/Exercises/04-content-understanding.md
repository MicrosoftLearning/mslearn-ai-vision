---
lab:
    title: 'Analyze images with Azure Content Understanding'
    description: 'Learn how to use Azure Content Understanding to analyze images and generate descriptive metadata.'
    level: 300
    duration: 30
    islab: true
    status: 'released'
---

# Analyze images with Azure Content Understanding

Azure Content Understanding in Foundry Tools is a capability available in Microsoft AI Foundry that uses generative AI to analyze and interpret different types of unstructured content, including documents, images, audio, and video. By applying AI models to this content, the service can generate structured outputs that follow a user-defined schema. These structured outputs make it easier to integrate extracted information into automation, analytics, and search workflows.

One common challenge organizations face is managing large collections of visual content. Images often contain valuable information, but that information can be difficult to search or organize without descriptive metadata. Azure Content Understanding can analyze images and generate structured descriptions that help classify and index visual content, making it easier to locate relevant images and integrate them into search systems.

In this exercise, you'll explore how to create and use an image analyzer in the Content Understanding Studio web interface. You'll run the analyzer on sample images and review the generated descriptions that can be used as metadata for indexing and search. By the end of this lab, you'll understand how AI-generated image descriptions can help make visual content more searchable and useful in data-driven applications.

This exercise will take approximately **30** minutes.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors. Video generation can take 1 to 5 minutes to complete depending on your settings.

## Prerequisites

To complete this exercise, you need:

- An [Azure subscription](https://azure.microsoft.com/free/) with permissions to create AI resources.
- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine.
- [Python 3.13](https://www.python.org/downloads/) or later installed on your local machine.
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed on your local machine.

## Create a Microsoft Foundry project

Microsoft Foundry uses projects to organize models, resources, data, and other assets used to develop an AI solution.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` to start building; signing in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in.

1. If it is not already enabled, in the tool bar the top of the page, enable the **New Foundry** option. Then, if prompted, create a new project with a unique name; expanding the **Advanced options** area to specify the following settings for your project:
    - **Foundry resource**: *Use the default name for your resource (usually {project_name}-resource)*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: Select any available region

1. Wait for your project to be created. Then on the home page for your project, view the project details.

    Creating a Foundry project also creates a Foundry resource group in Azure that is linked to your project. This resource group will connect to the Azure Content Understanding service and any other AI services you choose to deploy for use in your Foundry project.

## Create an Azure storage account

You'll need an Azure storage account for the content assets you're going to analyze using Azure Content Understanding.

1. In a new browser tab, open the [Azure portal](https://portal.azure.com) at `https://portal.azure.com` and browse to the resource group where you created your Foundry project resource.

    The resource group should contain your Foundry resource and the project you created.

1. Create a new **Storage account** resource in the resource group, with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *The resource group containing your Foundry resource*
    - **Storage account name**: *A unique name for your storage account*
    - **Region**: *The same region as your Foundry resource*
    - **Preferred storage type**: Azure Blob Storage or Azure Data Lake Storage Gen 2
    - **Performance**: Standard
    - **Redundancy**: Locally-redundant storage (LRS)
1. Wait for your storage account to be created.

## Create an image analyzer in Azure Content Understanding

Now that you have a Foundry project, you can deploy the AI models needed for content understanding.

1. In a new browser tab, navigate to [Content Understanding Studio](https://contentunderstanding.ai.azure.com/home) at `https://contentunderstanding.ai.azure.com/home` and sign in using your Azure credentials if prompted.
1. At the top right, select the **Settings** icon to view your account settings for Azure Content Understanding.

1. On the **Setup Azure resource** page, select the **Add resource** button.

1. Select your subscription and the Foundry resources that match your Foundry project name.

1. Check the box for **Enable auto-deployment for required models if no default deployment available**.

1. Select **Next**, then select **Save** to deploy the required models.

    The deployment process can take several minutes. Once the models are deployed, the resource will appear under **Connected Azure AI Foundry Resources**. Note the name of the resource.

1. On the menu bar, select **Build**. Then use the **Create** button to create a new Content Understanding project with the following settings.
    - **Project name**: *A unique name for your image analysis project*
    - **Description**: Image analysis project
    - **Type of project**: Extract content and field with custom schema
    - **Advanced settings**: Ensure your Foundry resource and storage account are selected, a new container will be created, and a chat completion model such as gpt-4.1 is selected.
1. When the project has been created, in a new browser tab, download the [lion.jpg](https://microsoftlearning.github.io/mslearn-ai-vision/Labfiles/content-understanding/lion.jpg) image from `https://microsoftlearning.github.io/mslearn-ai-vision/Labfiles/content-understanding/lion.jpg` and save it in a local folder.

    Then return to the Content Understanding project, and upload the **lion.jpg** file to the project.

1.When prompted to choose a template, select **Image Analysis** and ensure the schema is set to **Start from Scratch**. Then save the project.

1. After the image has been uploaded, in the **Schema** pane, use the **Add new field** to add the following fields to the schema:

    | Field Name | Field Descriptopn | Value type | Method |
    |--|--|--|--|
    | `Description` | `Image description` | String | Generate |
    | `Tags` | `Image tags` | List of Strings | Generate |

1. Save the changes to the schema.
1. Select **Run analysis** to run the analyzer on the image, and review the fields that are generated; which should include an accurate description and a collection of relevant tags for the image.
1. When you're satisfied that the analyzer has returned accurate values for the fields, use the **Build analyzer** button to publish an analyzer with a unique name and suitable description.

    >**Tip**: You'll need the name later to identify your analyzer in application code.

1. When your analyzer has been built, jump to the analyzer list and verify it's listed there.
1. Select your analyzer in the list to open it, and then view the **Code Example** tab to see the code necessary to use your analyzer.
1. Review the Python code example, noting in the **main** function the **endpoint** for your Content Understanding resource; which should look similar to this:

    ```
   https://{your_foundry_resource}.services.ai.azure.com/
    ```

1. Under the code example, note that your **resource key** is available. You *can* use this in a client application to authenticate a connection to the endpoint; but in this exercise we're going to use Microsoft Entra ID authentication.

## Create an image analyzer application

Now that you've created an analyzer, let's build a Python application that uses it to analyzes images.

### Get application files from GitHub

The initial application files you'll need to develop the image analysis application are provided in a GitHub repo.

1. Open Visual Studio Code.
1. Open the command palette (*Ctrl+Shift+P*) and use the `Git:clone` command to clone the `https://github.com/microsoftlearning/mslearn-ai-vision` repo to a local folder (it doesn't matter which one). Then open it.

    You may be prompted to confirm you trust the authors.

1. In Visual Studio Code, view the **Extensions** pane; and if it is not already installed, install the **Python** extension.
1. In the **Command Palette**, use the command `python:select interpreter`. Then select an existing environment if you have one, or create a new **Venv** environment based on your Python 3.1x installation.

    > **Tip**: If you are prompted to install dependencies, you can install the ones in the *requirements.txt* file in the */labfiles/content-understanding/python* folder; but it's OK if you don't - we'll install them later!

### Prepare the application configuration

1. After the repo has been cloned, open the folder in VS Code (**File > Open Folder**), and navigate to the `/labfiles/content-understanding/python` folder.

1. In the VS Code Explorer pane, review the files in the folder:

    - `.env` - A configuration file for application settings.
    - `analyze-image.py` - The Python code file for the image analyzer application.
    - `requirements.txt` - A file listing the package dependencies.
    - `images` - A folder containing images for analysis.

1. In the **Explorer** pane, in the **python** folder, select the **.env** file to open it. Then update it with the  **endpoint** value for your resource endpoint (copied from the code example in Content Understanding Studio) and the name of your analyzer.

    > **Important**:Be sure to add the `https://{YOUR-RESOURCE-NAME}.services.ai.azure.com` Foundry resource endpoint, <u>not</u> the project endpoint or Azure OpenAI endpoint!

    Save the modified configuration file.

1. In the **Explorer** pane, right-click the **python** folder containing the application files, and select **Open in integrated terminal** (or open a terminal in the **Terminal** menu and navigate to the */labfiles/content-understanding/python* folder.)

    > **Note**: Opening the terminal in Visual Studio Code will automatically activate the Python environment. You may need to enable running scripts on your system.

1. Ensure that the terminal is open in the **/labfiles/content-understanding/python*** folder with the prefix **(.venv)** to indicate that the Python environment you created is active.
1. Install the required Python packages by running the following command:

    ```
    pip install -r requirements.txt
    ```

### Write code to analyze images and generate descriptions

> **Tip**: As you add code, be sure to maintain the correct indentation.

1. In VS Code, open the `analyze-image.py` file.

1. Find the comment **Add references** and add the following code for the necessary imports:

    ```python
   # Add references
   from azure.ai.contentunderstanding import ContentUnderstandingClient
   from azure.ai.contentunderstanding.models import AnalysisInput, AnalysisResult
   from azure.core.exceptions import AzureError
   from azure.identity import DefaultAzureCredential
    ```

1. In the **main** function, note that code to get the configuration values from your environment file has been provided.
1. Find the comment **Set up Content Understanding client** and add the following code:

    ```python
   # Set up Content Understanding client
   credential = DefaultAzureCredential()
   client = ContentUnderstandingClient(
        endpoint=endpoint,
        credential=credential,
        api_version=api_version)
    ```

1. Note that code for the user to input a file number or quit the program has been provided.
1. Find the comment **Analyze the file** and add the following code:

    ```python
   # Analyze the file
   try:
        poller = client.begin_analyze(
            analyzer_id=analyzer_id,
            inputs=[AnalysisInput(data=file_bytes)],
        )
        result: AnalysisResult = poller.result()
   except AzureError as err:
        print(f"[Azure Error]: {err.message}")
        sys.exit(1)
   except Exception as ex:
        print(f"[Unexpected Error]: {ex}")
        sys.exit(1)

   for field in result.contents[0].fields:
        if field == "Description":
            print(f"{field}:\n{result.contents[0].fields[field].value_string}\n")
        elif field == "Tags":
            print(f"{field}:")
            for tag in result.contents[0].fields[field].value_array:
                print("  -", tag.value_string)
    ```

    This code submits the selected file data to your analyuzer, polls for the results, and then displays the *Description* and *Tags* values that are returned.

1. Save the file (**Ctrl+S**).

### Test the app

1. In the terminal pane, use the following command to sign into Azure.

    ```powershell
    az login
    ```

    > **Note**: In most scenarios, just using *az login* will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the *--tenant* parameter. See [Sign into Azure interactively using the Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) for details.

1. When prompted, follow the instructions to sign into Azure. Then complete the sign in process in the command line, viewing (and confirming if necessary) the details of the subscription containing your Foundry resource.
1. After you have signed in, enter the following command to run the application:

    ```
    python analyze-image.py
    ```

1. When prompted, enter a number that corresponds to one of these images:

    |![A giraffe.](../../Labfiles/content-understanding/python/images/image1.jpg) | ![An elephant.](../../Labfiles/content-understanding/python/images/image2.jpg) | ![A lion.](../../Labfiles/content-understanding/python/images/image3.jpg)
    |--|--|--|
    | 1 | 2 | 3 |

1. Observe the output, which should include a description of the selected image and a collection of appropriate tags.
1. When you're finished, enter any value other than 1, 2, or 3 to exit.

## Summary

In this exercise, you created a Foundry resource and deployed the necessary models for content understanding. You explored the pre-built image analyzer in the Content Understanding Studio, and then built a Python application that sends images to the analyzer and retrieves generated descriptions. Great work!

## Clean up

When you finish exploring content understanding in Foundry, you should delete the resources you've created to avoid unnecessary Azure costs.

- Navigate to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`.
- In the Azure portal, on the **Home** page, select **Resource groups**.
- Select the resource group that you created for this exercise.
- At the top of the **Overview** page for your resource group, select **Delete resource group**.
- Enter the resource group name to confirm you want to delete it, and select **Delete**.
