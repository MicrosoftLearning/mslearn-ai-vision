---
lab:
    title: 'Detect and Analyze Faces'
    module: 'Module 4 - Detecting and Analyze Faces'
---

# Detect and Analyze Faces

The ability to detect and analyze human faces is a core AI capability. In this exercise, you'll explore two Azure AI Services that you can use to work with faces in images: the **Azure AI Vision** service, and the **Face** service.

> **Important**: This lab can be completed without requesting any additional access to restricted features.

> **Note**: From June 21st 2022, capabilities of Azure AI services that return personally identifiable information are restricted to customers who have been granted [limited access](https://docs.microsoft.com/azure/cognitive-services/cognitive-services-limited-access). Additionally, capabilities that infer emotional state are no longer available. For more details about the changes Microsoft has made, and why - see [Responsible AI investments and safeguards for facial recognition](https://azure.microsoft.com/blog/responsible-ai-investments-and-safeguards-for-facial-recognition/).

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
   cd mslearn-ai-vision/Labfiles/04-face
    ```

## Prepare to use the Azure AI Vision SDK

In this exercise, you'll complete a partially implemented client application that uses the Azure AI Vision SDK to analyze images.

> **Note**: You can choose to use the SDK for either **C#** or **Python**. In the steps below, perform the actions appropriate for your preferred language.

1. Navigate to the folder containing the application code files for your preferred language:  

    **C#**

    ```
   cd C-Sharp/computer-vision
    ```
    
    **Python**

    ```
   cd Python/computer-vision
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
1. After you've replaced the placeholders, use the **CTRL+S** command to save your changes and then use the **CTRL+Q** command to close the code editor while keeping the cloud shell command line open.

## View the image you will analyze

In this exercise, you will use the Azure AI Vision service to analyze an image of people.

1. In the cloud shell toolbar, select **Upload/Download files** and then **Download**. In the new dialog box, enter the following file path and select **Download**:

    ```
    mslearn-ai-vision/Labfiles/04-face/C-Sharp/computer-vision/images/people.jpg
    ```

1. Open the **people.jpg** image to view it.

## Detect faces in an image

Now you're ready to use the SDK to call the Vision service and detect faces in an image.

1. Note that the **computer-vision** folder contains a code file for the client application:

    - **C#**: Program.cs
    - **Python**: detect-people.py

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
    
1. In the **Main** function, note that the code to load the configuration settings has been provided. Then find the comment **Authenticate Azure AI Vision client**. Then, under this comment, add the following language-specific code to create and authenticate a Azure AI Vision client object:

    **C#**

    ```C#
    // Authenticate Azure AI Vision client
    ImageAnalysisClient cvClient = new ImageAnalysisClient(
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

1. In the **Main** function, under the code you just added, note that the code specifies the path to an image file and then passes the image path to a function named **AnalyzeImage**. This function is not yet fully implemented.

1. In the **AnalyzeImage** function, under the comment **Get result with specified features to be retrieved (PEOPLE)**, add the following code:

    **C#**

    ```C#
    // Get result with specified features to be retrieved (PEOPLE)
    ImageAnalysisResult result = client.Analyze(
        BinaryData.FromStream(stream),
        VisualFeatures.People);
    ```

    **Python**

    ```Python
    # Get result with specified features to be retrieved (PEOPLE)
    result = cv_client.analyze(
        image_data=image_data,
        visual_features=[
            VisualFeatures.PEOPLE],
    )
    ```

1. In the **AnalyzeImage** function, under the comment **Draw bounding box around detected people**, add the following code:

    **C#**

    ```C
    // Draw bounding box around detected people
    foreach (DetectedPerson person in result.People.Values)
    {
        if (person.Confidence > 0.5) 
        {
            // Draw object bounding box
            var r = person.BoundingBox;
            SKRect rect = new SKRect(r.X, r.Y, r.X + r.Width, r.Y + r.Height);
            canvas.DrawRect(rect, paint);
        }

        // Return the confidence of the person detected
        //Console.WriteLine($"   Bounding box {person.BoundingBox.ToString()}, Confidence: {person.Confidence:F2}");
    }
    ```

    **Python**
    
    ```Python
    # Draw bounding box around detected people
    for detected_people in result.people.list:
        if(detected_people.confidence > 0.5):
            # Draw object bounding box
            r = detected_people.bounding_box
            bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height))
            draw.rectangle(bounding_box, outline=color, width=3)

        # Return the confidence of the person detected
        #print(" {} (confidence: {:.2f}%)".format(detected_people.bounding_box, detected_people.confidence * 100))
    ```

1. Save your changes, close the code editor, and enter the following command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python detect-people.py
    ```

6. Observe the output, which should indicate the number of faces detected.
7. Download the **people.jpg** file that is generated in the same folder as your code file to see the annotated faces. In this case, your code has used the attributes of the face to label the location of the top left of the box, and the bounding box coordinates to draw a rectangle around each face.

