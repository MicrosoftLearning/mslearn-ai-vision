---
lab:
    title: 'Read Text in Images'
    module: 'Module 11 - Reading Text in Images and Documents'
---

# Read Text in Images

Optical character recognition (OCR) is a subset of computer vision that deals with reading text in images and documents. The **Azure AI Vision** service provides an API for reading text, which you'll explore in this exercise.

## Clone the repository for this course

If you haven't already done so, you must clone the code repository for this course:

1. Start Visual Studio Code.
2. Open the palette (SHIFT+CTRL+P) and run a **Git: Clone** command to clone the `https://github.com/MicrosoftLearning/mslearn-ai-vision` repository to a local folder (it doesn't matter which folder).
3. When the repository has been cloned, open the folder in Visual Studio Code.
4. Wait while additional files are installed to support the C# code projects in the repo.

    > **Note**: If you are prompted to add required assets to build and debug, select **Not Now**. If you are prompted with the Message *Detected an Azure Function Project in folder*, you can safely close that message.

## Provision an Azure AI Services resource

If you don't already have one in your subscription, you'll need to provision an **Azure AI Services** resource.

1. Open the Azure portal at `https://portal.azure.com`, and sign in using the Microsoft account associated with your Azure subscription.
2. In the top search bar, search for *Azure AI services*, select **Azure AI Services**, and create an Azure AI services multi-service account resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Choose or create a resource group (if you are using a restricted subscription, you may not have permission to create a new resource group - use the one provided)*
    - **Region**: *Choose from East US, France Central, Korea Central, North Europe, Southeast Asia, West Europe, West US, or East Asia\**
    - **Name**: *Enter a unique name*
    - **Pricing tier**: Standard S0

    \*Azure AI Vision 4.0 features are currently only available in these regions.

3. Select the required checkboxes and create the resource.
4. Wait for deployment to complete, and then view the deployment details.
5. When the resource has been deployed, go to it and view its **Keys and Endpoint** page. You'll need the endpoint and one of the keys from this page in the next procedure.

## Prepare to use the Azure AI Vision SDK

In this exercise, you'll complete a partially implemented client application that uses the Azure AI Vision SDK to read text.

> **Note**: You can choose to use the SDK for either **C#** or **Python**. In the following steps, perform the actions appropriate for your preferred language.

1. In Visual Studio Code, in the **Explorer** pane, browse to the **Labfiles\05-ocr** folder and expand the **C-Sharp** or **Python** folder depending on your language preference.
2. Right-click the **read-text** folder and open an integrated terminal. Then install the Azure AI Vision SDK package by running the appropriate command for your language preference:

    **C#**
    
    ```
    dotnet add package Azure.AI.Vision.ImageAnalysis
    ```

    > **Note**: If you are prompted to install dev kit extensions, you can safely close the message.

    **Python**
    
    ```
    pip install azure-ai-vision-imageanalysis
    ```

3. View the contents of the **read-text** folder, and note that it contains a file for configuration settings:

    - **C#**: appsettings.json
    - **Python**: .env

    Open the configuration file and update the configuration values it contains to reflect the **endpoint** and an authentication **key** for your Azure AI services resource. Save your changes.


## Use the Azure AI Vision SDK to read text from an image

One of the features of the **Azure AI Vision SDK** is to read text from an image. In this exercise, you'll complete a partially implemented client application that uses the Azure AI Vision SDK to read text from an image.

1. The **read-text** folder contains a code file for the client application:

    - **C#**: Program.cs
    - **Python**: read-text.py

    Open the code file and at the top, under the existing namespace references, find the comment **Import namespaces**. Then, under this comment, add the following language-specific code to import the namespaces you'll need to use the Azure AI Vision SDK:

    **C#**
    
    ```C#
    // Import namespaces
    using Azure.AI.Vision.ImageAnalysis;
    ```
    
    **Python**
    
    ```Python
    # import namespaces
    from azure.ai.vision.imageanalysis import ImageAnalysisClient
    from azure.ai.vision.imageanalysis.models import VisualFeatures
    from azure.core.credentials import AzureKeyCredential
    ```

2. In the code file for your client application, in the **Main** function, the code to load the configuration settings has been provided. Then find the comment **Authenticate Azure AI Vision client**. Then, under this comment, add the following language-specific code to create and authenticate an Azure AI Vision client object:

    **C#**
    
    ```C#
    // Authenticate Azure AI Vision client
    ImageAnalysisClient client = new ImageAnalysisClient(
        new Uri(aiSvcEndpoint),
        new AzureKeyCredential(aiSvcKey));
    ```
    
    **Python**
    
    ```Python
    # Authenticate Azure AI Vision client
    cv_client = ImageAnalysisClient(
        endpoint=ai_endpoint,
        credential=AzureKeyCredential(ai_key)
    )
    ```

3. In the **Main** function, under the code you just added, note that the code specifies the path to an image file and then passes the image path to the **GetTextRead** function. This function isn't yet fully implemented. Let's implement **GetTextRead** function before function name **AnnotateLines** / **annotate_lines**. Noting that the visual features are specified when calling the `Analyze` function:

    **C#**
    
    ```C#
    static ImageAnalysisResult GetTextRead(ImageAnalysisClient client, string imageFile)
    {
        // Read image file
        FileStream stream = new FileStream(imageFile, FileMode.Open, FileAccess.Read);
        Console.WriteLine($"Reading image file {imageFile}...\n");

        // Use Analyze image function to read text in image
        Console.WriteLine($"Analyzing image for text...\n");
        ImageAnalysisResult result = client.Analyze(
            BinaryData.FromStream(stream),
            // Specify the features to be retrieved
            VisualFeatures.Read);

        stream.Close();

        return result;
    }
    ```
    
    **Python**
    
    ```Python
    def GetTextRead(client, image_file):
        print(f'\nReading text in image {image_file}...')

        # Read image file
        with open(image_file, "rb") as image:
            # Use Analyze image function to read text in image
            print('  Analyzing image for text...')
            result = client.analyze(
                image_data=image,
                # Specify the features to be retrieved
                visual_features=[VisualFeatures.READ]
            )
        
        return result
    ```

4. Let's add some code to invoke the **GetTextRead** function. Find the comment **Read text in image**. Then, under this comment, add the following language-specific code, noting that how the return result is being verify:

    **C#**

    ```C#
    // Read text in image
    var result = GetTextRead(client, imageFile);
    // Check if text is detected
    if (result.Read == null)
    {
        Console.WriteLine("No text detected in image.");
        return;
    }

    // Annotate lines of text in image
    AnnotateLines(imageFile, result.Read);
    
    // Annotate individual words in image
    AnnotateWords(imageFile, result.Read);
    ```
    
    **Python**
    
    ```Python
    # Read text in image
    result = GetTextRead(cv_client, image_file)
    if result.read is not None:
        detected_text = result.read
    else:
        print('No text detected in image.')
        exit()

    # Annotate lines of text in image
    annotate_lines(image_file, detected_text)

    # Annotate individual words in image
    annotate_words(image_file, detected_text)
    ```

5. From the implemented code, as you can see the result and original image path is use to create the annotate result image.

6. In the **Main** function, under the code you just added, note that the detected text pass to the **PrintDetectedText** function. This function isn't yet fully implemented. Let's implement **PrintDetectedText** function before function name **AnnotateLines** / **annotate_lines**:

    **C#**
    
    ```C#
    static void PrintDetectedText(ReadResult detectedText)
    {
        // Print the detected text
        Console.WriteLine($"Detected text in image:");
        foreach (var line in detectedText.Blocks.SelectMany(block => block.Lines))
        {
            // Return the text detected in the image
            Console.WriteLine($"Line: {line.Text}");

            // Return the position bounding box around each line
            Console.WriteLine($"   Bounding Polygon: [{string.Join(" ", line.BoundingPolygon)}]");

            foreach (DetectedTextWord word in line.Words)
            {
                // Return the text detected in the image
                Console.WriteLine($"     Word: '{word.Text}', Confidence {word.Confidence:F4}, Bounding Polygon: [{string.Join(" ", word.BoundingPolygon)}]");
            }
        }
    }
    ```
    
    **Python**
    
    ```Python
    def PrintDetectedText(detected_text):
    # Print the detected text
    for line in detected_text.blocks[0].lines:
        # Return the text detected in the image
        print(f"Line: {line.text}")

        # Return the position bounding box around each line
        r = line.bounding_polygon
        bounding_polygon = ((r[0].x, r[0].y),(r[1].x, r[1].y),(r[2].x, r[2].y),(r[3].x, r[3].y))
        print("   Bounding Polygon: {}".format(bounding_polygon))

        for word in line.words:
            # Return the text detected in the image
            r = word.bounding_polygon
            bounding_polygon = ((r[0].x, r[0].y),(r[1].x, r[1].y),(r[2].x, r[2].y),(r[3].x, r[3].y))
            print(f"    Word: '{word.text}', Bounding Polygon: {bounding_polygon}, Confidence: {word.confidence:.4f}")
    ```

7. In the **read-text/images** folder, select **Lincoln.jpg** to view the file that your code processes.

8. Save your changes and return to the integrated terminal for the **read-text** folder, and enter the following command to run the program:

    **C#**
    
    ```
    dotnet run
    ```
    
    **Python**
    
    ```
    python read-text.py
    ```

9. When error **Lincoln.jpg** not found happen on **C#** program. Copy **images** folder to the bin folder locate at **bin\Debug\netcoreapp8.0** and run the program again.

10. In the **read-text** folder, select the **lines.jpg** or **words.jpg** image and noticed how there's a polygon around each *word* of the note.


## Use the Azure AI Vision SDK to read handwritten text from an image

In the previous exercise, you read well defined text from an image, but sometimes you might also want to read text from handwritten notes or papers. The good news is that the **Azure AI Vision SDK** can also read handwritten text with the same exact code you used to read well defined text. We'll use the same code from the previous exercise, but this time we'll use a different image.

1. In the **read-text/images** folder, select on **Note.jpg** to view the file that your code processes.

2. In the code file for your application, in the **Main** function. Find the comment **Get image**. Change the path to the *images/Lincoln.jpg* image file.

3. From the integrated terminal for the **read-text** folder, enter the following command to run the program:

    **C#**
    
    ```
    dotnet run
    ```
    
    **Python**
    
    ```
    python read-text.py
    ```

4. In the **read-text** folder, select the **lines.jpg** or **words.jpg** image and noticed how there's a polygon around each *word* of the note.

## Clean up resources

If you're not using the Azure resources created in this lab for other training modules, you can delete them to avoid incurring further charges. Here's how:

1. Open the Azure portal at `https://portal.azure.com`, and sign in using the Microsoft account associated with your Azure subscription.

2. In the top search bar, search for *Azure AI services multi-service account*, and select the Azure AI services multi-service account resource you created in this lab

3. On the resource page, select **Delete** and follow the instructions to delete the resource.

## More information

For more information about using the **Azure AI Vision** service to read text, see the [Azure AI Vision documentation](https://learn.microsoft.com/azure/ai-services/computer-vision/concept-ocr).
