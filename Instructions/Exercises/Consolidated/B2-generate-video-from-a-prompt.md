---
lab:
    title: 'Task 2 – Generate video from a text prompt'
    description: 'Use Sora 2 in Microsoft Foundry to create a video generation job from a text prompt, poll the asynchronous job until it completes, and download the finished file.'
    level: 300
    concepts: 'video generation, Sora, asynchronous jobs, polling'
    islab: true
    status: 'draft'
---

# Task 2 — Generate video from a text prompt

*Part of the **Generate images and video with AI** lab. New here? Start with [Getting started](B0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project with a **video generation** model
> deployed, and the starter code. If you haven't already, complete
> [Getting started](B0-getting-started.md) to create your project, deploy `sora-2`, clone the code,
> and set `OPENAI_ENDPOINT` and `VIDEO_MODEL_DEPLOYMENT_NAME` in `Python/.env`. Then, from the
> `Labfiles/B-generate-images-and-video-with-ai` folder, verify you're ready:

```
python ../setup/check_env.py --task 2
```

> **Continuing from a previous task?** If you just finished Task 1 in the same `Python` folder,
> your project, virtual environment, and `az login` are already set — but Task 1 used a *different
> model*. Make sure you've deployed `sora-2` and set `VIDEO_MODEL_DEPLOYMENT_NAME` in your `.env`
> before you start, then go straight to **Write code to authenticate** below.

> **Note**: Access to video generation models is restricted — you may need to register your
> subscription before **sora-2** is available to deploy. Video generation typically takes 1 to 5
> minutes per video, so this task takes longer to run than it does to write.

---

Task 1 returned an image the instant you asked for it. Video doesn't work that way — a clip takes
minutes to render, so the API hands you a **job** instead of a result. In this task you'll write the
create → poll → download loop that turns a written brief into a finished Wide World Importers promo
clip on disk.

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
<summary>What is a long-running operation?</summary>
<div class="concept-body" markdown="1">

Some work takes far too long to finish inside a single HTTP request. Instead of making you wait,
the service accepts the work, gives you an **ID** immediately, and gets on with it in the
background. Your job is to check back — that's **polling**.

A video job moves through statuses like `queued` → `in_progress` → `completed`. Your loop keeps
retrieving the job until the status is one of the terminal values (`completed`, `failed`, or
`cancelled`), sleeping between checks so you're not hammering the service. Only once it's
`completed` can you download the file.

[Learn more →](https://learn.microsoft.com/azure/foundry/openai/concepts/video-generation)

</div>
</details>

Open the `Python` folder and activate the virtual environment from [Getting started](B0-getting-started.md) (`.\labenv\Scripts\Activate.ps1`), then continue below.

### Write code to authenticate

Open **video_from_text.py** and add code at each commented placeholder.

1. Review the code already in the file. Note that, unlike the other apps in this lab, the configuration and client live at **module level** (outside `main`) so that the helper functions further down the file can use the client too.

    > **Tip**: As you add code, be sure to maintain the correct indentation.

1. Find the comment **Add references** and add the following code for the necessary imports:

    ```python
    # Add references
    import time
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

### Write code to create the video job

1. In the **main** function, find the comment **Generate a video from a text prompt** and add the following code:

    ```python
    # Generate a video from a text prompt
    video = client.videos.create(
        model=model_deployment,
        prompt="A crate of fresh citrus fruit on a sunlit market stall, gentle camera push in",
        size="1280x720",
        seconds=4,
    )
    video = poll_video_status(video.id)
    ```

    `client.videos.create` returns as soon as the job is **accepted** — the `video` object you get
    back holds an ID and a status, not a finished film. The call to `poll_video_status` is what
    waits for the real thing.

    > **Tip**: `size` accepts values such as `"1280x720"` (landscape) and `"720x1280"` (portrait), and `seconds` accepts 4, 8, or 12. Shorter clips finish faster, so stick with 4 while you're testing.

### Write code to poll for completion

1. Find the comment **Poll video status until completion** and add the following code to complete the `poll_video_status` function:

    ```python
    # Poll video status until completion
    video = client.videos.retrieve(video_id)

    while video.status not in ["completed", "failed", "cancelled"]:
        print(f"Status: {video.status}. Waiting 20 seconds...")
        time.sleep(20)
        video = client.videos.retrieve(video_id)

    if video.status == "completed":
        print("Video successfully completed!")
    else:
        print(f"Video creation ended with status: {video.status}")

    return video
    ```

    Note the three terminal statuses. Checking for *all* of them — not just `completed` — is what
    stops the loop spinning forever when a job fails or is cancelled.

### Write code to download the result

1. Find the comment **Download the completed video** and add the following code to complete the `download_video` function:

    ```python
    # Download the completed video
    print(f"Downloading video {video_id}...")
    content = client.videos.download_content(video_id, variant="video")
    content.write_to_file(output_filename)
    print(f"Saved video to {output_filename}")
    ```

    The `variant="video"` argument asks for the video file itself; the service can also return other
    variants, such as a thumbnail.

1. Save the file (**Ctrl+S**).

### Run and test

1. In the terminal, make sure you're signed in and then run the app:

    ```
    az login
    ```

    ```
    python video_from_text.py
    ```

1. Observe the output as the application:
    - Creates a video job from your text prompt
    - Prints a status line every 20 seconds while it polls
    - Downloads the completed video

    > **Note**: Video generation typically takes 1 to 5 minutes. Be patient while waiting for the status to change to "completed".

1. When the application finishes, check your project folder for `original_video.mp4` and play it.

    > **Tip**: If generation ends with a `failed` status, the content filters may have rejected your prompt. Try a prompt with no people, no brands, and no copyrighted characters in it.

> ✅ **Checkpoint**: You've created an asynchronous video job, polled it to completion, and
> downloaded the result — the create/poll/download pattern that almost every long-running AI API
> follows.

When you're finished, enter `deactivate` to exit the virtual environment.

---

**Next (optional):** [Task 3 — Animate a reference image and remix it](B3-animate-a-reference-image.md)
