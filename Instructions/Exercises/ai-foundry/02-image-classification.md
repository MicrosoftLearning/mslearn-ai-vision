---
lab:
    title: 'Classify images with an Azure AI Vision custom model'
    module: 'Module 2 - Develop computer vision solutions with Azure AI Vision'
---

# Classify images with an Azure AI Vision custom model

Azure AI Vision enables you to train custom models to classify and detect objects with labels you specify. In this lab, we'll build a custom image classification model to classify images of fruit.

## Create an Azure AI Foundry project

Let's start by creating an Azure AI Foundry project.

1. In a web browser, open the [Azure AI Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the **Azure AI Foundry** logo at the top left to navigate to the home page, which looks similar to the following image:

    ![Screenshot of Azure AI Foundry portal.](./media/ai-foundry-home.png)

1. In the home page, select **+ Create project**.
1. In the **Create a project** wizard, enter a suitable project name for (for example, `my-ai-project`) then review the Azure resources that will be automatically created to support your project.
1. Select **Customize** and specify the following settings for your hub:
    - **Hub name**: *A unique name - for example `my-ai-hub`*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create a new resource group with a unique name (for example, `my-ai-resources`), or select an existing one*
    - **Location**: *Choose from East US, West Europe, West US 2\**
    - **Connect Azure AI Services or Azure OpenAI**: *Create a new AI Services resource with an appropriate name (for example, `my-ai-services`) or use an existing one*
    - **Connect Azure AI Search**: Skip connecting

    \*Azure AI Vision 4.0 custom model tags are currently only available in these regions.
   
1. Select **Next** and review your configuration. Then select **Create** and wait for the process to complete.
1. When your project is created, close any tips that are displayed and review the project page in Azure AI Foundry portal, which should look similar to the following image:

    ![Screenshot of a Azure AI project details in Azure AI Foundry portal.](./media/ai-foundry-project.png)

We also need a storage account to store the training images.

1. In Azure portal, search for and select **Storage accounts**, and create a new storage account with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource Group**: *Choose the same resource group you created your Azure AI Service resource in*
    - **Storage Account Name**: customclassifySUFFIX 
        - *note: replace the `SUFFIX` token with your initials or another value to ensure the resource name is globally unique.*
    - **Region**: *Choose the same region you used for your Azure AI Service resource*
    - **Primary service**: Azure Blob Storage or Azure Data Lake Storage Gen 2
    - **Primary workload**: Other
    - **Performance**: Standard
    - **Redundancy**: Locally-redundant storage (LRS)
1. While your storage account is being created, go to Visual studio code, and expand the **Labfiles/02-image-classification** folder.
1. In that folder, select **replace.ps1** and review the code. You'll see that it replaces the name of your storage account for the placeholder in a JSON file (the COCO file) we use in a later step. Replace the placeholder *in the first line only* of the file with the name of your storage account. Save the file.
1. Right-click on the **02-image-classification** folder and open an Integrated Terminal. Run the following command.

    ```powershell
    ./replace.ps1
    ```

1. You can review the COCO file to ensure your storage account name is there. Select **training-images/training_labels.json** and view the first few entries. In the *absolute_url* field, you should see something similar to *"https://myStorage.blob.core.windows.net/fruit/...*. If you don't see the change expected, make sure you updated only the first placeholder in the PowerShell script.
1. Close both the JSON and PowerShell file, and go back to your browser window.
1. Your storage account should be complete. Go to your storage account.
1. Enable public access on the storage account. In the left pane, navigate to **Configuration** in the **Settings** group, and enable *Allow Blob anonymous access*. Select **Save**
1. In the left pane, in **Data storage**, select **Containers** and create a new container named `fruit`, and set **Anonymous access level** to *Container (anonymous read access for containers and blobs)*.

    > **Note**: If the **Anonymous access level** is disabled, refresh the browser page.

1. Navigate to `fruit`, select **Upload**, and upload the images (and the one JSON file) in **Labfiles/02-image-classification/training-images** to that container.

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
