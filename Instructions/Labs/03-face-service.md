---
lab:
    title: 'Detect and analyze faces'
    description: 'Use the Azure AI Vision Face API to implement face detection and analysis solutions.'
---

# Detect and analyze faces

The ability to detect and analyze human faces is a core AI capability. In this exercise, you'll explore two Azure AI Services that you can use to work with faces in images: the **Azure AI Vision** service, and the **Face** service.

This exercise takes approximately **30** minutes.

> **Note**: Capabilities of Azure AI services that return personally identifiable information are restricted to customers who have been granted [limited access](https://docs.microsoft.com/azure/cognitive-services/cognitive-services-limited-access). This exercise does not include facial recognition tasks, and can be completed without requesting any additional access to restricted features.

## Provision an Azure AI Vision resource

If you don't already have one in your subscription, you'll need to provision an Azure AI Vision resource.

> **Note**: In this exercise, you'll use a standalone **Computer Vision** resource. You can also use Azure AI Vision services in an *Azure AI Services* multi-service resource, either directly or in an *Azure AI Foundry* project.

1. Open the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`, and sign in using your Azure credentials.
1. Select **Create a resource**.
1. In the search bar, search for *Computer Vision*, select **Computer Vision**, and create the resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: *Choose from **East US**, **West US**, **France Central**, **Korea Central**, **North Europe**, **Southeast Asia**, **West Europe**, or **East Asia**\**
    - **Name**: *A valid name for your resource*
    - **Pricing tier**: Free F0

    \*Azure AI Vision 4.0 full feature sets are currently only available in these regions.

1. Select the required checkboxes and create the resource.
1. Wait for deployment to complete, and then view the deployment details.
1. When the resource has been deployed, go to it and view the **Keys and Endpoint** section on its **Overview** page. You will need the endpoint and one of the keys from this page in the next procedure.

## Develop a facial analysis app with the Azure AI Vision SDK

In this exercise, you'll complete a partially implemented client application that uses the Azure AI Vision SDK to detect and analyze human faces in images.

> **Note**: You can choose to use the SDK for either **C#** or **Python**. In the steps below, perform the actions appropriate for your preferred language.

### Prepare the application configuration

1. In the Azure portal, use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment. The cloud shell provides a command line interface in a pane at the bottom of the Azure portal.

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
   cd mslearn-ai-vision/Labfiles/face/python/face-api
   ls -a -l
    ```

    **C#**

    ```
   cd mslearn-ai-vision/Labfiles/face/c-sharp/face-api
   ls -a -l
    ```

    The folder contains application configuration and code files for your app. It also contains an **/images** subfolder, which contains some image files for your app to analyze.

1. Install the Azure AI Vision SDK package and other required packages by running the appropriate commands for your language preference:

    **Python**

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install dotenv pillow matplotlib azure-ai-vision-face==1.0.0b2
    ```

    **C#**

    ```
   dotnet add package Azure.AI.Vision.Face -v 1.0.0-beta.2
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

### Add code to create a Face API client

1. In the cloud shell command line, enter the following command to open the code file for the client application:

    **Python**

    ```
   code analyze-faces.py
    ```

    **C#**

    ```
   code Program.cs
    ```

    > **Tip**: You might want to maximize the cloud shell pane and move the split-bar between the command line cosole and the code editor so you can see the code more easily.

1. In the code file, find the comment **Import namespaces**, and add the following code to import the namespaces you will need to use the Azure AI Vision SDK:

    **Python**

    ```python
   # Import namespaces
   from azure.ai.vision.face import FaceClient
   from azure.ai.vision.face.models import FaceDetectionModel, FaceRecognitionModel, FaceAttributeTypeDetection03
   from azure.core.credentials import AzureKeyCredential
    ```

    **C#**

    ```C#
   // Import namespaces
   using Azure.AI.Vision.Face;
    ```

1. In the **Main** function, note that the code to load the configuration settings has been provided. Then find the comment **Authenticate Face client** and add the following code to create and authenticate a **FaceClient** object:

  **Python**

    ```python
   # Authenticate Face client
   face_client = FaceClient(
        endpoint=cog_endpoint,
        credential=AzureKeyCredential(cog_key)
   )
    ```

    **C#**

    ```C#
   // Authenticate Face client
   faceClient = new FaceClient(
        new Uri(cogSvcEndpoint),
        new AzureKeyCredential(cogSvcKey));
    ```

1. In the **Main** function, under the code you just added, note that the code calls the **DetectFaces** function to detect faces in the image. This function is only partially implemented - you will add code to it in the remainder of this exercise.

### Add code to detect and analyze faces

1. In the code file for your application, in the **DetectFaces** function, find the comment **Specify facial features to be retrieved** and add the following code:

    **Python**

    ```python
   # Specify facial features to be retrieved
   features = [FaceAttributeTypeDetection03.HEAD_POSE,
                FaceAttributeTypeDetection03.BLUR,
                FaceAttributeTypeDetection03.MASK]
    ```

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

1. In the **DetectFaces** function, under the code you just added, find the comment **Get faces** and add the following code:

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

1. Examine the code you added to the **DetectFaces** function. It analyzes an image file and detects any faces it contains, including attributes for head pose, blur, and the presence of mask. The details of each face are displayed, including a unique face identifier that is assigned to each face; and the location of the faces is indicated on the image using a bounding box.
1. Save your changes (*CTRL+S*) but keep the code editor open in case you need to fix any typo's.

1. Resize the panes so you can see more of the console, then enter the following command to run the program with the argument *images/face1.jpg*:

    **Python**

    ```
   python analyze-faces.py images/face1.jpg
    ```

    **C#**

    ```
   dotnet run images/face1.jpg
    ```

    The app runs and analyzes the following image:

    ![Photograph of a statue of a person.](../media/face1.jpg)

1. Observe the output, which should include the ID and attributes of each face detected. 
1. Note that an image file named **detected_faces.jpg** is also generated. Use the (Azure cloud shell-specific) **download** command to download it:

    ```
   download detected_faces.jpg
    ```

    The download command creates a popup link at the bottom right of your browser, which you can select to download and open the file. The image should look simlar to this:

    ![An image with the text highlighted.](../media/detected_faces.jpg)

1. Run the program again, this time specifying the parameter *images/face2.jpg* to extract text from the following image:

    ![Image of another persn.](../media/face2.jpg)

    **Python**

    ```
   python analyze-faces.py images/face2.jpg
    ```

    **C#**

    ```
   dotnet run images/face2.jpg
    ```

1. Download and view the resulting **detected_faces.jpg** file:

    ```
   download detected_faces.jpg
    ```

1. Run the program one more time, this time specifying the parameter *images/faces.jpg* to extract text from this image:

    ![Photograph of both people.](../media/faces.jpg)

    **Python**

    ```
   python analyze-faces.py images/faces.jpg
    ```

    **C#**

    ```
   dotnet run images/faces.jpg
    ```

1. Download and view the resulting **detected_faces.jpg** file:

    ```
   download detected_faces.jpg
    ```

## Clean up resources

If you've finished exploring Azure AI Vision, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs:

1. Open the Azure portal at `https://portal.azure.com`, and in the top search bar, search for the resources you created in this lab.

1. On the resource page, select **Delete** and follow the instructions to delete the resource. Alternatively, you can delete the entire resource group to clean up all resources at the same time.
