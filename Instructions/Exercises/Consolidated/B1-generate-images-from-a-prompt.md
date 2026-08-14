---
lab:
    title: 'Task 1 – Generate images from a prompt'
    description: 'Use a gpt-image model in Microsoft Foundry to generate Wide World Importers campaign artwork from text prompts, decode the base64 response, and save each image to disk.'
    level: 300
    concepts: 'image generation, gpt-image, base64 responses'
    islab: true
    status: 'draft'
---

# Task 1 — Generate images from a prompt

*Part of the **Generate images and video with AI** lab. New here? Start with [Getting started](B0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project with an image generation model
> deployed, and the starter code. If you haven't already, complete
> [Getting started](B0-getting-started.md) to create your project, deploy `gpt-image-2`, clone the
> code, and set `OPENAI_ENDPOINT` and `IMAGE_MODEL_DEPLOYMENT_NAME` in `Python/.env`. Then, from the
> `Labfiles/B-generate-images-and-video-with-ai` folder, verify you're ready:

```
python ../setup/check_env.py --task 1
```

> **Continuing from a previous task?** If you just finished an earlier task in the same
> `Python` folder, your project, virtual environment, and `.env` are already set — go
> straight to **Write code to connect to your model** below.

---

The Wide World Importers marketing studio needs seasonal artwork faster than a photo shoot can
deliver it. In this task you'll build the tool that turns a written brief into a saved image file:
you type a prompt, the model returns the picture, and your code decodes and stores it.

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
<summary>Why does the response contain text instead of an image?</summary>
<div class="concept-body" markdown="1">

The `gpt-image` models always return the picture as **base64-encoded data** in a `b64_json` field —
never as a link you download. Base64 is a way of representing binary data (the PNG bytes) using
only text characters, so it can travel inside a JSON response.

That's why your code has three steps rather than one: read `b64_json` out of the response, decode
it back into bytes with `base64.b64decode`, and write those bytes to a `.png` file.

[Learn more →](https://learn.microsoft.com/azure/foundry/openai/how-to/dall-e)

</div>
</details>

Open the `Python` folder and activate the virtual environment from [Getting started](B0-getting-started.md) (`.\labenv\Scripts\Activate.ps1`), then continue below.

### Write code to connect to your model

Open **image_client.py** and add code at each commented placeholder.

1. Review the code already in the file. It contains:
    - Some **import** statements.
    - A `main` function that loads your configuration and then loops asking you for a prompt until you type `quit`.
    - A `save_image` function, already written, that creates an `images` folder and writes the decoded bytes to a `.png` file.

    > **Tip**: As you add code, be sure to maintain the correct indentation.

1. Find the comment **Add references** and add the following code to reference the namespaces in the libraries you installed previously:

    ```python
    # Add references
    from dotenv import load_dotenv
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    from openai import OpenAI
    import base64
    ```

1. In the **main** function, under the comment **Get configuration settings**, note that the code loads the endpoint and model deployment name values you defined in the configuration file.

1. Under the comment **Initialize the client**, add the following code to connect to your model using the Azure credentials you're currently signed in with:

    ```python
    # Initialize the client
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://ai.azure.com/.default"
    )

    client = OpenAI(
        base_url=endpoint,
        api_key=token_provider(),
    )
    ```

### Write code to generate and save an image

1. Note that the code includes a loop to allow a user to input a prompt until they enter "quit". In the loop section, under the comment **Generate an image**, add the following code to submit the prompt and retrieve the data for the generated image from your model:

    ```python
    # Generate an image
    img = client.images.generate(
        model=model_deployment,
        prompt=input_text,
        n=1
    )

    json_response = json.loads(img.model_dump_json())
    image_data = json_response["data"][0].get("b64_json")
    image_data_in_bytes = base64.b64decode(image_data)
    ```

    > **Note**: The gpt-image model returns the generated image as base64-encoded data in `b64_json`. The `n=1` parameter asks for a single image; you can request up to 10.

1. Note that the code in the remainder of the **main** function passes the image data and a filename to the provided `save_image` function, which writes the decoded bytes out as a .png file.

1. Save the file (**Ctrl+S**).

### Run the client application

1. In the terminal, make sure you're signed in and then run the app:

    ```
    az login
    ```

    ```
    python image_client.py
    ```

1. When prompted, enter a request for an image, such as:

    ```
    Create a bright poster of a crate of imported citrus fruit at a street market
    ```

    After a moment or two, the app should confirm that the image has been saved. The image appears
    in the `images` folder in your project directory with the name `image_1.png`.

1. Try a few more prompts to refine the campaign look. When you're finished, enter `quit` to exit the program.

    > **Note**: In this simple app, we haven't implemented logic to retain conversation history; so the model will treat each prompt as a new request with no context of the previous prompt.

1. Review the generated images in the `images` folder.

> ✅ **Checkpoint**: You've generated images from text prompts and saved them to disk. That's the
> Core of this lab — and notice how fast it was, because image generation returns synchronously.
> The optional tasks move to video, where results take minutes and the code has to be shaped
> differently.

When you're finished, enter `deactivate` to exit the virtual environment.

---

**Next (optional):** [Task 2 — Generate video from a text prompt](B2-generate-video-from-a-prompt.md) · [Task 3 — Animate a reference image and remix it](B3-animate-a-reference-image.md)
