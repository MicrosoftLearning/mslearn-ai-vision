---
lab:
    title: 'Read text in images'
    description: 'Use optical character recognition (OCR) in the Azure AI Vision Image Analysis service to locate and extract text in images.'
---

# Read text in images

Optical character recognition (OCR) is a subset of computer vision that deals with reading text in images and documents. The **Azure AI Vision** Image Analysis service provides an API for reading text, which you'll explore in this exercise.

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

## Develop a text extraction app with the Azure AI Vision SDK

In this exercise, you'll complete a partially implemented client application that uses the Azure AI Vision SDK to extract text from images.

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
   cd mslearn-ai-vision/Labfiles/ocr/python/read-text
   ls -a -l
    ```

    **C#**

    ```
   cd mslearn-ai-vision/Labfiles/ocr/c-sharp/read-text
   ls -a -l
    ```

    The folder contains application configuration and code files for your app. It also contains an **/images** subfolder, which contains some image files for your app to analyze.

1. Install the Azure AI Vision SDK package and other required packages by running the appropriate commands for your language preference:

    **Python**

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install dotenv pillow matplotlib azure-ai-vision-imageanalysis==1.0.0
    ```

    **C#**

    ```
   dotnet add package Azure.AI.Vision.ImageAnalysis -v 1.0.0
   dotnet add package SkiaSharp --version 3.116.1
   dotnet add package SkiaSharp.NativeAssets.Linux --version 3.116.1
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

### Add code to read text from an image

1. In the cloud shell command line, enter the following command to open the code file for the client application:

    **Python**

    ```
   code read-text.py
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

1. In the **Main** function, the code to load the configuration settings has been provided. Then find the comment **Authenticate Azure AI Vision client** and add the following language-specific code to create and authenticate an Azure AI Vision client object:

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

