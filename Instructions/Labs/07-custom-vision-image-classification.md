---
lab:
    title: 'Classify Images with Azure AI Custom Vision'
---

# Classify Images with Azure AI Custom Vision

The **Azure AI Custom Vision** service enables you to create computer vision models that are trained on your own images. You can use it to train *image classification* and *object detection* models; which you can then publish and consume from applications.

In this exercise, you will use the Custom Vision service to train an image classification model that can identify three classes of fruit (apple, banana, and orange).

## Create Custom Vision resources

Before you can train a model, you will need Azure resources for *training* and *prediction*. You can create **Custom Vision** resources for each of these tasks, or you can create a single **Azure AI Services** resource and use it for either (or both).

In this exercise, you'll create **Custom Vision** resources for training and prediction so that you can manage access and costs for these workloads separately.

1. In a new browser tab, open the Azure portal at `https://portal.azure.com`, and sign in using the Microsoft account associated with your Azure subscription.
1. Select the **&#65291;Create a resource** button, search for *custom vision*, and create a **Custom Vision** resource with the following settings:
    - **Create options**: Both
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Choose or create a resource group (if you are using a restricted subscription, you may not have permission to create a new resource group - use the one provided)*
    - **Region**: *Choose any available region*
    - **Name**: *Enter a unique name*
    - **Training pricing tier**: F0
    - **Prediction pricing tier**: F0

    > **Note**: If you already have an F0 custom vision service in your subscription, select **S0** for this one.

1. Wait for the resources to be created, and then view the deployment details and note that two Custom Vision resources are provisioned; one for training, and another for prediction (evident by the **-Prediction** suffix). You can view these by navigating to the resource group where you created them.

> **Important**: Each resource has its own *endpoint* and *keys*, which are used to manage access from your code. To train an image classification model, your code must use the *training* resource (with its endpoint and key); and to use the trained model to predict image classes, your code must use the *prediction* resource (with its endpoint and key).

## Clone the repository for this course

You'll develop your code using Cloud Shell from the Azure Portal. The code files for your app have been provided in a GitHub repo.

> **Tip**: If you have already cloned the **mslearn-ai-vision** repo recently, you can skip this task. Otherwise, follow these steps to clone it to your development environment.

1. In the Azure Portal, use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment. The cloud shell provides a command line interface in a pane at the bottom of the Azure portal.

    > **Note**: If you have previously created a cloud shell that uses a *Bash* environment, switch it to ***PowerShell***.

1. In the cloud shell toolbar, in the **Settings** menu, select **Go to Classic version** (this is required to use the code editor).

    > **Tip**: As you paste commands into the cloudshell, the ouput may take up a large amount of the screen buffer. You can clear the screen by entering the `cls` command to make it easier to focus on each task.

1. In the PowerShell pane, enter the following commands to clone the GitHub repo for this exercise:

    ```
    rm -r mslearn-ai-vision -f
    git clone https://github.com/microsoftlearning/mslearn-ai-vision mslearn-ai-vision
    ```

1. After the repo has been cloned, navigate to the folder containing the application code files:  

    ```
   cd mslearn-ai-vision/Labfiles/07-custom-vision-image-classification
    ```
    
## Create a Custom Vision project

To train an image classification model, you need to create a Custom Vision project based on your training resource. To do this, you'll use the Custom Vision portal.

1. Download the training images from `https://github.com/MicrosoftLearning/mslearn-ai-vision/raw/main/Labfiles/07-custom-vision-image-classification/training-images.zip` and extract the zip folder to view its contents. This folder contains subfolders of apple, banana, and orange images.
1. In a new browser tab, open the Custom Vision portal at `https://customvision.ai`. If prompted, sign in using the Microsoft account associated with your Azure subscription and agree to the terms of service.
1. In the Custom Vision portal, create a new project with the following settings:
    - **Name**: Classify Fruit
    - **Description**: Image classification for fruit
    - **Resource**: *The Custom Vision resource you created previously*
    - **Project Types**: Classification
    - **Classification Types**: Multiclass (single tag per image)
    - **Domains**: Food
