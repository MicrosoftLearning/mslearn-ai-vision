---
lab:
    title: 'Detect Objects in Images with Azure AI Custom Vision'
---

# Detect Objects in Images with Azure AI Custom Vision

In this exercise, you will use the Custom Vision service to train an *object detection* model that can detect and locate three classes of fruit (apple, banana, and orange) in an image.

## Create Custom Vision resources

If you already have **Custom Vision** resources for training and prediction in your Azure subscription, you can use them or an existing multi-service account in this exercise. If not, use the following instructions to create them.

> **Note**: If you use a multi-service account, the key and endpoint will be the same for both your training and prediction.

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
   cd mslearn-ai-vision/Labfiles/03-object-detection
    ```

## Create a Custom Vision project

To train an object detection model, you need to create a Custom Vision project based on your training resource. To do this, you'll use the Custom Vision portal.

1. In a new browser tab, open the Custom Vision portal at `https://customvision.ai`, and sign in using the Microsoft account associated with your Azure subscription.
1. Create a new project with the following settings:
    - **Name**: Detect Fruit
    - **Description**: Object detection for fruit.
    - **Resource**: *The Custom Vision resource you created previously*
    - **Project Types**: Object Detection
    - **Domains**: General
1. Wait for the project to be created and opened in the browser.

## Add and tag images

To train an object detection model, you need to upload images that contain the classes you want the model to identify, and tag them to indicate bounding boxes for each object instance.

1. Download the training images from `https://github.com/MicrosoftLearning/mslearn-ai-vision/raw/main/Labfiles/03-object-detection/training-images.zip` and extract the zip folder to view its contents. This folder contains images of fruit.
1. In the Custom Vision portal, in your object detection project, select **Add images** and upload all of the images in the extracted folder.
1. After the images have been uploaded, select the first one to open it.
1. Hold the mouse over any object in the image until an automatically detected region is displayed like the image below. Then select the object, and if necessary resize the region to surround it.

    ![The default region for an object](../media/object-region.jpg)

    Alternatively, you can simply drag around the object to create a region.

1. When the region surrounds the object, add a new tag with the appropriate object type (*apple*, *banana*, or *orange*) as shown here:

    ![A tagged object in an image](../media/object-tag.jpg)

1. Select and tag each other object in the image, resizing the regions and adding new tags as required.

    ![Two tagged objects in an image](../media/object-tags.jpg)

1. Use the **>** link on the right to go to the next image, and tag its objects. Then just keep working through the entire image collection, tagging each apple, banana, and orange.

1. When you have finished tagging the last image, close the **Image Detail** editor. On the **Training Images** page, under **Tags**, select **Tagged** to see all of your tagged images:

![Tagged images in a project](../media/tagged-images.jpg)

## Use the Training API to upload images

You can use the UI in the Custom Vision portal to tag your images, but many AI development teams use other tools that generate files containing information about tags and object regions in images. In scenarios like this, you can use the Custom Vision training API to upload tagged images to the project.

> **Note**: In this exercise, you can choose to use the API from either the **C#** or **Python** SDK. In the steps below, perform the actions appropriate for your preferred language.

