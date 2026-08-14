# Lab A — Solution (complete code)

This folder contains **finished, working versions** of every code file learners write in
*Analyze visual content with AI*. Use it to unblock a stuck learner, verify expected behavior, or
run the whole scenario end to end.

All tasks share a **single** `Python/` folder (one virtual environment, one `.env`), exactly
like the starter code learners work in:

```
Solution/
└─ Python/
   ├─ image_chat_url.py       # Task 1 — multimodal chat with an image from a public URL
   ├─ image_chat_local.py     # Task 2 — same app, image inlined from disk as a base64 data URL
   │   └─ mystery-fruit.jpeg  #   Task 2 — the local image the app reads
   ├─ analyze_image.py        # Task 3 — Azure AI Content Understanding analyzer client
   │   └─ images/             #   Task 3 — Wide World Importers asset library samples
   ├─ requirements.txt
   └─ .env.example
```

Tasks 1 and 2 use the **Responses API** through the OpenAI Python SDK's `OpenAI` client pointed at
the Azure OpenAI v1 endpoint — `client.responses.create(...)` with an `input_text` + `input_image`
content array. Task 3 uses a **different service**: `azure-ai-contentunderstanding`, where
`begin_analyze_binary(...)` submits raw image bytes to a schema-backed analyzer and returns the
same fields for every image.

---

## Setup helpers and modular (per-task) labs

This lab can be completed end to end **or one task at a time**. Two things make that possible:

- **Per-task instruction pages** — `Instructions/Exercises/Consolidated/A0-getting-started.md`
  (shared setup) plus `A1`–`A3` (one page per task). Each task page tells a standalone learner
  exactly what it needs and how to fast-forward.
- **Setup script** in `Labfiles/A-analyze-visual-content-with-ai/setup/`:
  - `check_env.py` — run it from the starter `Python/` folder as `python ../setup/check_env.py --task N` to preflight-check that `.env` has the keys task *N* needs.

The script runs from the starter `Python/` folder and reads the shared `Python/.env`.

---

## What YOU must do to run this solution (the agent can't do these for you)

Everything below requires an Azure subscription and interactive sign-in, so it can't be
automated in the repo. Do these once, then run each task.

### 1. Azure / Microsoft Foundry setup
1. Have an **Azure subscription** with access to **Microsoft Foundry**.
2. Create (or open) a **Foundry project** and copy its **Azure OpenAI endpoint** (not the project endpoint).
3. **Deploy a multimodal model** (for example `gpt-5.2`, or `gpt-4.1` / `gpt-4o` if quota is tight) and note the **deployment name**. Needed for Tasks 1 and 2 only.
4. For Task 3, create a **storage account** and then build an **image analyzer** in
   [Content Understanding Studio](https://contentunderstanding.ai.azure.com/) with two generated
   fields named exactly `Description` (String) and `Tags` (List of Strings). Note the analyzer name
   and the `https://<resource>.services.ai.azure.com/` endpoint.
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
- `OPENAI_ENDPOINT` — Tasks 1 and 2; must end with `/openai/v1/`
- `MODEL_DEPLOYMENT_NAME` — Tasks 1 and 2
- `CONTENT_UNDERSTANDING_ENDPOINT` — Task 3; the `services.ai.azure.com` resource endpoint
- `ANALYZER_ID` — Task 3; the name of the analyzer you built

### 4. Run each task
All commands run from the single `Python/` folder:

| Task | Command | What you get |
|------|---------|--------------|
| 1 | `python image_chat_url.py` | Console output: the model answers questions about an orange it reads from a public URL |
| 2 | `python image_chat_local.py` | Console output: the model identifies `mystery-fruit.jpeg` from disk, sent as a base64 data URL |
| 3 | `python analyze_image.py` | Console output: your analyzer returns a `Description` and a list of `Tags` for the image you pick |

---

## Notes on the SDK surface

- **Auth scope.** All Azure OpenAI calls use the `https://ai.azure.com/.default` scope with
  `get_bearer_token_provider`, which is the scope documented for the v1 API. The older
  `https://cognitiveservices.azure.com/.default` scope is legacy.
- **Content Understanding bytes vs URLs.** Analyzing bytes read from disk uses
  `begin_analyze_binary(analyzer_id=..., binary_input=<bytes>)`. The sibling `begin_analyze(...)`
  method takes `inputs=[AnalysisInput(url=...)]` and is for content already published at a URL —
  `AnalysisInput` has no `data=` parameter.
- **Field access.** In `azure-ai-contentunderstanding` 1.x, each field exposes a typed `.value`.
  A `Description` string field is `field.value`; a `Tags` array field is a list you iterate,
  reading each item's own `.value`.

## Quick sanity checks that DON'T need Azure
- `python -m py_compile <file>` — all solution files compile.
- From the **starter** `Python/` folder (not `Solution/Python/`): `python ../setup/check_env.py --task 1` reports exactly which `.env` keys are still missing.
