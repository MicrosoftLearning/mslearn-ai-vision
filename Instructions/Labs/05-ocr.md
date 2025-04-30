---
lab:
    title: 'Read Text in Images'
    module: 'Module 11 - Reading Text in Images and Documents'
---

# Read Text in Images

Optical character recognition (OCR) is a subset of computer vision that deals with reading text in images and documents. The **Azure AI Vision** service provides an API for reading text, which you'll explore in this exercise.

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
   cd mslearn-ai-vision/Labfiles/05-ocr
    ```

## Prepare to use the Azure AI Vision SDK

In this exercise, you'll complete a partially implemented client application that uses the Azure AI Vision SDK to read text.

> **Note**: You can choose to use the SDK for either **C#** or **Python**. In the steps below, perform the actions appropriate for your preferred language.

1. Navigate to the folder containing the application code files for your preferred language:  

    **C#**

    ```
   cd C-Sharp/read-text
    ```
    
    **Python**

    ```
   cd Python/read-text
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
    pip install matplotlib
    ```

1. Using the `ls` command, you can view the contents of the **computer-vision** folder. Note that it contains a file for configuration settings:

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
1. After you've replaced the placeholders, within the code editor, use the **CTRL+S** command or **Right-click > Save** to save your changes and then use the **CTRL+Q** command or **Right-click > Quit** to close the code editor while keeping the cloud shell command line open.

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
    using SkiaSharp;
    ```
    
    **Python**
    
    ```Python
    # import namespaces
    from azure.ai.vision.imageanalysis import ImageAnalysisClient
    from azure.ai.vision.imageanalysis.models import VisualFeatures
    from azure.core.credentials import AzureKeyCredential
    ```

1. In the code file for your client application, in the **Main** function, the code to load the configuration settings has been provided. Then find the comment **Authenticate Azure AI Vision client**. Then, under this comment, add the following language-specific code to create and authenticate an Azure AI Vision client object:

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

1. In the **Main** function, under the code you just added, note that the code specifies the path to an image file and then passes the image path to the **GetTextRead** function. This function isn't yet fully implemented.

1. Let's add some code to the body of the **GetTextRead** function. Find the comment **Use Analyze image function to read text in image**. Then, under this comment, add the following language-specific code, noting that the visual features are specified when calling the `Analyze` function:

    **C#**

    ```C#
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
        using (SKFileWStream output = new SKFileWStream("text.jpg"))
        {
            // Encode the bitmap into JPEG format with full quality (100)
            bitmap.Encode(output, SKEncodedImageFormat.Jpeg, 100);
        }

        Console.WriteLine("\nResults saved in text.jpg\n");
    }
    ```
    
    **Python**
    
    ```Python
    # Use Analyze image function to read text in image
    result = cv_client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.READ]
    )

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
        outputfile = 'text.jpg'
        fig.savefig(outputfile)
        print('\n  Results saved in', outputfile)
    ```

