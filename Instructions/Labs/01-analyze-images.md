---
lab:
    title: 'Analyze images'
    description: 'Use Azure AI Vision Image Analysis to analyze images, suggest captions and tags, and detect objects and people.'
---

# Analyze images

Azure AI Vision is an artificial intelligence capability that enables software systems to interpret visual input by analyzing images. In Microsoft Azure, the **Vision** Azure AI service provides pre-built models for common computer vision tasks, including analysis of images to suggest captions and tags, detection of common objects and people. You can also use the Azure AI Vision service to remove the background or create a foreground matting of images.

This exercise takes approximately **30** minutes.

## Provision an Azure AI Vision resource

If you don't already have one in your subscription, you'll need to provision an Azure AI Vision resource.

> **Note**: In this exercise, you'll use a standalone **Computer Vision** resource. You can also use Azure AI Vision services in an *Azure AI Services* multi-service resource, either directly or in an *Azure AI Foundry* project.

1. Open the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`, and sign in using your Azure credentials. Close any welcome messages or tips that are displayed.
1. Select **Create a resource**.
1. In the search bar, search for `Computer Vision`, select **Computer Vision**, and create the resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: *Choose from **East US**, **West US**, **France Central**, **Korea Central**, **North Europe**, **Southeast Asia**, **West Europe**, or **East Asia**\**
    - **Name**: *A valid name for your resource*
    - **Pricing tier**: Free F0

    \*Azure AI Vision 4.0 full feature sets are currently only available in these regions.

1. Select the required checkboxes and create the resource.
1. Wait for deployment to complete, and then view the deployment details.
1. When the resource has been deployed, go to it and view the **Keys and Endpoint** section on its **Overview** page. You will need the endpoint and one of the keys from this page in the next procedure.

## Develop an image analysis app with the Azure AI Vision SDK

In this exercise, you'll complete a partially implemented client application that uses the Azure AI Vision SDK to analyze images.

> **Note**: You can choose to use the SDK for either **C#** or **Python**. In the steps below, perform the actions appropriate for your preferred language.

### Prepare the application configuration

1. In the Azure portal, use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment with no storage in your subscription.

    The cloud shell provides a command-line interface in a pane at the bottom of the Azure portal. You can resize or maximize this pane to make it easier to work in.

    > **Note**: If you have previously created a cloud shell that uses a *Bash* environment, switch it to ***PowerShell***.

1. In the cloud shell toolbar, in the **Settings** menu, select **Go to Classic version** (this is required to use the code editor).

    **<font color="red">Ensure you've switched to the classic version of the cloud shell before continuing.</font>**

1. Resize the cloud shell pane so you can still see the **Overview** page for your Computer Vision resource.

    > **Tip**" You can resize the pane by dragging the top border. You can also use the minimize and maximize buttons to switch between the cloud shell and the main portal interface.

1. In the cloud shell pane, enter the following commands to clone the GitHub repo containing the code files for this exercise (type the command, or copy it to the clipboard and then right-click in the command line and paste as plain text):

    ```
    rm -r mslearn-ai-vision -f
    git clone https://github.com/MicrosoftLearning/mslearn-ai-vision
    ```

    > **Tip**: As you paste commands into the cloudshell, the ouput may take up a large amount of the screen buffer. You can clear the screen by entering the `cls` command to make it easier to focus on each task.

1. After the repo has been cloned, use the following commands to navigate to and view he language-specific folder containing the application code files, based on the programming language of your choice (Python or C#):   

    **Python**

    ```
   cd mslearn-ai-vision/Labfiles/analyze-images/python/image-analysis
   ls -a -l
    ```

    **C#**

    ```
   cd mslearn-ai-vision/Labfiles/analyze-images/c-sharp/image-analysis
   ls -a -l
    ```

    The folder contains application configuration and code files for your app. It also contains a **/images** subfolder, which contains some image files for your app to analyze.
    
1. Install the Azure AI Vision SDK package and other required packages by running the appropriate commands for your language preference:

    **Python**
    
    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt azure-ai-vision-imageanalysis==1.0.0
    ```

    **C#**
    
    ```
   dotnet add package Azure.AI.Vision.ImageAnalysis -v 1.0.0
    ``` 

1. Enter the following command to edit the configuration file for your app:

    **Python**

    ```
   code .env
    ```

    **C#**

    ```
   code appsettings.json
    ```

    The file is opened in a code editor.

