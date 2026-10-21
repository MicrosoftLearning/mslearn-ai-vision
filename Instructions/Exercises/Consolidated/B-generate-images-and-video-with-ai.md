---
lab:
    title: 'Generate images and video with AI'
    description: 'Build the Wide World Importers campaign studio: generate marketing images from text prompts with a gpt-image model, then produce and remix short promo videos with Sora 2. A modular lab you can complete end to end or one task at a time.'
    level: 300
    concepts: 'image generation, video generation, Sora, asynchronous jobs, responsible AI'
    duration: 30
    islab: true
    status: 'draft'
---

# Generate images and video with AI

**Difficulty** ▰▰▰▱▱ **L300**  (filled bars out of 5; **L100** beginner → **L500** expert)

Reading an image is one half of visual AI. *Making* one is the other. In this lab you'll build the
**Wide World Importers** campaign studio — generating marketing images from a written brief, then
producing short promo videos and remixing them without reshooting anything.

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
<summary>Why is video generation shaped so differently to image generation?</summary>
<div class="concept-body" markdown="1">

Generating an image takes seconds, so `client.images.generate(...)` simply **returns the image**.
Generating video takes minutes, so it can't work that way — instead you create a **job**, get an ID
back immediately, **poll** the job until its status becomes `completed`, and then **download** the
result as a separate step.

That create → poll → download rhythm is the single most important pattern in this lab. Once you
recognize it, most long-running AI APIs look familiar.

[Learn more →](https://learn.microsoft.com/azure/foundry/openai/concepts/video-generation)

</div>
</details>

**Your scenario:** you work at **Wide World Importers**, a specialty grocery importer that ships
unusual produce to supermarkets worldwide, and runs its own marketing studio. The studio needs
seasonal campaign artwork faster than a photo shoot can deliver it, and short social clips for
every product line. Across this lab you'll build the generation pipeline behind both.

You'll start with the **Core** task that gets you generating images as quickly as possible. From
there, a set of **Optional** tasks moves you into video.

> **Note**: Some of the technologies used in this exercise are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## What you'll learn

By completing the **Core** task of this exercise, you'll be able to:

- **Generate an image from a text prompt** with a `gpt-image` model, decode the base64 response,
  and save the result to disk.

The **Optional** tasks let you additionally:

- **Generate a video from a text prompt** with **Sora 2**, poll the asynchronous job until it
  finishes, and download the finished file.
- **Animate a reference image** by using a still photograph as the first frame, and **remix** an
  existing video with a new creative direction instead of regenerating it from scratch.

## How this lab is organized

This lab is **modular**. Each task is written to be completed **on its own, starting fresh** —
so you can pick a single task and do just that one. Every task also shares one starter folder,
one virtual environment, and one `.env`, so if you'd rather work straight through, you can.

1. **Start with [Getting started](B0-getting-started.md)** — create your Microsoft Foundry
   project, deploy the models you need, get the starter code, and set up your `.env`. Every task
   begins here; if you're doing the whole lab in one sitting, you only need to do this once.
2. **Do any task.** Each task lists the setup it needs so you can start it independently. If
   you're moving straight from the previous task, a short *"Continuing from a previous task?"*
   note at the top lets you skip the repeated setup and keep going.

## Lab at a glance

Complete the **Core** task first (about **30 minutes**) — it ends with a working image generation
app. Then expand any **Optional** tasks that interest you. The full lab, including all optional
tasks, takes about **1 hour 45 minutes**.

| Section | Task | Difficulty | Time |
| --- | --- | --- | --- |
| **Core** | [Task 1 – Generate images from a prompt](B1-generate-images-from-a-prompt.md) | ▰▰▰▱▱ L300 | ~30 min |
| *Optional* | [Task 2 – Generate video from a text prompt](B2-generate-video-from-a-prompt.md) | ▰▰▰▱▱ L300 | ~35 min |
| *Optional* | [Task 3 – Animate a reference image and remix it](B3-animate-a-reference-image.md) | ▰▰▰▰▱ L400 | ~40 min |

**Choosing your path** — pick the tasks that fit the time you have:

- **Core only (~30 min):** do Task 1.
- **Core + video (~1h 5m):** add **Task 2**, which introduces the create/poll/download job pattern.
- **Everything (~1h 45m):** add **Task 3**, which grounds generation in an existing image and
  iterates on a finished video.

> **Important**: Tasks 2 and 3 need access to a video generation model. Access to these models is
> restricted, and you may need to register your subscription before **sora-2** is available to
> deploy. If you can't deploy it, you can still complete the Core task in full.

## From instant results to long-running jobs

The three tasks build one idea at a time, and the shape of the code changes as they do:

- In **Task 1**, generation is **synchronous**: you call `client.images.generate(...)`, and the
  base64 image comes straight back in the response.
- In **Task 2**, generation becomes **asynchronous**: `client.videos.create(...)` returns a job, and
  you write the polling loop and download step yourself.
- In **Task 3**, you keep that same job pattern but change the *input* — a reference image becomes
  the first frame — and then feed a finished video back in as the input to a **remix**.

## Understand responsible AI considerations

Azure video generation models include built-in Responsible AI (RAI) protections to help ensure safe
and compliant use.

The Sora 2 model enforces several content restrictions:

- Only content suitable for audiences under 18
- Copyrighted characters and copyrighted music are rejected
- Real people — including public figures — cannot be generated
- Input images with faces of humans are currently rejected

Azure provides input and output moderation across all image and video generation models, along with
Azure-specific safeguards such as content filtering and abuse monitoring. These systems help detect
and prevent the generation or misuse of harmful, unsafe, or policy-violating content.

## Summary

Across this lab you:

- Generated **campaign images** from text prompts with a `gpt-image` model and saved the decoded
  results to disk.
- (Optionally) generated **video** from a text prompt with Sora 2, polling an asynchronous job to
  completion and downloading the file.
- (Optionally) used a **reference image** as a video's first frame, and **remixed** a finished video
  with a new creative direction.

Together these show how generative media moves from an instant response to a managed, long-running
pipeline — and how to iterate on a result rather than starting over.

## Clean up

If you're finished, delete the resources you created to avoid unnecessary Azure costs.

1. In the [Azure portal](https://portal.azure.com), navigate to the resource group that contains your Foundry resource.
1. On the toolbar, select **Delete resource group**, enter the resource group name, and confirm.
