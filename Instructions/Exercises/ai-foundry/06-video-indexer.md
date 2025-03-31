---
lab:
    title: 'Analyze Video with Video Indexer'
    module: 'Module 8 - Getting Started with Azure AI Vision'
---

# Analyze Video with Video Indexer

A large proportion of the data created and consumed today is in the format of video. **Azure AI Video Indexer** is an AI-powered service that you can use to index videos and extract insights from them.

> **Note**: From June 21st 2022, capabilities of Azure AI services that return personally identifiable information are restricted to customers who have been granted [limited access](https://docs.microsoft.com/azure/cognitive-services/cognitive-services-limited-access). Without getting limited access approval, recognizing people and celebrities with Video Indexer for this lab is not available. For more details about the changes Microsoft has made, and why - see [Responsible AI investments and safeguards for facial recognition](https://azure.microsoft.com/blog/responsible-ai-investments-and-safeguards-for-facial-recognition/).

## Upload a video to Video Indexer

First, you'll need to sign into the Video Indexer portal and upload a video.

> **Tip**: If the Video Indexer page is slow to load in the hosted lab environment, use your locally installed browser. You can switch back to the hosted VM for the later tasks.

1. In your browser, open the Video Indexer portal at `https://www.videoindexer.ai`.
1. If you have an existing Video Indexer account, sign in. Otherwise, sign up for a free account and sign in using your Microsoft account (or any other valid account type). If you have difficulty signing in, try opening a private browser session.
1. In a new tab, download the Responsible AI video by visiting `https://aka.ms/responsible-ai-video`. Save the file.
1. In Video Indexer, select the **Upload** option. Then select the option to **Browse for files**, select the downloaded video, and click **Add**. Change the default name to **Responsible AI**, review the default settings, select the checkbox to verify compliance with Microsoft's policies for facial recognition, and upload the file.
1. After the file has uploaded, wait a few minutes while Video Indexer automatically indexes it.

> **Note**: In this exercise, we're using this video to explore Video Indexer functionality; but you should take the time to watch it in full when you've finished the exercise as it contains useful information and guidance for developing AI-enabled applications responsibly! 

## Review video insights

The indexing process extracts insights from the video, which you can view in the portal.

1. In the Video Indexer portal, when the video is indexed, select it to view it. You'll see the video player alongside a pane that shows insights extracted from the video.

    > **Note**: Due to the limited access policy to protect individuals identities, you may not see names when you index the video.

![Video Indexer with a video player and Insights pane](../media/video-indexer-insights.png)

1. As the video plays, select the **Timeline** tab to view a transcript of the video audio.

![Video Indexer with a video player and Timeline pane showing the video transcript.](../media/video-indexer-transcript.png)

1. At the top right of the portal, select the **View** symbol (which looks similar to &#128455;), and in the list of insights, in addition to **Transcript**, select **OCR** and **Speakers**.

![Video Indexer view menu with Transcript, OCR, and Speakers selected](../media/video-indexer-view-menu.png)

1. Observe that the **Timeline** pane now includes:
    - Transcript of audio narration.
    - Text visible in the video.
    - Indications of speakers who appear in the video. Some well-known people are  automatically recognized by name, others are indicated by number (for example *Speaker #1*).
1. Switch back to the **Insights** pane and view the insights show there. They include:
    - Individual people who appear in the video.
    - Topics discussed in the video.
    - Labels for objects that appear in the video.
    - Named entities, such as people and brands that appear in the video.
    - Key scenes.
1. With the **Insights** pane visible, select the **View** symbol again, and in the list of insights, add **Keywords** and **Sentiments** to the pane.

    The insights found can help you determine the main themes in the video. For example, the **topics** for this video show that it is clearly about technology, social responsibility, and ethics.

## Search for insights

You can use Video Indexer to search the video for insights.

1. In the **Insights** pane, in the **Search** box, enter *Bee*. You may need to scroll down in the Insights pane to see results for all types of insight.
1. Observe that one matching *label* is found, with its location in the video indicated beneath.
1. Select the beginning of the section where the presence of a bee is indicated, and view the video at that point (you may need to pause the video and select carefully - the bee only appears briefly!)
1. Clear the **Search** box to show all insights for the video.

![Video Indexer search results for Bee](../media/video-indexer-search.png)

## Clone the repository for this course

You'll run scripts for this lab using Cloud Shell from the Azure Portal. The files have been provided in a GitHub repo.

> **Tip**: If you have already cloned the **mslearn-ai-vision** repo recently, you can skip this task. Otherwise, follow these steps to clone it to your development environment.

1. Open the Azure portal at `https://portal.azure.com`, and sign in using the Microsoft account associated with your Azure subscription.
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
   cd mslearn-ai-vision/Labfiles/06-video-indexer
    ```

## Use Video Indexer widgets

The Video Indexer portal is a useful interface to manage video indexing projects. However, there may be occasions when you want to make the video and its insights available to people who don't have access to your Video Indexer account. Video Indexer provides widgets that you can embed in a web page for this purpose.

1. Using the `ls` command, you can view the contents of the **06-video-indexer** folder. Note that it contains a **analyze-video.html** file. This is a basic HTML page to which you will add the Video Indexer **Player** and **Insights** widgets.
1. Enter the following command to edit the file:

    ```
   code analyze-video.html
    ```

    The file is opened in a code editor.
   
1. Note the reference to the **vb.widgets.mediator.js** script in the header - this script enables multiple Video Indexer widgets on the page to interact with one another.
1. In the Video Indexer portal, return to the **Media files** page and open your **Responsible AI** video.
1. Under the video player, select **&lt;/&gt; Embed** to view the HTML iframe code to embed the widgets.
1. In the **Share and Embed** dialog box, select the **Player** widget, set the video size to 560 x 315, and then copy the embed code to the clipboard.
1. In the Azure portal, in the **analyze-video.html** file, paste the copied code under the comment **&lt;-- Player widget goes here -- &gt;**.
1. Back in the **Share and Embed** dialog box, select the **Insights** widget and then copy the embed code to the clipboard. Then close the **Share and Embed** dialog box, switch back to Azure portal, and paste the copied code under the comment **&lt;-- Insights widget goes here -- &gt;**.
1. After editing the file, within the code editor, use the **CTRL+S** command or **Right-click > Save** to save your changes and then use the **CTRL+Q** command or **Right-click > Quit** to close the code editor while keeping the cloud shell command line open.
1. In the cloud shell toolbar, select **Upload/Download files** and then **Download**. In the new dialog box, enter the following file path and select **Download**:

    ```
    mslearn-ai-vision/Labfiles/06-video-indexer/analyze-video.html
    ```

1. Open **analyze-video.html** in your browser to see the web page.
1. Experiment with the widgets, using the **Insights** widget to search for insights and jump to them in the video.

![Video Indexer widgets in a web page](../media/video-indexer-widgets.png)

## Use the Video Indexer REST API

Video Indexer provides a REST API that you can use to upload and manage videos in your account.

### Get your API details

To use the Video Indexer API, you need some information to authenticate requests:

1. In the Video Indexer portal, expand the left pane and select the **Account settings** page.
1. Note the **Account ID** on this page - you will need it later.
1. Open a new browser tab and go to the Video Indexer developer portal at `https://api-portal.videoindexer.ai`, signing in using the credentials for your Video Indexer account.
1. On the **Profile** page, view the **Subscriptions** associated with your profile.
1. On the page with your subscription(s), observe that you have been assigned two keys (primary and secondary) for each subscription. Then select **Show** for any of the keys to see it. You will need this key shortly.

### Use the REST API

Now that you have the account ID and an API key, you can use the REST API to work with videos in your account. In this procedure, you'll use a PowerShell script to make REST calls; but the same principles apply with HTTP utilities such as cURL or Postman, or any programming language capable of sending and receiving JSON over HTTP.

All interactions with the Video Indexer REST API follow the same pattern:

- An initial request to the **AccessToken** method with the API key in the header is used to obtain an access token.
- Subsequent requests use the access token to authenticate when calling REST methods to work with videos.

1. In the cloud shell, use the command `code get-videos.ps1` to open the PowerShell script.
1. In the PowerShell script, replace the **YOUR_ACCOUNT_ID** and **YOUR_API_KEY** placeholders with the account ID and API key values you identified previously.
1. Observe that the *location* for a free account is "trial". If you have created an unrestricted Video Indexer account (with an associated Azure resource), you can change this to the location where your Azure resource is provisioned (for example "eastus").
1. Review the code in the script, noting that invokes two REST methods: one to get an access token, and another to list the videos in your account.
1. Save your changes, close the code editor and then run `./get-videos.ps1` to execute the script.
1. View the JSON response from the REST service, which should contain details of the **Responsible AI** video you indexed previously.

## More information

Recognition of people and celebrities is still available, but following the [Responsible AI Standard](https://aka.ms/aah91ff) those are restricted behind a Limited Access policy. These features include facial identification and celebrity recognition. To learn more and apply for access, see the [Limited Access for Azure AI Services](https://docs.microsoft.com/azure/cognitive-services/cognitive-services-limited-access).

For more information about **Video Indexer**, see the [Video Indexer documentation](https://learn.microsoft.com/azure/azure-video-indexer/).