1. In the code file, update the configuration values it contains to reflect the **endpoint** and an authentication **key** for your Computer Vision resource (copied from its **Overview** page in the Azure portal).
1. After you've replaced the placeholders, use the **CTRL+S** command to save your changes and then use the **CTRL+Q** command to close the code editor while keeping the cloud shell command line open.

### Add code to suggest a caption

1. In the cloud shell command line, enter the following command to open the code file for the client application:

    **Python**

    ```
   code image-analysis.py
    ```

    **C#**

    ```
   code Program.cs
    ```

    > **Tip**: You might want to maximize the cloud shell pane and move the split-bar between the command line cosole and the code editor so you can see the code more easily.

1. In the code file, find the comment **Import namespaces**, and add the following code to import the namespaces you will need to use the Azure AI Vision SDK:

    **Python**
    
    ```python
   # import namespaces
   from azure.ai.vision.imageanalysis import ImageAnalysisClient
   from azure.ai.vision.imageanalysis.models import VisualFeatures
   from azure.core.credentials import AzureKeyCredential
    ```

    **C#**
    
    ```csharp
   // Import namespaces
   using Azure.AI.Vision.ImageAnalysis;
    ```

1. Find the comment **Declare variable for Azure AI Vision client**, and add the following code:

    **Python**
    
    ```python
   # Declare variable for Azure AI Vision client
   global cv_client
    ```

    **C#**
    
    ```csharp
   // Declare variable for Azure AI Vision client
   private static ImageAnalysisClient client;
    ```

1. In the **Main** function, note that the code to load the configuration settings has been provided. Then find the comment **Authenticate Azure AI Vision client** and add the following code to create and authenticate a Azure AI Vision client object (be sure to maintain the correct indentation levels):

    **Python**
    
    ```python
   # Authenticate Azure AI Vision client
   cv_client = ImageAnalysisClient(
        endpoint=ai_endpoint,
        credential=AzureKeyCredential(ai_key))
    ```

    **C#**
    
    ```csharp
   // Authenticate Azure AI Vision client
   client = new ImageAnalysisClient(
        new Uri(aiSvcEndpoint),
        new AzureKeyCredential(aiSvcKey));
    ```

1. In the **Main** function, under the code you just added, note that the code specifies the path to an image file and then passes the image path to another function (**AnalyzeImage**). This function is not yet fully implemented.

1. In the **AnalyzeImage** function, find the comment **Get result with specify features to be retrieved** and add the following code:

    **Python**

    ```python
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

    **C#**

    ```csharp
   // Get result with specified features to be retrieved
   ImageAnalysisResult result = client.Analyze(
        BinaryData.FromStream(stream),
        VisualFeatures.Caption | 
        VisualFeatures.DenseCaptions |
        VisualFeatures.Objects |
        VisualFeatures.Tags |
        VisualFeatures.People);
    ```
    
1. In the **AnalyzeImage** function, under the comment **Display analysis results**, add the following code (including the comments indicating where you will add more code later.):

    **Python**

    ```python
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

    **C#**
    
    ```csharp
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
    
1. Save your changes (*CTRL+S*) and resize the panes so you can clearly see the command line console while keeping the code editor open. Then enter the following command to run the program with the argument **images/street.jpg**:

    **Python**

    ```
   python image-analysis.py images/street.jpg
    ```

    **C#**

    ```
   dotnet run images/street.jpg
    ```

1. Observe the output, which should include a suggested caption for the **street.jpg** image, which looks like this:

    ![A picture of a busy street.](../media/street.jpg)

1. Run the program again, this time with the argument **images/building.jpg** to see the caption that gets generated for the **building.jpg** image, which looks like this:

    ![A picture of a building.](../media/building.jpg)

1. Repeat the previous step to generate a caption for the **images/person.jpg** file, which looks like this:

    ![A picture of a person.](../media/person.jpg)

### Add code to generate suggested tags

It can sometimes be useful to identify relevant *tags* that provide clues about the contents of an image.

1. In the code editor, in the **AnalyzeImage** function, find the comment **Get image tags** and add the following code:

    **Python**
    
    ```python
   # Get image tags
   if result.tags is not None:
        print("\nTags:")
        for tag in result.tags.list:
            print(" Tag: '{}' (confidence: {:.2f}%)".format(tag.name, tag.confidence * 100))
    ```

    **C#**

    ```csharp
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

