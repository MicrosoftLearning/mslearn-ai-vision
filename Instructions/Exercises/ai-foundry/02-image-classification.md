---
lab:
    title: 'Classify images with an Azure AI Vision custom model'
    module: 'Module 2 - Develop computer vision solutions with Azure AI Vision'
---

# Classify images with an Azure AI Vision custom model

Azure AI Vision enables you to train custom models to classify and detect objects with labels you specify. In this lab, we'll build a custom image classification model to classify images of fruit.

## Provision a Computer Vision resource

If you don't already have one in your subscription, you'll need to provision a **Computer Vision** resource.

1. Open the Azure portal at `https://portal.azure.com`, and sign in using the Microsoft account associated with your Azure subscription.
1. Select **Create a resource**.
1. In the search bar, search for *Computer Vision*, select **Computer Vision**, and create the resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Choose or create a resource group (if you are using a restricted subscription, you may not have permission to create a new resource group - use the one provided)*
    - **Region**: *Choose from East US, West US, France Central, Korea Central, North Europe, Southeast Asia, West Europe, or East Asia\**
    - **Name**: *Enter a unique name*
    - **Pricing tier**: Free F0

    \*Azure AI Vision 4.0 full feature sets are currently only available in these regions.

1. Select the required checkboxes and create the resource.
<!--4. When the resource has been deployed, go to it and view its **Keys and Endpoint** page. You will need the endpoint and one of the keys from this page in a future step. Save them off or leave this browser tab open.-->

We also need a storage account to store the training images.

1. In Azure portal, search for and select **Storage accounts**, and create a new storage account with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource Group**: *Choose the same resource group you created your Custom Vision resource in*
    - **Storage Account Name**: customclassifySUFFIX 
        - *Note: replace the `SUFFIX` token with your initials or another value to ensure the resource name is globally unique.*
    - **Region**: *Choose the same region you used for your Azure AI Service resource*
    - **Primary service**: Azure Blob Storage or Azure Data Lake Storage Gen 2
    - **Primary workload**: Other
    - **Performance**: Standard
    - **Redundancy**: Locally-redundant storage (LRS)

1. When the resource has been deployed, select **Go to resource**.
1. Enable public access on the storage account. In the left pane, navigate to **Configuration** in the **Settings** group, and enable *Allow Blob anonymous access*. Select **Save**
1. In the left pane, in **Data storage**, select **Containers** and create a new container named `fruit`, and set **Anonymous access level** to *Container (anonymous read access for containers and blobs)*.

    > **Note**: If the **Anonymous access level** is disabled, refresh the browser page.
   
## Clone the repository for this course

The image files for training your model have been provided in a GitHub repo. You'll clone the repository and upload the images to your storage account using Cloud Shell from the Azure Portal. 

> **Tip**: If you have already cloned the **mslearn-ai-vision** repo recently, you can skip the clone task. Otherwise, follow these steps to clone the repo to your development environment.

1. In the Azure Portal, use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment. The cloud shell provides a command line interface in a pane at the bottom of the Azure portal.

    > **Note**: If you have previously created a cloud shell that uses a *Bash* environment, switch it to ***PowerShell***.

1. In the cloud shell toolbar, in the **Settings** menu, select **Go to Classic version** (this is required to use the code editor).

    > **Tip**: As you paste commands into the cloudshell, the ouput may take up a large amount of the screen buffer. You can clear the screen by entering the `cls` command to make it easier to focus on each task.

1. In the PowerShell pane, enter the following commands to clone the GitHub repo for this exercise:

    ```
    rm -r mslearn-ai-vision -f
    git clone https://github.com/microsoftlearning/mslearn-ai-vision mslearn-ai-vision
    ```

1. After the repo has been cloned, navigate to the folder containing the exercise files:  

    ```
   cd mslearn-ai-vision/Labfiles/02-image-classification
    ```

1. Run the command `code replace.ps1` and review the code. You'll see that it replaces the name of your storage account for the placeholder in a JSON file (the COCO file) we use in a later step.
1. Replace the placeholder *in the first line only* of the file with the name of your storage account.
1. After you've replaced the placeholder, within the code editor, use the **CTRL+S** command or **Right-click > Save** to save your changes and then use the **CTRL+Q** command or **Right-click > Quit** to close the code editor while keeping the cloud shell command line open.
1. Run the script with the following command:

    ```powershell
    ./replace.ps1
    ```

1. You can review the COCO file to ensure your storage account name is there. Run `code training-images/training_labels.json` and view the first few entries. In the *absolute_url* field, you should see something similar to *"https://myStorage.blob.core.windows.net/fruit/...*. If you don't see the change expected, make sure you updated only the first placeholder in the PowerShell script.
1. Close the code editor.
1. Run the following command, replacing `<your-storage-account>` with the name of your storage account, to upload the content of the **training-images** folder to the `fruit` container you created earlier.

    ```powershell
    az storage blob upload-batch --account-name <your-storage-account> -d fruit -s ./training-images/
    ```

1. Open the `fruit` container and verify that the files were uploaded correctly.

## Create a custom model training project

Next, you will create a new training project for custom image classification in Vision Studio.

1. In the web browser, navigate to `https://portal.vision.cognitive.azure.com/` and sign in with the Microsoft account where you created your Azure AI resource.
1. Select the **Customize models with images** tile (can be found in the **Image analysis** tab if it isn't showing in your default view).
1. Select the Azure AI Services account you created.
1. In your project, select **Add new dataset** on the top. Configure with the following settings:
    - **Dataset name**: training_images
    - **Model type**: Image classification
    - **Select Azure blob storage container**: Select **Select Container**
        - **Subscription**: *Your Azure subscription*
        - **Storage account**: *The storage account you created*
        - **Blob container**: fruit
    - Select the box to "Allow Vision Studio to read and write to your blob storage"
1. Select the **training_images** dataset.

At this point in project creation, you would usually select **Create Azure ML Data Labeling Project** and label your images, which generates a COCO file. You are encouraged to try this if you have time, but for the purposes of this lab we've already labeled the images for you and supplied the resulting COCO file.

1. Select **Add COCO file**
1. In the dropdown, select **Import COCO file from a Blob Container**
1. Since you have already connected your container named `fruit`, Vision Studio searches that for a COCO file. Select **training_labels.json** from the dropdown, and add the COCO file.
1. Navigate to **Custom models** on the left, and select **Train a new model**. Use the following settings:
    - **Name of model**: classifyfruit
    - **Model type**: Image classification
    - **Choose training dataset**: training_images
    - Leave the rest as default, and select **Train model**

Training can take some time - default budget is up to an hour, however for this small dataset it is usually much quicker than that. Select the **Refresh** button every couple minutes until the status of the job is *Succeeded*. Select the model.

Here you can view the performance of the training job. Review the precision and accuracy of the trained model.

## Test your custom model

Your model has been trained and is ready to test.

1. On the top of the page for your custom model, select **Try it out**.
1. Select the **classifyfruit** model from the dropdown specifying the model you want to use, and browse to the **02-image-classification\test-images** folder.
1. Select each image and view the results. Select the **JSON** tab in the results box to examine the full JSON response.

<!-- Option coding example to run-->
## Clean up resources

If you're not using the Azure resources created in this lab for other training modules, you can delete them to avoid incurring further charges.

1. Open the Azure portal at `https://portal.azure.com`, and in the top search bar, search for the resources you created in this lab.

2. On the resource page, select **Delete** and follow the instructions to delete the resource. Alternatively, you can delete the entire resource group to clean up all resources at the same time.