1. In the code you just added in the **GetTextRead** function, and under the **Return the text detected in the image** comment, add the following code (this code prints the image text to the console and generates the image **text.jpg** which highlights the image's text):

    **C#**
    
    ```C#
    // Return the text detected in the image
    Console.WriteLine($"   '{line.Text}'");
    
    // Draw bounding box around line
    bool drawLinePolygon = true;
    
    // Return the position bounding box around each line
    
    
    
    // Return each word detected in the image and the position bounding box around each word with the confidence level of each word
    
    
    
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

    DrawPolygon(canvas, polygonPoints, paint);
    }
    ```
    
    **Python**
    
    ```Python
    # Return the text detected in the image
    print(f"  {line.text}")    
    
    drawLinePolygon = True
    
    r = line.bounding_polygon
    bounding_polygon = ((r[0].x, r[0].y),(r[1].x, r[1].y),(r[2].x, r[2].y),(r[3].x, r[3].y))
    
    # Return the position bounding box around each line
    
    
    # Return each word detected in the image and the position bounding box around each word with the confidence level of each word
    
    
    # Draw line bounding polygon
    if drawLinePolygon:
        draw.polygon(bounding_polygon, outline=color, width=3)
    ```

1. For the C# program file only, a helper function is still needed to draw a polygon. Under the **Helper method to draw a polygon given an array of SKPoints** comment, add the following code:

    **C#**
   
    ```C#
    // Helper method to draw a polygon given an array of SKPoints
    static void DrawPolygon(SKCanvas canvas, SKPoint[] points, SKPaint paint)
    {
        if (points == null || points.Length == 0)
            return;

        using (var path = new SKPath())
        {
            path.MoveTo(points[0]);
            for (int i = 1; i < points.Length; i++)
            {
                path.LineTo(points[i]);
            }
            path.Close();
            canvas.DrawPath(path, paint);
        }
    }
    ```

1. In the **Main** function, examine the code that runs if the user selects menu option **1**. This code calls the **GetTextRead** function, passing the path to the *Lincoln.jpg* image file.

1. Save your changes and close the code editor.

1. In the cloud shell toolbar, select **Upload/Download files** and then **Download**. In the new dialog box, enter the following file path and select **Download**:

    **C#**
   
    ```
    mslearn-ai-vision/Labfiles/05-ocr/C-Sharp/read-text/images/Lincoln.jpg
    ```

    **Python**

    ```
    mslearn-ai-vision/Labfiles/05-ocr/Python/read-text/images/Lincoln.jpg
    ```
       
1. Open the **Lincoln.jpg** image to view it.

1. After viewing the image that your code processes, enter the following command to run the program:

    **C#**
    
    ```
    dotnet run
    ```
    
    **Python**
    
    ```
    python read-text.py
    ```

1. When prompted, enter **1** and observe the output, which is the text extracted from the image.

1. In the **read-text** folder, a **text.jpg** image has been created. You can download it using the file path `mslearn-ai-vision/Labfiles/05-ocr/***C-Sharp or Python***/read-text/text.jpg` and notice how there's a polygon around each *line* of text.

1. Reopen the code file and find the comment **Return the position bounding box around each line**. Then, under this comment, add the following code:

    **C#**
    
    ```C#
    // Return the position bounding box around each line
    Console.WriteLine($"   Bounding Polygon: [{string.Join(" ", line.BoundingPolygon)}]");
    ```
    
    **Python**
    
    ```Python
    # Return the position bounding box around each line
    print("   Bounding Polygon: {}".format(bounding_polygon))
    ```

1. Save your changes and close the code editor, then enter the following command to run the program:

    **C#**
    
    ```
    dotnet run
    ```
    
    **Python**
    
    ```
    python read-text.py
    ```

1. When prompted, enter **1** and observe the output, which should be each line of text in the image with their respective position in the image.

1. Open the code file again and find the comment **Return each word detected in the image and the position bounding box around each word with the confidence level of each word**. Then, under this comment, add the following code:

    **C#**
    
    ```C#
    // Return each word detected in the image and the position bounding box around each word with the confidence level of each word
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
    
    **Python**
    
    ```Python
    # Return each word detected in the image and the position bounding box around each word with the confidence level of each word
    for word in line.words:
        r = word.bounding_polygon
        bounding_polygon = ((r[0].x, r[0].y),(r[1].x, r[1].y),(r[2].x, r[2].y),(r[3].x, r[3].y))
        print(f"    Word: '{word.text}', Bounding Polygon: {bounding_polygon}, Confidence: {word.confidence:.4f}")
    
        # Draw word bounding polygon
        drawLinePolygon = False
        draw.polygon(bounding_polygon, outline=color, width=3)
    ```

1. Save your changes and close the code editor, then enter the following command to run the program:

    **C#**
    
    ```
    dotnet run
    ```
    
    **Python**
    
    ```
    python read-text.py
    ```

1. When prompted, enter **1** and observe the output, which should be each word of text in the image with their respective position in the image. Notice how the confidence level of each word is also returned.

1. Download the **text.jpg** image again and notice how there's a polygon around each *word*.

## Use the Azure AI Vision SDK to read handwritten text from an image

In the previous exercise, you read well defined text from an image, but sometimes you might also want to read text from handwritten notes or papers. The good news is that the **Azure AI Vision SDK** can also read handwritten text with the same exact code you used to read well defined text. We'll use the same code from the previous exercise, but this time we'll use a different image.

1. Download **Note.jpg** using the file path `mslearn-ai-vision/Labfiles/05-ocr/***C-Sharp or Python***/read-text/images/Note.jpg` to view the next image that your code processes.

1. In the code file for your application, in the **Main** function, examine the code that runs if the user selects menu option **2**. This code calls the **GetTextRead** function, passing the path to the *Note.jpg* image file.

1. From the terminal, enter the following command to run the program:

    **C#**
    
    ```
    dotnet run
    ```
    
    **Python**
    
    ```
    python read-text.py
    ```

1. When prompted, enter **2** and observe the output, which is the text extracted from the note image.

1. Download the **text.jpg** image again and notice how there's a polygon around each *word* of the note.

## Clean up resources

If you're not using the Azure resources created in this lab for other training modules, you can delete them to avoid incurring further charges. Here's how:

1. Open the Azure portal at `https://portal.azure.com`, and sign in using the Microsoft account associated with your Azure subscription.

1. In the top search bar, search for *Computer Vision*, and select the Computer Vision resource you created in this lab.

1. On the resource page, select **Delete** and follow the instructions to delete the resource.

## More information

For more information about using the **Azure AI Vision** service to read text, see the [Azure AI Vision documentation](https://learn.microsoft.com/azure/ai-services/computer-vision/concept-ocr).