1. Save your changes (*CTRL+S*) and run the program with the argument **images/street.jpg**, observing that in addition to the image caption, a list of suggested tags is displayed.
1. Rerun the program for the **images/building.jpg** and **images/person.jpg** files.

### Add code to detect and locate objects

1. In the code editor, in the **AnalyzeImage** function, find the comment **Get objects in the image** and add the following code:

    **Python**

    ```python
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
        objectfile = 'objects.jpg'
        fig.savefig(objectfile)
        print('  Results saved in', objectfile)
    ```

    **C#**

    ```csharp
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
            Color = SKColors.Cyan,
            IsAntialias = true
        };

        SKFont textFont = new SKFont(SKTypeface.Default,24,1,0);

        foreach (DetectedObject detectedObject in result.Objects.Values)
        {
            Console.WriteLine($"   \"{detectedObject.Tags[0].Name}\"");

            // Draw object bounding box
            var r = detectedObject.BoundingBox;
            SKRect rect = new SKRect(r.X, r.Y, r.X + r.Width, r.Y + r.Height);
            canvas.DrawRect(rect, paint);

            // Draw label
            canvas.DrawText(detectedObject.Tags[0].Name, r.X, r.Y - 5, SKTextAlign.Left, textFont, textPaint);
        }

        // Save the annotated image
        var objectFile = "objects.jpg";
        using SKFileWStream output = new SKFileWStream(objectFile);
        bitmap.Encode(output, SKEncodedImageFormat.Jpeg, 100);
        Console.WriteLine($"  Results saved in {objectFile}\n");
   }
    ```

1. Save your changes (*CTRL+S*) and run the program with the argument **images/street.jpg**, observing that in addition to the image caption and suggested tags; a file named **objects.jpg** is generated.
1. Use the (Azure cloud shell-specific) **download** command to download the **objects.jpg** file:

    ```
   download objects.jpg
    ```

    The download command creates a popup link at the bottom right of your browser, which you can select to download and open the file. The image should look simlar to this:

    ![An image with object boundary boxes.](../media/objects.jpg)

1. Rerun the program for the **images/building.jpg** and **images/person.jpg** files, downloading the generated objects.jpg file after each run.

### Add code to detect and locate people

1. In the code editor, in the **AnalyzeImage** function, find the comment **Get people in the image** and add the following code:

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
    
            # Print location and confidence of each person detected
            print(" {} (confidence: {:.2f}%)".format(detected_people.bounding_box, detected_people.confidence * 100))
            
        # Save annotated image
        plt.imshow(image)
        plt.tight_layout(pad=0)
        peoplefile = 'people.jpg'
        fig.savefig(peoplefile)
        print('  Results saved in', peoplefile)
    ```

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

            // Print location and confidence of each person detected
            Console.WriteLine($"   Bounding box {person.BoundingBox}, Confidence: {person.Confidence:F2}");
        }

        // Save the annotated image
        var peopleFile = "people.jpg";
        using SKFileWStream output = new SKFileWStream(peopleFile);
        bitmap.Encode(output, SKEncodedImageFormat.Jpeg, 100);
        Console.WriteLine($"  Results saved in {peopleFile}\n");
   }
    ```

1. Save your changes (*CTRL+S*) and run the program with the argument **images/street.jpg**, observing that in addition to the image caption, suggested tags, and objects.jpg file; a list of person locations and file named **people.jpg** is generated.
1. Use the (Azure cloud shell-specific) **download** command to download the **objects.jpg** file:

    ```
   download people.jpg
    ```

    The download command creates a popup link at the bottom right of your browser, which you can select to download and open the file. The image should look simlar to this:

    ![An image with boundary boxes for detected people.](../media/people.jpg)

1. Rerun the program for the **images/building.jpg** and **images/person.jpg** files, downloading the generated people.jpg file after each run.

## Clean up resources

If you've finished exploring Azure AI Vision, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs:

1. Open the Azure portal at `https://portal.azure.com`, and sign in using the Microsoft account associated with your Azure subscription.

1. In the top search bar, search for *Computer Vision*, and select the Computer Vision resource you created in this lab.

1. On the resource page, select **Delete** and follow the instructions to delete the resource.