1. In the **Main** function, under the code you just added, note that the code passes an image path (which was obtained from the program's arguments) to the **GetTextRead** function. This function isn't yet fully implemented.

1. Let's add some code to the body of the **GetTextRead** function. Find the comment **Use Analyze image function to read text in image** and add the following language-specific code, noting that the visual features are specified when calling the `Analyze` function:

    **Python**

    ```python
   # Use Analyze image function to read text in image
   result = cv_client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.READ])

   # Display the image and overlay it with the extracted text
   if result.read is not None:
        print("\nText:")

        # Prepare image for drawing
        image = Image.open(image_file)
        fig = plt.figure(figsize=(image.width/100, image.height/100))
        plt.axis('off')
        draw = ImageDraw.Draw(image)
        color = 'cyan'

        for line in result.read.blocks[0].lines:

            # Return the text detected in the image

            
        # Save image
        plt.imshow(image)
        plt.tight_layout(pad=0)
        textfile = 'text.jpg'
        fig.savefig(textfile)
        print('\n  Results saved in', textfile)
    ```

    **C#**

    ```csharp
   // Use Analyze image function to read text in image
   ImageAnalysisResult result = client.Analyze(
        BinaryData.FromStream(stream),
        // Specify the features to be retrieved
        VisualFeatures.Read);
    
   stream.Close();
    
   // Display analysis results
   if (result.Read != null)
   {
        Console.WriteLine($"Text:");
    
        // Load the image using SkiaSharp
        using SKBitmap bitmap = SKBitmap.Decode(imageFile);
        // Create canvas to draw on the bitmap
        using SKCanvas canvas = new SKCanvas(bitmap);

        // Create paint for drawing polygons (bounding boxes)
        SKPaint paint = new SKPaint
        {
            Color = SKColors.Cyan,
            StrokeWidth = 3,
            Style = SKPaintStyle.Stroke,
            IsAntialias = true
        };

        foreach (var line in result.Read.Blocks.SelectMany(block => block.Lines))
        {

            // Return the text detected in the image
    
    
        }
            
        // Save the annotated image using SkiaSharp
        var textFile = "text.jpg";
        using (SKFileWStream output = new SKFileWStream(textFile))
        {
            // Encode the bitmap into JPEG format with full quality (100)
            bitmap.Encode(output, SKEncodedImageFormat.Jpeg, 100);
        }

        Console.WriteLine($"\nResults saved in {textFile}\n");
   }
    ```

1. In the code you just added in the **GetTextRead** function, find the **Return the text detected in the image** comment and add the following code to print the image text to the console and generate an image file named **text.jpg** that highlights the image's text:

    **Python**

    ```python
   # Return the text detected in the image
   print(f"  {line.text}")    
    
   drawLinePolygon = True
    
   r = line.bounding_polygon
   bounding_polygon = ((r[0].x, r[0].y),(r[1].x, r[1].y),(r[2].x, r[2].y),(r[3].x, r[3].y))
    
   # Return the position bounding box around each line
    
    
   # Find individual words in the line
    
    
   # Draw line bounding polygon
   if drawLinePolygon:
        draw.polygon(bounding_polygon, outline=color, width=3)
    ```

    **C#**

    ```csharp
   // Return the text detected in the image
   Console.WriteLine($"   '{line.Text}'");
    
   // Draw bounding box around line
   bool drawLinePolygon = true;
    
   // Return the position bounding box around each line
    
    
    
   // Find individual words in the line
    
    
    
   // Draw line bounding polygon
   if (drawLinePolygon)
   {
        var r = line.BoundingPolygon;
        SKPoint[] polygonPoints = new SKPoint[]
        {
            new SKPoint(r[0].X, r[0].Y),
            new SKPoint(r[1].X, r[1].Y),
            new SKPoint(r[2].X, r[2].Y),
            new SKPoint(r[3].X, r[3].Y)
        };

        // Call helper method to draw a polygon
        DrawPolygon(canvas, polygonPoints, paint);
   }
    ```

1. Save your changes (*CTRL+S*) but keep the code editor open in case you need to fix any typo's.

1. Resize the panes so you can see more of the console, then enter the following command to run the program:

    **Python**

    ```
   python read-text.py images/Lincoln.jpg
    ```

    **C#**

    ```
   dotnet run images/Lincoln.jpg
    ```

1. The program reads the text in the specified image file (*images/Lincoln.jpg*), which looks like this:

    ![Photograph of a statue of Abraham Lincoln.](../media/Lincoln.jpg)

1. In the **read-text** folder, a **text.jpg** image has been created. Use the (Azure cloud shell-specific) **download** command to download it:

    ```
   download text.jpg
    ```

    The download command creates a popup link at the bottom right of your browser, which you can select to download and open the file. The image should look simlar to this:

    ![An image with the text highlighted.](../media/text.jpg)

1. Run the program again, this time specifying the parameter *images/Business-card.jpg* to extract text from the following image:

    ![Image of a scanned buisness card.](../media/Business-card.jpg)

    **Python**

    ```
   python read-text.py images/Business-card.jpg
    ```

    **C#**

    ```
   dotnet run images/Business-card.jpg
    ```

1. Download and view the resulting **text.jpg** file:

    ```
   download text.jpg
    ```

1. Run the program one more time, this time specifying the parameter *images/Note.jpg* to extract text from this image:

    ![Photograph of a handwritten shopping list.](../media/Note.jpg)

    **Python**

    ```
   python read-text.py images/Note.jpg
    ```

    **C#**

    ```
   dotnet run images/Note.jpg
    ```

1. Download and view the resulting **text.jpg** file:

    ```
   download text.jpg
    ```

### Add code to return the position of each line of text

1. Resize the panes so you can see more of the code file. Then find the comment **Return the position bounding box around each line** and add the following code:

    **Python**

    ```python
   # Return the position bounding box around each line
   print("   Bounding Polygon: {}".format(bounding_polygon))
    ```

    **C#**

    ```csharp
   // Return the position bounding box around each line
   Console.WriteLine($"   Bounding Polygon: [{string.Join(" ", line.BoundingPolygon)}]");
    ```

1. Save your changes (*CTRL+S*). Then, in the command line pane, rerun the program to extract text from *images/Lincoln.jpg*.
1. Observe the output, which should be each line of text in the image with their respective position in the image.
1. Rerun the program for *images/Business-card.jpg* and *images/Note.jpg*.

### Add code to identify individual words in an image

1. In the code file, find the comment **Find individual words in the line** and add the following code:

    **Python**
    
    ```python
   # Find individual words in the line
   for word in line.words:
        r = word.bounding_polygon
        bounding_polygon = ((r[0].x, r[0].y),(r[1].x, r[1].y),(r[2].x, r[2].y),(r[3].x, r[3].y))
        print(f"    Word: '{word.text}', Bounding Polygon: {bounding_polygon}, Confidence: {word.confidence:.4f}")
    
        # Draw word bounding polygon
        drawLinePolygon = False
        draw.polygon(bounding_polygon, outline=color, width=3)
    ```

    **C#**

    ```C#
   // Find individual words in the line
   foreach (DetectedTextWord word in line.Words)
   {
        Console.WriteLine($"     Word: '{word.Text}', Confidence {word.Confidence:F4}, Bounding Polygon: [{string.Join(" ", word.BoundingPolygon)}]");
        
        // Draw word bounding polygon
        drawLinePolygon = false;
        var r = word.BoundingPolygon;
    
        // Convert the bounding polygon into an array of SKPoints    
        SKPoint[] polygonPoints = new SKPoint[]
        {
            new SKPoint(r[0].X, r[0].Y),
            new SKPoint(r[1].X, r[1].Y),
            new SKPoint(r[2].X, r[2].Y),
            new SKPoint(r[3].X, r[3].Y)
        };

        // Draw the word polygon on the canvas
        DrawPolygon(canvas, polygonPoints, paint);
   }
    ```

1. Save your changes (*CTRL+S*). Then, in the command line pane, rerun the program to extract text from *images/Lincoln.jpg*.
1. Observe the output, which should be each word of text in the image with their respective position in the image. Notice how the confidence level of each word is also returned.
1. Download and view the **text.jpg** image again and notice how there's a polygon around each *word*.

    ```
   download text.jpg
    ```

1. Rerun the program for *images/Business-card.jpg* and *images/Note.jpg*.

## Clean up resources

If you've finished exploring Azure AI Vision, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs:

1. Open the Azure portal at `https://portal.azure.com`, and sign in using the Microsoft account associated with your Azure subscription.

1. In the top search bar, search for *Computer Vision*, and select the Computer Vision resource you created in this lab.

1. On the resource page, select **Delete** and follow the instructions to delete the resource.
