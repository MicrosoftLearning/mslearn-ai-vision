---
lab:
    title: 'Task 3 – Extract structured metadata with Content Understanding'
    description: 'Build an Azure AI Content Understanding image analyzer with a custom schema, then call it from Python to turn the Wide World Importers asset library into searchable descriptions and tags.'
    level: 300
    concepts: 'Azure AI Content Understanding, custom schemas, structured output, image metadata'
    islab: true
    status: 'draft'
---

# Task 3 — Extract structured metadata with Content Understanding

*Part of the **Analyze visual content with AI** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **Set up (start here):** This task needs the Foundry project and starter code from
> [Getting started](A0-getting-started.md), plus two things you'll create on this page: an Azure
> **storage account** and a Content Understanding **analyzer**. It does **not** need the chat model
> deployment from Tasks 1 and 2, and it doesn't reuse any code from them — you can start here cold.
> Once you've built your analyzer below, set `CONTENT_UNDERSTANDING_ENDPOINT` and `ANALYZER_ID` in
> `Python/.env`, then verify from the `Python` folder:

```
python ../setup/check_env.py --task 3
```

> **Continuing from a previous task?** If you just finished Task 1 or Task 2 in the same `Python`
> folder, your project, virtual environment, and `az login` are already set — skip the clone and
> the `pip install`, but you still need to complete **Create a storage account** and **Create an
> image analyzer** below, because this task uses a different service to the chat tasks.

---

The Wide World Importers marketing studio has thousands of photographs and almost no metadata.
Task 1 could tell one staff member what's in one picture — but you can't build a searchable
library on free-form paragraphs. In this task you'll define a **schema**, build an analyzer that
fills it in the same way for every image, and call that analyzer from Python.