If you'd like to see the confidence score of all people the service detected, you can uncomment the code line under the comment `Return the confidence of the person detected` and rerun the code.

## Prepare to use the Face SDK

While the **Azure AI Vision** service offers basic face detection (along with many other image analysis capabilities), the **Face** service provides more comprehensive functionality for facial analysis and recognition.

1. Navigate to the **face-api** folder by running the command `cd ../face-api`. Then install the Face SDK package by running the appropriate command for your language preference:

    **C#**

    ```
    dotnet add package Azure.AI.Vision.Face -v 1.0.0-beta.2
    ```

    **Python**

    ```
    pip install azure-ai-vision-face==1.0.0b2
    ```
    
1. View the contents of the **face-api** folder, and note that it contains a file for configuration settings:
    - **C#**: appsettings.json
    - **Python**: .env

1. Open the configuration file and update the configuration values it contains to reflect the **endpoint** and an authentication **key** for your Azure AI services resource. Save your changes.

1. Note that the **face-api** folder contains a code file for the client application:

    - **C#**: Program.cs
    - **Python**: analyze-faces.py

1. Open the code file and at the top, under the existing namespace references, find the comment **Import namespaces**. Then, under this comment, add the following language-specific code to import the namespaces you will need to use the Vision SDK:

    **C#**

    ```C#
    // Import namespaces
    using Azure;
    using Azure.AI.Vision.Face;
    using SkiaSharp;
    ```

    **Python**

    ```Python
    # Import namespaces
    from azure.ai.vision.face import FaceClient
    from azure.ai.vision.face.models import FaceDetectionModel, FaceRecognitionModel, FaceAttributeTypeDetection03
    from azure.core.credentials import AzureKeyCredential
    ```

1. In the **Main** function, note that the code to load the configuration settings has been provided. Then find the comment **Authenticate Face client**. Then, under this comment, add the following language-specific code to create and authenticate a **FaceClient** object:

    **C#**

    ```C#
    // Authenticate Face client
    faceClient = new FaceClient(
        new Uri(cogSvcEndpoint),
        new AzureKeyCredential(cogSvcKey));
    ```

    **Python**

    ```Python
    # Authenticate Face client
    face_client = FaceClient(
        endpoint=cog_endpoint,
        credential=AzureKeyCredential(cog_key)
    )
    ```

1. In the **Main** function, under the code you just added, note that the code displays a menu that enables you to call functions in your code to explore the capabilities of the Face service. You will implement these functions in the remainder of this exercise.

## Detect and analyze faces

One of the most fundamental capabilities of the Face service is to detect faces in an image, and determine their attributes, such as head pose, blur, the presence of mask, and so on.

1. In the code file for your application, in the **Main** function, examine the code that runs if the user selects menu option **1**. This code calls the **DetectFaces** function, passing the path to an image file.
1. Find the **DetectFaces** function in the code file, and under the comment **Specify facial features to be retrieved**, add the following code:

    **C#**

    ```C#
    // Specify facial features to be retrieved
    FaceAttributeType[] features = new FaceAttributeType[]
    {
        FaceAttributeType.Detection03.HeadPose,
        FaceAttributeType.Detection03.Blur,
        FaceAttributeType.Detection03.Mask
    };
    ```

    **Python**

    ```Python
    # Specify facial features to be retrieved
    features = [FaceAttributeTypeDetection03.HEAD_POSE,
                FaceAttributeTypeDetection03.BLUR,
                FaceAttributeTypeDetection03.MASK]
    ```

