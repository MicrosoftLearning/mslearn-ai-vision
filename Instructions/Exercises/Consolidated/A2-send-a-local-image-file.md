---
lab:
    title: 'Task 2 – Send a local image file'
    description: 'Base64-encode an image from disk into a data URL so a multimodal model can read a picture that isn''t published anywhere.'
    level: 200
    concepts: 'image input, base64 data URLs, Responses API'
    islab: true
    status: 'draft'
---

# Task 2 — Send a local image file

*Part of the **Analyze visual content with AI** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project with a multimodal model deployed, and
> the starter code. If you haven't already, complete [Getting started](A0-getting-started.md) to
> create your project, deploy the model, clone the code, and set `OPENAI_ENDPOINT` and
> `MODEL_DEPLOYMENT_NAME` in `Python/.env`. Then, from the
> `Labfiles/A-analyze-visual-content-with-ai` folder, verify you're ready:

```
python ../setup/check_env.py --task 2
```

> **Continuing from a previous task?** If you just finished Task 1 in the same `Python` folder,
> your project, virtual environment, and `.env` are already set — go straight to
> **Write code to upload a local image file** below. This task uses its own file,
> `image_chat_local.py`, so your Task 1 code stays intact for comparison.

---

Task 1 pointed the model at a picture on a public website. That's fine for a catalog photo, but
the shots that actually arrive at Wide World Importers come from a phone at the loading dock —
they're on someone's disk, not on the internet. In this task you'll send an image the model can't
reach by URL, by encoding the file itself into the request.

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
<summary>What is a data URL?</summary>
<div class="concept-body" markdown="1">

A **data URL** carries the file's bytes inside the URL itself instead of pointing at a location.
It looks like `data:image/jpeg;base64,/9j/4AAQSkZJRg...` — a MIME type, the word `base64`, and then
the whole file encoded as text.

That matters here because the `input_image` part expects an `image_url`, and the service has to be
able to *fetch* a normal link. A file on your laptop isn't fetchable, so you inline it instead. The
API call is otherwise identical to Task 1 — only the value of `image_url` changes.

[Learn more →](https://learn.microsoft.com/azure/foundry/openai/how-to/responses)

</div>
</details>

Open the `Python` folder and activate the virtual environment from [Getting started](A0-getting-started.md) (`.\labenv\Scripts\Activate.ps1`), then continue below.

### Write code to get an OpenAI chat client

Open **image_chat_local.py** and add code at each commented placeholder.

1. Review the code already in the file. It's the same produce assistant shell as Task 1, and it already imports `base64` and `Path` for you.

    > **Tip**: As you add code, keep the indentation aligned with the comments.

1. At the top of the file, find the comment **Add references** and add the namespaces you'll need:

    ```python
    # Add references
    from openai import OpenAI
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    ```

1. Find the comment **Create an OpenAI client**, and add the following code:

    ```python
    # Create an OpenAI client
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
    client = OpenAI(
        base_url=openai_endpoint,
        api_key=token_provider()
    )
    ```

### Write code to upload a local image file

The starter folder includes **mystery-fruit.jpeg** — a photograph of a fruit that isn't published anywhere:

![A photo of a dragon fruit.](../../media/mystery-fruit.jpeg)

1. In the loop section, find the comment **Get a response to image input** and add the following code to read the file, encode it, and send it:

    ```python
    # Get a response to image input
    image_path = Path("mystery-fruit.jpeg")
    image_format = "jpeg"
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    data_url = f"data:image/{image_format};base64,{image_data}"

    response = client.responses.create(
        model=model_deployment,
        input=[
            {"role": "developer", "content": system_message},
            {"role": "user", "content": [
                {"type": "input_text", "text": prompt},
                {"type": "input_image", "image_url": data_url}
            ]}
        ]
    )
    print(response.output_text)
    ```

    Compare this with Task 1: the request shape is identical. The only difference is that
    `image_url` now holds a `data:` URL built from the file's bytes rather than a link to a
    website.

1. Save the file (**Ctrl+S**).

### Run and test

1. In the terminal, make sure you're signed in and then run the app:

    ```
    az login
    ```

    ```
    python image_chat_local.py
    ```

1. When prompted, enter the following prompt:

    ```
    What is this fruit? What recipes could I use it in?
    ```

1. Review the response. The model should identify the fruit from the photo on disk and suggest
    recipes for it. Then enter `quit` to exit the program.

    > **Note**: Base64 encoding makes the request noticeably larger than a URL-based one. For very
    > large images, expect a slightly longer round trip.

> ✅ **Checkpoint**: You've sent a local image file to a multimodal model by inlining it as a data
> URL — the same technique you'd use for a photo captured in your own app.

When you're finished, enter `deactivate` to exit the virtual environment.

---

**Next (optional):** [Task 3 — Extract structured metadata with Content Understanding](A3-extract-structured-metadata.md)
