# Lab B — Solution (complete code)

This folder contains **finished, working versions** of every code file learners write in
*Generate images and video with AI*. Use it to unblock a stuck learner, verify expected behavior,
or run the whole scenario end to end.

All tasks share a **single** `Python/` folder (one virtual environment, one `.env`), exactly
like the starter code learners work in:

```
Solution/
└─ Python/
   ├─ image_client.py       # Task 1 — generate images from a prompt, decode b64_json, save to images/
   ├─ video_from_text.py    # Task 2 — create a video job from text, poll it, download it
   ├─ video_from_image.py   # Task 3 — animate a reference image, then remix the finished video
   │   └─ reference.png     #   Task 3 — the still used as the video's first frame
   ├─ requirements.txt
   └─ .env.example
```

Every task uses the OpenAI Python SDK's `OpenAI` client pointed at the Azure OpenAI v1 endpoint,
authenticated with `DefaultAzureCredential` + `get_bearer_token_provider`. The difference between
the tasks is the *shape* of the work:

- **Task 1** is synchronous — `client.images.generate(...)` returns the base64 image immediately.
- **Tasks 2 and 3** are asynchronous — `client.videos.create(...)` returns a job, and the code polls
  `client.videos.retrieve(...)` until the status is terminal before calling
  `client.videos.download_content(...)`.

Task 3 reuses Task 2's polling and download helpers verbatim; they ship **already implemented** in
the starter file so that task can focus on `input_reference` and `client.videos.remix(...)`.

---

## Setup helpers and modular (per-task) labs

This lab can be completed end to end **or one task at a time**. Two things make that possible:

- **Per-task instruction pages** — `Instructions/Exercises/Consolidated/B0-getting-started.md`
  (shared setup) plus `B1`–`B3` (one page per task). Each task page tells a standalone learner
  exactly what it needs and how to fast-forward.
- **Setup script** in `Labfiles/B-generate-images-and-video-with-ai/setup/`:
  - `check_env.py` — run it from the starter `Python/` folder as `python ../setup/check_env.py --task N` to preflight-check that `.env` has the keys task *N* needs.

The script runs from the starter `Python/` folder and reads the shared `Python/.env`.

---

## What YOU must do to run this solution (the agent can't do these for you)

Everything below requires an Azure subscription and interactive sign-in, so it can't be
automated in the repo. Do these once, then run each task.

### 1. Azure / Microsoft Foundry setup
1. Have an **Azure subscription** with access to **Microsoft Foundry**.
2. Create (or open) a **Foundry project** and copy its **Azure OpenAI endpoint** (not the project endpoint).
3. **Deploy `gpt-image-2`** for Task 1 and note the deployment name.
4. **Deploy `sora-2`** for Tasks 2 and 3 and note the deployment name. Access to video generation
   models is restricted — the subscription may need to be registered before `sora-2` can be deployed.
5. Make sure your signed-in identity has an appropriate role (for example **Azure AI User**) on the resource.

### 2. Sign in locally
```
az login
```
Sign in with the same account that has access to the project. Every task authenticates with
`DefaultAzureCredential`, so a missing or expired `az login` is the most common reason a task
fails at run time.

### 3. Set up the environment once (shared by all tasks)
From the `Python/` folder:
```
python -m venv labenv
.\labenv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
```
Then copy `.env.example` to `.env` and fill in the values:
- `OPENAI_ENDPOINT` — every task; must end with `/openai/v1/`
- `IMAGE_MODEL_DEPLOYMENT_NAME` — Task 1
- `VIDEO_MODEL_DEPLOYMENT_NAME` — Tasks 2 and 3

> If you hit `AttributeError: 'OpenAI' object has no attribute 'videos'`, run
> `pip install openai --upgrade` — `client.videos` needs a recent SDK release.

### 4. Run each task
All commands run from the single `Python/` folder:

| Task | Command | What you get |
|------|---------|--------------|
| 1 | `python image_client.py` | Prompts you for image briefs in a loop; each generated image is saved to `images/image_N.png` |
| 2 | `python video_from_text.py` | Creates one video from a text prompt, prints status while polling, saves `original_video.mp4` |
| 3 | `python video_from_image.py` | Animates `reference.png` into `image_based_video.mp4`, then remixes it into `remixed_video.mp4` |

Tasks 2 and 3 take minutes, not seconds — 1 to 5 minutes per video, and Task 3 generates two.

---

## Notes on the SDK surface

- **Auth scope.** All calls use the `https://ai.azure.com/.default` scope with
  `get_bearer_token_provider`, which is the scope documented for the v1 API. The older
  `https://cognitiveservices.azure.com/.default` scope is legacy.
- **`api_key=token_provider()`.** The token provider must be **called** — passing the function
  object itself (`api_key=token_provider`) fails, because the SDK expects a string.
- **Video parameters.** `size` takes strings such as `"1280x720"` and `"720x1280"`; `seconds` takes
  4, 8, or 12. Reference images must match the requested `size`.

## Quick sanity checks that DON'T need Azure
- `python -m py_compile <file>` — all solution files compile.
- From the **starter** `Python/` folder (not `Solution/Python/`): `python ../setup/check_env.py --task 1` reports exactly which `.env` keys are still missing.