1. Click the *settings* (&#9881;) icon at the top right of the **Training Images** page in the Custom Vision portal to view the project settings.
1. Under **General** (on the left), note the **Project Id** that uniquely identifies this project.
1. On the right, under **Resources** note that the key and endpoint are shown. These are the details for the *training* resource (you can also obtain this information by viewing the resource in the Azure portal).
1. Back in the Azure Portal, run the command `cd C-Sharp/train-detector` or `cd Python/train-detector` depending on your language preference.
1. Install the Custom Vision Training package by running the appropriate command for your language preference:

    **C#**

    ```
   dotnet add package Microsoft.Azure.CognitiveServices.Vision.CustomVision.Training --version 2.0.0
    ```

    **Python**

    ```
   pip install azure-cognitiveservices-vision-customvision==3.1.1
    ```

1. Using the `ls` command, you can view the contents of the **train-detector** folder. Note that it contains a file for configuration settings:

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
1. Run `code tagged-images.json` to open the file and examine the JSON it contains. The JSON defines a list of images, each containing one or more tagged regions. Each tagged region includes a tag name, and the top and left coordinates and width and height dimensions of the bounding box containing the tagged object.

    > **Note**: The coordinates and dimensions in this file indicate relative points on the image. For example, a *height* value of 0.7 indicates a box that is 70% of the height of the image. Some tagging tools generate other formats of file in which the coordinate and dimension values represent pixels, inches, or other units of measurements.

1. Note that the **train-detector** folder contains a subfolder in which the image files referenced in the JSON file are stored.

1. Note that the **train-detector** folder contains a code file for the client application:

    - **C#**: Program.cs
    - **Python**: train-detector.py

    Open the code file and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **CustomVisionTrainingClient**, which is then used with the project ID to create a **Project** reference to your project.
    - The **Upload_Images** function extracts the tagged region information from the JSON file and uses it to create a batch of images with regions, which it then uploads to the project.

1. Run the following command to run the program:
    
    **C#**
    
    ```
   dotnet run
    ```
    
    **Python**
    
    ```
   python train-detector.py
    ```
    
1. Wait for the program to end. Then return to your browser and view the **Training Images** page for your project in the Custom Vision portal (refreshing the browser if necessary).
1. Verify that some new tagged images have been added to the project.

## Train and test a model

Now that you've tagged the images in your project, you're ready to train a model.

1. In the Custom Vision project, click **Train** to train an object detection model using the tagged images. Select the **Quick Training** option.
1. Wait for training to complete (it might take ten minutes or so), and then review the *Precision*, *Recall*, and *mAP* performance metrics - these measure the prediction accuracy of the classification model, and should all be high.
1. At the top right of the page, click **Quick Test**, and then in the **Image URL** box, enter `https://aka.ms/apple-orange` and view the prediction that is generated. Then close the **Quick Test** window.

## Publish the object detection model

Now you're ready to publish your trained model so that it can be used from a client application.

1. In the Custom Vision portal, on the **Performance** page,  click **&#128504; Publish** to publish the trained model with the following settings:
    - **Model name**: fruit-detector
    - **Prediction Resource**: *The **prediction** resource you created previously which ends with "-Prediction" (<u>not</u> the training resource)*.
1. At the top left of the **Project Settings** page, click the *Projects Gallery* (&#128065;) icon to return to the Custom Vision portal home page, where your project is now listed.
1. On the Custom Vision portal home page, at the top right, click the *settings* (&#9881;) icon to view the settings for your Custom Vision service. Then, under **Resources**, find your *prediction* resource which ends with "-Prediction" (<u>not</u> the training resource) to determine its **Key** and **Endpoint** values (you can also obtain this information by viewing the resource in the Azure portal).

## Use the image classifier from a client application

Now that you've published the image classification model, you can use it from a client application. Once again, you can choose to use **C#** or **Python**.

1. In the Azure Portal, navigate to the **test-detector** folder running the command `cd ../test-detector`.
1. Enter the following SDK-specific command to install the Custom Vision Prediction package:

    **C#**

    ```
   dotnet add package Microsoft.Azure.CognitiveServices.Vision.CustomVision.Prediction --version 2.0.0
    ```

    **Python**

    ```
   pip install azure-cognitiveservices-vision-customvision==3.1.1
    ```

> **Note**: The Python SDK package includes both training and prediction packages, and may already be installed.

1. Open the configuration file for your client application (*appsettings.json* for C# or *.env* for Python) and update the configuration values it contains to reflect the endpoint and key for your Custom Vision *prediction* resource, the project ID for the object detection project, and the name of your published model (which should be *fruit-detector*). Save your changes and close the file.
1. Open the code file for your client application (*Program.cs* for C#, *test-detector.py* for Python) and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **CustomVisionPredictionClient**.
    - The prediction client object is used to get object detection predictions for the **produce.jpg** image, specifying the project ID and model name in the request. The predicted tagged regions are then drawn on the image, and the result is saved as **output.jpg**.
1. Close the code editor and enter the following command to run the program:

    **C#**

    ```
   dotnet run
    ```

    **Python**

    ```
   python test-detector.py
    ```

1. After the program has completed, in the cloud shell toolbar, select **Upload/Download files** and then **Download**. In the new dialog box, enter the following file path and select **Download**:

    **C#**
   
    ```
   mslearn-ai-vision/Labfiles/03-object-detection/C-Sharp/test-detector/output.jpg
    ```

    **Python**
   
    ```
   mslearn-ai-vision/Labfiles/03-object-detection/Python/test-detector/output.jpg
    ```

1. View the resulting **output.jpg** file to see the detected objects in the image.

## Clean up resources

If you're not using the Azure resources created in this lab for other training modules, you can delete them to avoid incurring further charges.

1. Open the Azure portal at `https://portal.azure.com`, and in the top search bar, search for the resources you created in this lab.

1. On the resource page, select **Delete** and follow the instructions to delete the resource. Alternatively, you can delete the entire resource group to clean up all resources at the same time.
   
## More information

For more information about object detection with the Custom Vision service, see the [Custom Vision documentation](https://docs.microsoft.com/azure/cognitive-services/custom-vision-service/).