1. In the **DetectFaces** function, under the code you just added, find the comment **Get faces** and add the following code:

    **C#**

    ```C#
    // Get faces
    using (var imageData = File.OpenRead(imageFile))
    {    
        var response = await faceClient.DetectAsync(
            BinaryData.FromStream(imageData),
            FaceDetectionModel.Detection03,
            FaceRecognitionModel.Recognition04,
            returnFaceId: false,
            returnFaceAttributes: features);
        IReadOnlyList<FaceDetectionResult> detected_faces = response.Value;

        if (detected_faces.Count() > 0)
        {
            Console.WriteLine($"{detected_faces.Count()} faces detected.");

            // Load the image using SkiaSharp
            using SKBitmap bitmap = SKBitmap.Decode(imageFile);
            using SKCanvas canvas = new SKCanvas(bitmap);

            // Set up paint styles for drawing
            SKPaint rectPaint = new SKPaint
            {
                Color = SKColors.LightGreen,
                StrokeWidth = 3,
                Style = SKPaintStyle.Stroke,
                IsAntialias = true
            };

            SKPaint textPaint = new SKPaint
            {
                Color = SKColors.White,
                TextSize = 16,
                IsAntialias = true
            };

            int faceCount=0;

            // Draw and annotate each face
            foreach (var face in detected_faces)
            {
                faceCount++;
                Console.WriteLine($"\nFace number {faceCount}");
            
                // Get face properties
                Console.WriteLine($" - Head Pose (Yaw): {face.FaceAttributes.HeadPose.Yaw}");
                Console.WriteLine($" - Head Pose (Pitch): {face.FaceAttributes.HeadPose.Pitch}");
                Console.WriteLine($" - Head Pose (Roll): {face.FaceAttributes.HeadPose.Roll}");
                Console.WriteLine($" - Blur: {face.FaceAttributes.Blur.BlurLevel}");
                Console.WriteLine($" - Mask: {face.FaceAttributes.Mask.Type}");

                // Draw and annotate face
                var r = face.FaceRectangle;

                // Create an SKRect from the face rectangle data
                SKRect rect = new SKRect(r.Left, r.Top, r.Left + r.Width, r.Top + r.Height);
                canvas.DrawRect(rect, rectPaint);

                string annotation = $"Face number {faceCount}";
                canvas.DrawText(annotation, r.Left, r.Top, textPaint);
            }

            // Save annotated image
            using (SKFileWStream output = new SKFileWStream("detected_faces.jpg"))
            {
                bitmap.Encode(output, SKEncodedImageFormat.Jpeg, 100);
            }

            Console.WriteLine(" Results saved in detected_faces.jpg");   
        }
    }
    ```

    **Python**

    ```Python
    # Get faces
    with open(image_file, mode="rb") as image_data:
        detected_faces = face_client.detect(
            image_content=image_data.read(),
            detection_model=FaceDetectionModel.DETECTION03,
            recognition_model=FaceRecognitionModel.RECOGNITION04,
            return_face_id=False,
            return_face_attributes=features,
        )

        if len(detected_faces) > 0:
            print(len(detected_faces), 'faces detected.')

            # Prepare image for drawing
            fig = plt.figure(figsize=(8, 6))
            plt.axis('off')
            image = Image.open(image_file)
            draw = ImageDraw.Draw(image)
            color = 'lightgreen'
            face_count = 0

            # Draw and annotate each face
            for face in detected_faces:
    
                # Get face properties
                face_count += 1
                print('\nFace number {}'.format(face_count))

                print(' - Head Pose (Yaw): {}'.format(face.face_attributes.head_pose.yaw))
                print(' - Head Pose (Pitch): {}'.format(face.face_attributes.head_pose.pitch))
                print(' - Head Pose (Roll): {}'.format(face.face_attributes.head_pose.roll))
                print(' - Blur: {}'.format(face.face_attributes.blur.blur_level))
                print(' - Mask: {}'.format(face.face_attributes.mask.type))

                # Draw and annotate face
                r = face.face_rectangle
                bounding_box = ((r.left, r.top), (r.left + r.width, r.top + r.height))
                draw = ImageDraw.Draw(image)
                draw.rectangle(bounding_box, outline=color, width=5)
                annotation = 'Face number {}'.format(face_count)
                plt.annotate(annotation,(r.left, r.top), backgroundcolor=color)

            # Save annotated image
            plt.imshow(image)
            outputfile = 'detected_faces.jpg'
            fig.savefig(outputfile)

            print('\nResults saved in', outputfile)
    ```

1. Examine the code you added to the **DetectFaces** function. It analyzes an image file and detects any faces it contains, including attributes for head pose, blur, and the presence of mask. The details of each face are displayed, including a unique face identifier that is assigned to each face; and the location of the faces is indicated on the image using a bounding box.
1. Save your changes and close the code editor, then enter the following command to run the program:

    **C#**

    ```
    dotnet run
    ```

    *The C# output may display warnings about asynchronous functions not using the **await** operator. You can ignore these.*

    **Python**

    ```
    python analyze-faces.py
    ```

1. When prompted, enter **1** and observe the output, which should include the ID and attributes of each face detected.
1. Download the **detected_faces.jpg** file that is generated in the same folder as your code file to see the annotated faces.

## Clean up resources

If you're not using the Azure resources created in this lab for other training modules, you can delete them to avoid incurring further charges.

1. Open the Azure portal at `https://portal.azure.com`, and in the top search bar, search for the resources you created in this lab.

1. On the resource page, select **Delete** and follow the instructions to delete the resource. Alternatively, you can delete the entire resource group to clean up all resources at the same time.

## More information

There are several additional features available within the **Face** service, but following the [Responsible AI Standard](https://aka.ms/aah91ff) those are restricted behind a Limited Access policy. These features include identifying, verifying, and creating facial recognition models. To learn more and apply for access, see the [Limited Access for Azure AI Services](https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-limited-access).

For more information about using the **Azure AI Vision** service for face detection, see the [Azure AI Vision documentation](https://docs.microsoft.com/azure/cognitive-services/computer-vision/concept-detecting-faces).

To learn more about the **Face** service, see the [Face documentation](https://learn.microsoft.com/azure/ai-services/computer-vision/overview-identity).
