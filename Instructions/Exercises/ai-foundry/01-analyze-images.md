---
lab:
    title: 'Analyze Images with Azure AI Vision'
    module: 'Module 2 - Develop computer vision solutions with Azure AI Vision'
---

# Analyze Images with Azure AI Vision

Azure AI Vision is an artificial intelligence capability that enables software systems to interpret visual input by analyzing images. In Microsoft Azure, the **Vision** Azure AI service provides pre-built models for common computer vision tasks, including analysis of images to suggest captions and tags, detection of common objects and people. You can also use the Azure AI Vision service to remove the background or create a foreground matting of images.

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
1. Wait for deployment to complete, and then view the deployment details.
1. When the resource has been deployed, go to it and view its **Keys and Endpoint** page. You will need the endpoint and one of the keys from this page in the next procedure.

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
   cd mslearn-ai-vision/Labfiles/01-analyze-images
    ```

## Prepare to use the Azure AI Vision SDK

In this exercise, you'll complete a partially implemented client application that uses the Azure AI Vision SDK to analyze images.

> **Note**: You can choose to use the SDK for either **C#** or **Python**. In the steps below, perform the actions appropriate for your preferred language.

1. Navigate to the folder containing the application code files for your preferred language:  

    **C#**

    ```
   cd C-Sharp/image-analysis
    ```
    
    **Python**

    ```
   cd Python/image-analysis
    ```

1. Install the Azure AI Vision SDK package and required dependencies by running the appropriate commands for your language preference:

    **C#**
    
    ```
    dotnet add package Azure.AI.Vision.ImageAnalysis -v 1.0.0
    dotnet add package SkiaSharp --version 3.116.1
    dotnet add package SkiaSharp.NativeAssets.Linux --version 3.116.1
    ``` 

    **Python**
    
    ```
    pip install azure-ai-vision-imageanalysis==1.0.0
    pip install dotenv
    ```

    > **Tip**: If you are doing this lab on your own machine, you'll also need to install `matplotlib` and `pillow`.

1. Using the `ls` command, you can view the contents of the **rest-client** folder. Note that it contains a file for configuration settings:

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

1. In the code file, update the configuration values it contains to reflect the **endpoint** and an authentication **key** for your Computer Vision resource.
1. After you've replaced the placeholders, use the **CTRL+S** command to save your changes and then use the **CTRL+Q** command to close the code editor while keeping the cloud shell command line open.
1. Enter the following command to open the code file for the client application:

    **C#**

    ```
   code Program.cs
    ```

    **Python**

    ```
   code image-analysis.py
    ```

1. Add the following language-specific code under the comment **Import namespaces** to import the namespaces you will need to use the Azure AI Vision SDK:

    **C#**
    
    ```C#
    // Import namespaces
    using Azure.AI.Vision.ImageAnalysis;
    using SkiaSharp;
    ```
    
    **Python**
    
    ```Python
    # import namespaces
    from azure.ai.vision.imageanalysis import ImageAnalysisClient
    from azure.ai.vision.imageanalysis.models import VisualFeatures
    from azure.core.credentials import AzureKeyCredential
    ```
    
## View the images you will analyze

In this exercise, you will use the Azure AI Vision service to analyze multiple images.

1. In the cloud shell toolbar, select **Upload/Download files** and then **Download**. In the new dialog box, enter the following file path and select **Download**:

    ```
    mslearn-ai-vision/Labfiles/01-analyze-images/C-Sharp/image-analysis/images/building.jpg
    ```

1. Repeat the previous step using the paths below to download the remaining images and verify each of their contents:

    ```
    mslearn-ai-vision/Labfiles/01-analyze-images/C-Sharp/image-analysis/images/person.jpg
    mslearn-ai-vision/Labfiles/01-analyze-images/C-Sharp/image-analysis/images/street.jpg
    ```

## Analyze an image to suggest a caption

Now you're ready to use the SDK to call the Vision service and analyze an image.

1. In the code file for your client application (**Program.cs** or **image-analysis.py**), in the **Main** function, note that the code to load the configuration settings has been provided. Then find the comment **Authenticate Azure AI Vision client**. Then, under this comment, add the following language-specific code to create and authenticate a Azure AI Vision client object:

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

1. In the **Main** function, under the code you just added, note that the code specifies the path to an image file and then passes the image path to another function (**AnalyzeImage**). This function is not yet fully implemented.

1. In the **AnalyzeImage** function, under the comment **Get result with specify features to be retrieved**, add the following code:

    **C#**
    
    ```C#
    // Get result with specified features to be retrieved
    ImageAnalysisResult result = client.Analyze(
        BinaryData.FromStream(stream),
        VisualFeatures.Caption | 
        VisualFeatures.DenseCaptions |
        VisualFeatures.Objects |
        VisualFeatures.Tags |
        VisualFeatures.People);
    ```
    
    **Python**
    
    ```Python
    # Get result with specified features to be retrieved
    result = cv_client.analyze(
        image_data=image_data,
        visual_features=[
            VisualFeatures.CAPTION,
            VisualFeatures.DENSE_CAPTIONS,
            VisualFeatures.TAGS,
            VisualFeatures.OBJECTS,
            VisualFeatures.PEOPLE],
    )
    ```
    
1. In the **AnalyzeImage** function, under the comment **Display analysis results**, add the following code (including the comments indicating where you will add more code later.):

    **C#**
    
    ```C#
    // Display analysis results
    // Get image captions
    if (result.Caption.Text != null)
    {
        Console.WriteLine(" Caption:");
        Console.WriteLine($"   \"{result.Caption.Text}\", Confidence {result.Caption.Confidence:0.00}\n");
    }
    
    // Get image dense captions
    Console.WriteLine(" Dense Captions:");
    foreach (DenseCaption denseCaption in result.DenseCaptions.Values)
    {
        Console.WriteLine($"   Caption: '{denseCaption.Text}', Confidence: {denseCaption.Confidence:0.00}");
    }
    
    // Get image tags
    
    
    // Get objects in the image
    
    
    // Get people in the image
    ```
    
    **Python**
    
    ```Python
    # Display analysis results
    # Get image captions
    if result.caption is not None:
        print("\nCaption:")
        print(" Caption: '{}' (confidence: {:.2f}%)".format(result.caption.text, result.caption.confidence * 100))
    
    # Get image dense captions
    if result.dense_captions is not None:
        print("\nDense Captions:")
        for caption in result.dense_captions.list:
            print(" Caption: '{}' (confidence: {:.2f}%)".format(caption.text, caption.confidence * 100))
    
    # Get image tags
    
    
    # Get objects in the image
    
    
    # Get people in the image
    
    ```
    
1. Save your changes and return to the integrated terminal for the **image-analysis** folder, and enter the following command to run the program with the argument **images/street.jpg**:

    **C#**
    
    ```
    dotnet run images/street.jpg
    ```
    
    **Python**
    
    ```
    python image-analysis.py images/street.jpg
    ```

1. Observe the output, which should include a suggested caption for the **street.jpg** image.
1. Run the program again, this time with the argument **images/building.jpg** to see the caption that gets generated for the **building.jpg** image.
1. Repeat the previous step to generate a caption for the **images/person.jpg** file.

## Get suggested tags for an image

It can sometimes be useful to identify relevant *tags* that provide clues about the contents of an image.

1. In the **AnalyzeImage** function, under the comment **Get image tags**, add the following code:

    **C#**
    
    ```C#
    // Get image tags
    if (result.Tags.Values.Count > 0)
    {
        Console.WriteLine($"\n Tags:");
        foreach (DetectedTag tag in result.Tags.Values)
        {
            Console.WriteLine($"   '{tag.Name}', Confidence: {tag.Confidence:F2}");
        }
    }
    ```
    
    **Python**
    
    ```Python
    # Get image tags
    if result.tags is not None:
        print("\nTags:")
        for tag in result.tags.list:
            print(" Tag: '{}' (confidence: {:.2f}%)".format(tag.name, tag.confidence * 100))
    ```

1. Save your changes and run the program once for each of the image files in the **images** folder, observing that in addition to the image caption, a list of suggested tags is displayed.

## Detect and locate objects in an image

*Object detection* is a specific form of computer vision in which individual objects within an image are identified and their location indicated by a bounding box..

1. In the **AnalyzeImage** function, under the comment **Get objects in the image**, add the following code:

    **C#**
    
    ```C#
    // Get objects in the image
    if (result.Objects.Values.Count > 0)
    {
        Console.WriteLine(" Objects:");

        // Load the image using SkiaSharp
        using SKBitmap bitmap = SKBitmap.Decode(imageFile);
        using SKCanvas canvas = new SKCanvas(bitmap);

        // Set up styles for drawing
        SKPaint paint = new SKPaint
        {
            Color = SKColors.Cyan,
            StrokeWidth = 3,
            Style = SKPaintStyle.Stroke
        };

        SKPaint textPaint = new SKPaint
        {
            Color = SKColors.WhiteSmoke,
            TextSize = 16,
            IsAntialias = true
        };

        foreach (DetectedObject detectedObject in result.Objects.Values)
        {
            Console.WriteLine($"   \"{detectedObject.Tags[0].Name}\"");

            // Draw object bounding box
            var r = detectedObject.BoundingBox;
            SKRect rect = new SKRect(r.X, r.Y, r.X + r.Width, r.Y + r.Height);
            canvas.DrawRect(rect, paint);

            // Draw label
            canvas.DrawText(detectedObject.Tags[0].Name, r.X, r.Y - 5, textPaint);
        }

        // Save the annotated image
        using SKFileWStream output = new SKFileWStream("objects.jpg");
        bitmap.Encode(output, SKEncodedImageFormat.Jpeg, 100);
        Console.WriteLine("  Results saved in objects.jpg\n");
    }
    ```
    
    **Python**
    
    ```Python
    # Get objects in the image
    if result.objects is not None:
        print("\nObjects in image:")
    
        # Prepare image for drawing
        image = Image.open(image_filename)
        fig = plt.figure(figsize=(image.width/100, image.height/100))
        plt.axis('off')
        draw = ImageDraw.Draw(image)
        color = 'cyan'
    
        for detected_object in result.objects.list:
            # Print object name
            print(" {} (confidence: {:.2f}%)".format(detected_object.tags[0].name, detected_object.tags[0].confidence * 100))
            
            # Draw object bounding box
            r = detected_object.bounding_box
            bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height)) 
            draw.rectangle(bounding_box, outline=color, width=3)
            plt.annotate(detected_object.tags[0].name,(r.x, r.y), backgroundcolor=color)
    
        # Save annotated image
        plt.imshow(image)
        plt.tight_layout(pad=0)
        outputfile = 'objects.jpg'
        fig.savefig(outputfile)
        print('  Results saved in', outputfile)
    ```

1. Save your changes and run the program once for each of the image files in the **images** folder, observing any objects that are detected. After each run, download and view the **objects.jpg** file that is generated in the same folder as your code file to see the annotated objects.

## Detect and locate people in an image

*People detection* is a specific form of computer vision in which individual people within an image are identified and their location indicated by a bounding box.

1. In the **AnalyzeImage** function, under the comment **Get people in the image**, add the following code:

    **C#**
    
    ```C#
    // Get people in the image
    if (result.People.Values.Count > 0)
    {
        Console.WriteLine($" People:");

        using SKBitmap bitmap = SKBitmap.Decode(imageFile);
        using SKCanvas canvas = new SKCanvas(bitmap);

        SKPaint paint = new SKPaint
        {
            Color = SKColors.Cyan,
            StrokeWidth = 3,
            Style = SKPaintStyle.Stroke
        };

        foreach (DetectedPerson person in result.People.Values)
        {
            // Draw bounding box
            var r = person.BoundingBox;
            SKRect rect = new SKRect(r.X, r.Y, r.X + r.Width, r.Y + r.Height);
            canvas.DrawRect(rect, paint);

            // Return the confidence of the person detected
            //Console.WriteLine($"   Bounding box {person.BoundingBox}, Confidence: {person.Confidence:F2}");
        }

        // Save the annotated image
        using SKFileWStream output = new SKFileWStream("persons.jpg");
        bitmap.Encode(output, SKEncodedImageFormat.Jpeg, 100);
        Console.WriteLine("  Results saved in persons.jpg\n");
    }
    ```
    
    **Python**
    
    ```Python
    # Get people in the image
    if result.people is not None:
        print("\nPeople in image:")
    
        # Prepare image for drawing
        image = Image.open(image_filename)
        fig = plt.figure(figsize=(image.width/100, image.height/100))
        plt.axis('off')
        draw = ImageDraw.Draw(image)
        color = 'cyan'
    
        for detected_people in result.people.list:
            # Draw object bounding box
            r = detected_people.bounding_box
            bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height))
            draw.rectangle(bounding_box, outline=color, width=3)
    
            # Return the confidence of the person detected
            #print(" {} (confidence: {:.2f}%)".format(detected_people.bounding_box, detected_people.confidence * 100))
            
        # Save annotated image
        plt.imshow(image)
        plt.tight_layout(pad=0)
        outputfile = 'people.jpg'
        fig.savefig(outputfile)
        print('  Results saved in', outputfile)
    ```

1. (Optional) Uncomment the **Console.Writeline** command under the **Return the confidence of the person detected** section to review the confidence level returned that a person was detected at a particular position of the image.

1. Save your changes and run the program once for each of the image files in the **images** folder, observing any objects that are detected. After each run, view the **objects.jpg** file that is generated in the same folder as your code file to see the annotated objects.

> **Note**: In the preceding tasks, you used a single method to analyze the image, and then incrementally added code to parse and display the results. The SDK also provides individual methods for suggesting captions, identifying tags, detecting objects, and so on - meaning that you can use the most appropriate method to return only the information you need, reducing the size of the data payload that needs to be returned. See the [.NET SDK documentation](https://learn.microsoft.com/dotnet/api/overview/azure/cognitiveservices/computervision?view=azure-dotnet) or [Python SDK documentation](https://learn.microsoft.com/python/api/azure-cognitiveservices-vision-computervision/azure.cognitiveservices.vision.computervision) for more details.

## Clean up resources

If you're not using the Azure resources created in this lab for other training modules, you can delete them to avoid incurring further charges. Here's how:

1. Open the Azure portal at `https://portal.azure.com`, and sign in using the Microsoft account associated with your Azure subscription.

1. In the top search bar, search for *Computer Vision*, and select the Computer Vision resource you created in this lab.

1. On the resource page, select **Delete** and follow the instructions to delete the resource.

## More information

In this exercise, you explored some of the image analysis and manipulation capabilities of the Azure AI Vision service. The service also includes capabilities for detecting objects and people, and other computer vision tasks.

For more information about using the **Azure AI Vision** service, see the [Azure AI Vision documentation](https://learn.microsoft.com/azure/ai-services/computer-vision/).