1. In the new project, click **\[+\] Add images**, and select all of the files in the **training-images/apple** folder you viewed previously. Then upload the image files, specifying the tag *apple*, like this:

![Upload apple with apple tag](../media/upload_apples.jpg)
   
1. Repeat the previous step to upload the images in the **banana** folder with the tag *banana*, and the images in the **orange** folder with the tag *orange*.
1. Explore the images you have uploaded in the Custom Vision project - there should be 15 images of each class, like this:

![Tagged images of fruit - 15 apples, 15 bananas, and 15 oranges](../media/fruit.jpg)
    
1. In the Custom Vision project, above the images, click **Train** to train a classification model using the tagged images. Select the **Quick Training** option, and then wait for the training iteration to complete (this may take a minute or so).
1. When the model iteration has been trained, review the *Precision*, *Recall*, and *AP* performance metrics - these measure the prediction accuracy of the classification model, and should all be high.

> **Note**: The performance metrics are based on a probability threshold of 50% for each prediction (in other words, if the model calculates a 50% or higher probability that an image is of a particular class, then that class is predicted). You can adjust this at the top-left of the page.

## Test the model

Now that you've trained the model, you can test it.

1. Above the performance metrics, click **Quick Test**.
1. In the **Image URL** box, type `https://aka.ms/apple-image` and click &#10132;
1. View the predictions returned by your model - the probability score for *apple* should be the highest, like this:

![An image with a class prediction of apple](../media/test-apple.jpg)

1. Close the **Quick Test** window.

## View the project settings

The project you have created has been assigned a unique identifier, which you will need to specify in any code that interacts with it.

