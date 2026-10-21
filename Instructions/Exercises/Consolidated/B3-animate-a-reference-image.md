---
lab:
    title: 'Task 3 – Animate a reference image and remix it'
    description: 'Use a still photograph as the first frame of a Sora 2 video, then remix the finished clip with a new creative direction instead of regenerating it from scratch.'
    level: 400
    concepts: 'video generation, reference images, remix, asynchronous jobs'
    islab: true
    status: 'draft'
---

# Task 3 — Animate a reference image and remix it

*Part of the **Generate images and video with AI** lab. New here? Start with [Getting started](B0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project with a **video generation** model
> deployed, and the starter code. If you haven't already, complete
> [Getting started](B0-getting-started.md) to create your project, deploy `sora-2`, clone the code,
> and set `OPENAI_ENDPOINT` and `VIDEO_MODEL_DEPLOYMENT_NAME` in `Python/.env`. Then, from the
> `Labfiles/B-generate-images-and-video-with-ai` folder, verify you're ready:

```
python ../setup/check_env.py --task 3
```

> **Continuing from a previous task?** If you just finished Task 2 in the same `Python` folder, your
> project, virtual environment, and `.env` are already set — go straight to **Write code to
> authenticate** below. You'll recognize the polling and download helpers: in this task they're
> **already written for you**, so you can focus on the two calls that are new.

> **Note**: This task generates **two** videos, and each typically takes 1 to 5 minutes. Expect the
> script to run for several minutes before it finishes.

---

Text prompts give you a new scene every time — which is a problem when the Wide World Importers
studio has already approved a product shot. In this task you'll pin the video to that existing
photograph by using it as the **first frame**, and then **remix** the finished clip to try a
different look without paying to generate it all over again.

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
<summary>What's the difference between a reference image and a remix?</summary>
<div class="concept-body" markdown="1">

They're two different ways of *not* starting from a blank page.

A **reference image** grounds a **new** job: you pass `input_reference=` a still, and the model uses
it as the video's opening frame, so the generated motion continues from a scene you already
approved.

A **remix** takes a **finished** video and re-renders it under new instructions. You pass the
existing `video_id` plus a prompt describing the change, and get a new video back. Because the
source clip is the starting point, you can iterate on lighting or color without re-describing the
whole scene.

> The reference image's resolution must match the video `size` you request — the supported
> combinations are `1280x720` and `720x1280`.

[Learn more →](https://learn.microsoft.com/azure/foundry/openai/concepts/video-generation)

</div>
</details>

Open the `Python` folder and activate the virtual environment from [Getting started](B0-getting-started.md) (`.\labenv\Scripts\Activate.ps1`), then continue below.

### Write code to authenticate

Open **video_from_image.py** and add code at each commented placeholder.

1. Review the code already in the file:
    - `reference.png` in the same folder is the still image you'll animate.
    - `poll_video_status` and `download_video` are **already implemented** — they're the same helpers as Task 2.
    - `generate_video_from_image` and `remix_video` are the two functions you'll complete.

    > **Tip**: As you add code, be sure to maintain the correct indentation.

1. Find the comment **Add references** and add the following code for the necessary imports:

    ```python
    # Add references
    from openai import OpenAI
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    ```

1. Find the comment **Get the token provider for Azure OpenAI authentication** and add the following code:

    ```python
    # Get the token provider for Azure OpenAI authentication
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://ai.azure.com/.default"
    )

    # Initialize the OpenAI client with the endpoint and token provider
    client = OpenAI(
        base_url=endpoint,
        api_key=token_provider(),
    )
    ```

### Write code to generate a video from a reference image

1. In the **main** function, find the comment **Generate a video from a reference image** and add the following code:

    ```python
    # Generate a video from a reference image
    video = generate_video_from_image(
        image_path="reference.png",
        prompt="The scene comes to life with gentle movement and ambient lighting",
        size="1280x720",
        seconds=4
    )
    ```

1. Further down the file, find the comment **Create the video with an image reference** and add the following code to complete the `generate_video_from_image` function:

    ```python
    # Create the video with an image reference
    video = client.videos.create(
        model=model_deployment,
        prompt=prompt,
        size=size,
        seconds=seconds,
        input_reference=open(image_path, "rb"),
    )
    ```

    This is the same `client.videos.create` call as Task 2, with one addition: `input_reference`
    takes an open file handle for the still image. Everything after it — the polling and the
    download — is unchanged, which is the point: grounding the job in an image doesn't change how
    you manage it.

    > **Note**: Accepted reference image types are JPEG, PNG, and WebP. Remember that Sora 2 rejects input images containing human faces.

### Write code to remix the finished video

1. Find the comment **Remix an existing video** and add the following code to complete the `remix_video` function:

    ```python
    # Remix an existing video
    video = client.videos.remix(
        video_id=video_id,
        prompt=prompt,
    )

    print(f"Remix started. New video ID: {video.id}")
    print(f"Initial status: {video.status}")

    # Poll for completion
    video = poll_video_status(video.id)
    return video
    ```

    A remix is just another job: it returns a **new** video ID with its own status, so it goes
    through exactly the same polling loop. Note that `main` passes the *first* video's ID in, and
    downloads the remixed result under a different filename.

1. Save the file (**Ctrl+S**).

### Run and test

1. In the terminal, make sure you're signed in and then run the app:

    ```
    az login
    ```

    ```
    python video_from_image.py
    ```

1. Observe the output as the application:
    - Creates a video job that starts from `reference.png`
    - Polls until it completes, then downloads it
    - Remixes that video with a warmer color palette
    - Polls the remix job and downloads the result

    > **Note**: This generates two videos in sequence, so allow several minutes for the script to finish.

1. When the application finishes, check your project folder for `image_based_video.mp4` and `remixed_video.mp4`.

1. Play both files and compare them with `reference.png`. The first video should open on the still
    image and move from there; the remix should keep that scene but shift its color palette.

    > **Tip**: If either job ends with a `failed` status, the content filters may have rejected the prompt or the reference image. Sora 2 rejects images containing human faces.

> ✅ **Checkpoint**: You've grounded a video generation job in an existing image and iterated on a
> finished video with a remix — two techniques that let a studio stay on-brand instead of rolling
> the dice on every render.

When you're finished, enter `deactivate` to exit the virtual environment.

---

**Next:** You've completed the optional tasks. Head back to the [lab overview](B-generate-images-and-video-with-ai.md) for a summary and clean-up steps.