<style>
/* "Ask Mika" just-in-time concept blocks */
details.concept { margin:.6rem 0 1rem; }
details.concept > summary { display:inline-block; cursor:pointer; list-style:none;
  font-size:.85em; font-weight:600; color:#6b4ba1; background:#6b4ba112;
  border:1px solid #6b4ba133; border-radius:999px; padding:.2em .7em; }
details.concept > summary::-webkit-details-marker { display:none; }
details.concept > summary::before { content:"Ask Mika: "; font-weight:700; }
details.concept > summary:hover { background:#6b4ba1; color:#fff; border-color:#6b4ba1; }
details.concept[open] > summary { border-bottom-left-radius:0; border-bottom-right-radius:0; }
details.concept .concept-body { border:1px solid #6b4ba133; border-top:none;
  border-radius:0 8px 8px 8px; padding:.6rem .9rem; background:#6b4ba108; font-size:.95em; }
</style>

<details markdown="1" class="concept">
<summary>What is Azure AI Content Understanding?</summary>
<div class="concept-body" markdown="1">

**Azure AI Content Understanding** in Foundry Tools uses generative AI to interpret unstructured
content — documents, images, audio, and video — and return output that follows a **schema you
define**. You describe the fields you want (`Description`, `Tags`, and so on), Content
Understanding builds an **analyzer** for that schema, and every file you send back through it comes
out shaped the same way.

That predictability is the whole point. A chat model gives you a different paragraph every time; an
analyzer gives you the same fields every time, which is what you need to index, filter, and search
a library at scale.

[Learn more →](https://learn.microsoft.com/azure/ai-services/content-understanding/overview)

</div>
</details>

## Create an Azure storage account

Content Understanding needs somewhere to hold the content assets you analyze.

1. In a new browser tab, open the [Azure portal](https://portal.azure.com) at `https://portal.azure.com` and browse to the resource group where you created your Foundry project resource.

    The resource group should contain your Foundry resource and the project you created.

1. Create a new **Storage account** resource in the resource group, with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *The resource group containing your Foundry resource*
    - **Storage account name**: *A unique name for your storage account*
    - **Region**: *The same region as your Foundry resource*
    - **Preferred storage type**: Azure Blob Storage or Azure Data Lake Storage Gen 2
    - **Performance**: Standard
    - **Redundancy**: Locally-redundant storage (LRS)

1. Wait for your storage account to be created.

## Create an image analyzer

1. In a new browser tab, navigate to [Content Understanding Studio](https://contentunderstanding.ai.azure.com/home) at `https://contentunderstanding.ai.azure.com/home` and sign in using your Azure credentials if prompted.

1. At the top right, select the **Settings** icon to view your account settings for Azure AI Content Understanding.

1. On the **Setup Azure resource** page, select the **Add resource** button.

1. Select your subscription and the Foundry resources that match your Foundry project name.

1. Check the box for **Enable auto-deployment for required models if no default deployment available**.

1. Select **Next**, then select **Save** to deploy the required models.

    The deployment process can take several minutes. Once the models are deployed, the resource will appear under **Connected Azure AI Foundry Resources**. Note the name of the resource.

1. On the menu bar, select **Build**. Then use the **Create** button to create a new Content Understanding project with the following settings:
    - **Project name**: *A unique name for your image analysis project*
    - **Description**: `Wide World Importers asset library`
    - **Type of project**: Extract content and field with custom schema
    - **Advanced settings**: Ensure your Foundry resource and storage account are selected, a new container will be created, and a chat completion model such as `gpt-5.2` is selected.

1. When the project has been created, in a new browser tab, download the [lion.jpg](https://microsoftlearning.github.io/mslearn-ai-vision/Labfiles/A-analyze-visual-content-with-ai/lion.jpg) image from `https://microsoftlearning.github.io/mslearn-ai-vision/Labfiles/A-analyze-visual-content-with-ai/lion.jpg` and save it in a local folder.

    Then return to the Content Understanding project, and upload the **lion.jpg** file to the project.

1. When prompted to choose a template, select **Image Analysis** and ensure the schema is set to **Start from Scratch**. Then save the project.

1. After the image has been uploaded, in the **Schema** pane, use **Add new field** to add the following fields to the schema:

    | Field Name | Field Description | Value type | Method |
    |--|--|--|--|
    | `Description` | `Image description` | String | Generate |
    | `Tags` | `Image tags` | List of Strings | Generate |

    > **Important**: The field names are case-sensitive and your application code looks for these exact names. Use `Description` and `Tags` as written.

1. Save the changes to the schema.

1. Select **Run analysis** to run the analyzer on the image, and review the fields that are generated; which should include an accurate description and a collection of relevant tags for the image.

1. When you're satisfied that the analyzer has returned accurate values for the fields, use the **Build analyzer** button to publish an analyzer with a unique name and suitable description.

    > **Tip**: You'll need the name later to identify your analyzer in application code — it's your `ANALYZER_ID`.

1. When your analyzer has been built, jump to the analyzer list and verify it's listed there.

1. Select your analyzer in the list to open it, and then view the **Code Example** tab to see the code necessary to use your analyzer.

1. Review the Python code example, noting in the **main** function the **endpoint** for your Content Understanding resource; which should look similar to this:

    ```
    https://{your_foundry_resource}.services.ai.azure.com/
    ```

1. Under the code example, note that your **resource key** is available. You *can* use this in a client application to authenticate a connection to the endpoint; but in this exercise we're going to use Microsoft Entra ID authentication.

## Prepare the application configuration

1. If you haven't already, clone the repo and set up the `Python` folder as described in [Getting started](A0-getting-started.md).

1. Open the **.env** file in `Labfiles/A-analyze-visual-content-with-ai/Python` and set:

    - `CONTENT_UNDERSTANDING_ENDPOINT` — the resource endpoint you copied from the **Code Example** tab

    - `ANALYZER_ID` — the name you gave your analyzer when you selected **Build analyzer**

    > **Important**: Be sure to use the `https://{YOUR-RESOURCE-NAME}.services.ai.azure.com/` Foundry resource endpoint, <u>not</u> the project endpoint or the Azure OpenAI endpoint you used in Tasks 1 and 2.

    Save the file.

1. From the `Python` folder, confirm you're ready:

    ```
    python ../setup/check_env.py --task 3
    ```

### Write code to analyze images and generate descriptions

Open **analyze_image.py** and add code at each commented placeholder.

> **Tip**: As you add code, be sure to maintain the correct indentation.

1. Find the comment **Add references** and add the following code for the necessary imports:

    ```python
    # Add references
    from azure.ai.contentunderstanding import ContentUnderstandingClient
    from azure.ai.contentunderstanding.models import AnalysisResult
    from azure.core.exceptions import AzureError
    from azure.identity import DefaultAzureCredential
    ```

1. In the **main** function, note that code to get the configuration values from your environment file has been provided.

1. Find the comment **Set up Content Understanding client** and add the following code:

    ```python
    # Set up Content Understanding client
    credential = DefaultAzureCredential()
    client = ContentUnderstandingClient(
        endpoint=endpoint,
        credential=credential,
        api_version=api_version)
    ```

1. Note that code for the user to input a file number or quit the program has been provided, and that it reads the selected image into `file_bytes`.

1. Find the comment **Analyze the file** and add the following code:

    ```python
    # Analyze the file
    try:
        poller = client.begin_analyze_binary(
            analyzer_id=analyzer_id,
            binary_input=file_bytes,
        )
        result: AnalysisResult = poller.result()
    except AzureError as err:
        print(f"[Azure Error]: {err.message}")
        sys.exit(1)
    except Exception as ex:
        print(f"[Unexpected Error]: {ex}")
        sys.exit(1)

    for field_name, field in result.contents[0].fields.items():
        if field_name == "Description":
            print(f"{field_name}:\n{field.value}\n")
        elif field_name == "Tags":
            print(f"{field_name}:")
            for tag in field.value:
                print("  -", tag.value)
    ```

    This code submits the selected file data to your analyzer, polls for the results, and then
    displays the *Description* and *Tags* values that are returned. Note the two shapes:
    `Description` is a single string, so `field.value` is the text; `Tags` is a list, so
    `field.value` is a collection you iterate, reading each item's own `.value`.

    > **Note**: `begin_analyze_binary` is the method for analyzing raw bytes you've read from disk. There's a sibling method, `begin_analyze`, that takes `AnalysisInput(url=...)` when your content is already published at a URL.

1. Save the file (**Ctrl+S**).

### Test the app

1. In the terminal pane, make sure you're signed in to Azure:

    ```
    az login
    ```

    > **Note**: In most scenarios, just using *az login* will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the *--tenant* parameter. See [Sign into Azure interactively using the Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) for details.

1. Run the application:

    ```
    python analyze_image.py
    ```

1. When prompted, enter a number that corresponds to one of these images from the asset library:

    |![A giraffe.](../../../Labfiles/A-analyze-visual-content-with-ai/Python/images/image1.jpg) | ![An elephant.](../../../Labfiles/A-analyze-visual-content-with-ai/Python/images/image2.jpg) | ![A lion.](../../../Labfiles/A-analyze-visual-content-with-ai/Python/images/image3.jpg)
    |--|--|--|
    | 1 | 2 | 3 |

1. Observe the output, which should include a description of the selected image and a collection of appropriate tags.

1. Try the other images and notice that every result comes back with the *same two fields*, filled in differently — that consistency is what makes the library searchable.

1. When you're finished, enter any value other than 1, 2, or 3 to exit.

> ✅ **Checkpoint**: You've defined a schema, built an analyzer against it, and called it from
> Python to generate consistent metadata for a library of images.

When you're finished, enter `deactivate` to exit the virtual environment.

---

**Next:** You've completed the optional tasks. Head back to the [lab overview](A-analyze-visual-content-with-ai.md) for a summary and clean-up steps.