1. Click the *settings* (&#9881;) icon at the top right of the **Performance** page to view the project settings.
1. Under **General** (on the left), note the **Project Id** that uniquely identifies this project.
1. On the right, under **Resources** note that the key and endpoint are shown. These are the details for the *training* resource (you can also obtain this information by viewing the resource in the Azure portal).

## Use the *training* API

The Custom Vision portal provides a convenient user interface that you can use to upload and tag images, and train models. However, in some scenarios you may want to automate model training by using the Custom Vision training API.

> **Note**: In this exercise, you can choose to use the API from either the **C#** or **Python** SDK. In the steps below, perform the actions appropriate for your preferred language.

1. Back in the Azure Portal, run the command `cd C-Sharp/train-classifier` or `cd Python/train-classifier` depending on your language preference.
1. Install the Custom Vision Training package by running the appropriate command for your language preference:

    **C#**

    ```
    dotnet add package Microsoft.Azure.CognitiveServices.Vision.CustomVision.Training --version 2.0.0
    ```

    **Python**

    ```
    pip install azure-cognitiveservices-vision-customvision==3.1.0
    ```

1. Using the `ls` command, you can view the contents of the **train-classifier** folder, and note that it contains a file for configuration settings:
    - **C#**: appsettings.json
    - **Python**: .env

1. Enter the following command to edit the configuration file that has been provided:

    **C#**

    ```
   code appsettings.json
    ```

    **Python**

    ```
   code .env
    ```

    The file is opened in a code editor.

1. In the code file, update the configuration values it contains to reflect the **endpoint** and an authentication **key** for your Custom Vision *training* resource, and the project ID for the object detection project you created previously.
1. After you've replaced the placeholders, within the code editor, use the **CTRL+S** command or **Right-click > Save** to save your changes and then use the **CTRL+Q** command or **Right-click > Quit** to close the code editor while keeping the cloud shell command line open.
1. Note that the **train-classifier** folder contains a code file for the client application:

    - **C#**: Program.cs
    - **Python**: train-classifier.py

    Open the code file and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **CustomVisionTrainingClient**, which is then used with the project ID to create a **Project** reference to your project.
    - The **Upload_Images** function retrieves the tags that are defined in the Custom Vision project and then uploads image files from correspondingly named folders to the project, assigning the appropriate tag ID.
    - The **Train_Model** function creates a new training iteration for the project and waits for training to complete.
1. Close the code editor and enter the following command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python train-classifier.py
    ```
    
1. Wait for the program to end. Then return to your browser and view the **Training Images** page for your project in the Custom Vision portal (refreshing the browser if necessary).
1. Verify that some new tagged images have been added to the project. Then view the **Performance** page and verify that a new iteration has been created.

## Publish the image classification model

Now you're ready to publish your trained model so that it can be used from a client application.

1. In the Custom Vision portal, on the **Performance** page,  click **&#128504; Publish** to publish the trained model with the following settings:
    - **Model name**: fruit-classifier
    - **Prediction Resource**: *The **prediction** resource you created previously which ends with "-Prediction" (<u>not</u> the training resource)*.
1. At the top left of the **Project Settings** page, click the *Projects Gallery* (&#128065;) icon to return to the Custom Vision portal home page, where your project is now listed.
1. On the Custom Vision portal home page, at the top right, click the *settings* (&#9881;) icon to view the settings for your Custom Vision service. Then, under **Resources**, find your *prediction* resource which ends with "-Prediction" (<u>not</u> the training resource) to determine its **Key** and **Endpoint** values (you can also obtain this information by viewing the resource in the Azure portal).

## Use the image classifier from a client application

Now that you've published the image classification model, you can use it from a client application. Once again, you can choose to use **C#** or **Python**.

1. Back in cloud shell, run the command `cd ../test-classifier`, then enter the following SDK-specific command to install the Custom Vision Prediction package:

    **C#**

    ```
    dotnet add package Microsoft.Azure.CognitiveServices.Vision.CustomVision.Prediction --version 2.0.0
    ```

    **Python**

    ```
    pip install azure-cognitiveservices-vision-customvision==3.1.0
    ```

> **Note**: The Python SDK package includes both training and prediction packages, and may already be installed.

1. Using the `ls` command, you can view the contents of the **test-classifier** folder, which are used to implement a test client application for your image classification model.
1. Open the configuration file for your client application (*appsettings.json* for C# or *.env* for Python) and update the configuration values it contains to reflect the endpoint and key for your Custom Vision *prediction* resource, the project ID for the classification project, and the name of your published model (which should be *fruit-classifier*). Save your changes and close the code editor.
1. Open the code file for your client application (*Program.cs* for C#, *test-classification.py* for Python) and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **CustomVisionPredictionClient**.
    - The prediction client object is used to predict a class for each image in the **test-images** folder, specifying the project ID and model name for each request. Each prediction includes a probability for each possible class, and only predicted tags with a probability greater than 50% are displayed.
1. Close the code editor and enter the following SDK-specific command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python test-classifier.py
    ```

1. View the label (tag) and probability scores for each prediction. You can download the images in the **test-images** folder to verify that the model has classified them correctly.

1. In the cloud shell toolbar, select **Upload/Download files** and then **Download**. In the new dialog box, enter the following file path and select **Download**:

    **C#**
   
    ```
   mslearn-ai-vision/Labfiles/07-custom-vision-image-classification/C-Sharp/test-classifier/test-images/IMG_TEST_1.jpg
    ```

    **Python**
   
    ```
   mslearn-ai-vision/Labfiles/07-custom-vision-image-classification/Python/test-classifier/test-images/IMG_TEST_1.jpg
    ```

   You can also download `IMG_TEST_2.jpg` and `IMG_TEST_3.jpg` using the same path.

## Clean up resources

If you're not using the Azure resources created in this lab for other training modules, you can delete them to avoid incurring further charges.

1. Open the Azure portal at `https://portal.azure.com`, and in the top search bar, search for the resources you created in this lab.

1. On the resource page, select **Delete** and follow the instructions to delete the resource. Alternatively, you can delete the entire resource group to clean up all resources at the same time.

## More information

For more information about image classification with the Custom Vision service, see the [Custom Vision documentation](https://docs.microsoft.com/azure/cognitive-services/custom-vision-service/).
