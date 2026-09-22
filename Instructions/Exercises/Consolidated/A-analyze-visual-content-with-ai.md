---
lab:
    title: 'Analyze visual content with AI'
    description: 'Build the Wide World Importers visual analysis toolkit: a vision-enabled chat app that answers questions about produce photos, and an Azure AI Content Understanding analyzer that turns the campaign asset library into searchable structured metadata. A modular lab you can complete end to end or one task at a time.'
    level: 300
    concepts: 'multimodal chat, image input, Responses API, Azure AI Content Understanding, structured metadata'
    duration: 30
    islab: true
    status: 'draft'
---

# Analyze visual content with AI

**Difficulty** ▰▰▰▱▱ **L300**  (filled bars out of 5; **L100** beginner → **L500** expert)

A photograph is full of information that your systems can't use — until a model reads it for
you. In this lab you'll build the **Wide World Importers** visual analysis toolkit: first a chat
app that can *look* at a photo and answer questions about it, then an analyzer that turns a whole
image library into structured, searchable metadata.

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
<summary>What makes a model "multimodal"?</summary>
<div class="concept-body" markdown="1">

A **multimodal** model accepts more than one kind of input. A text-only model can only read the
words you send it; a multimodal model can accept an **image** alongside your text and reason about
both together. That means you can send a photo of an unfamiliar fruit and ask "what is this and
what would I cook with it?" in a single request — no separate image classifier, no fixed list of
labels.

[Learn more →](https://learn.microsoft.com/azure/foundry/openai/how-to/responses)

</div>
</details>

**Your scenario:** you work at **Wide World Importers**, a specialty grocery importer that ships
unusual produce to supermarkets worldwide, and runs its own marketing studio. Store staff regularly
receive crates of fruit nobody on the floor recognizes, and the studio's asset library has grown to
thousands of untagged photographs. Across this lab you'll build the AI that fixes both problems.

You'll start with the **Core** task that gets you to a working, vision-enabled app as quickly as
possible. From there, a set of **Optional** tasks lets you go deeper.

> **Note**: Some of the technologies used in this exercise are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## What you'll learn

By completing the **Core** task of this exercise, you'll be able to:

- **Send an image to a multimodal model** with the Responses API — combine an `input_text` prompt
  and an `input_image` reference in one request and read the model's answer.

The **Optional** tasks let you additionally:

- **Send a local image file** to the model by base64-encoding it into a data URL, instead of
  pointing at a public link.
- **Extract structured metadata** from images with **Azure AI Content Understanding** — define a
  schema of fields, build an analyzer against it, and call that analyzer from Python to get
  consistent descriptions and tags back.

## How this lab is organized

This lab is **modular**. Each task is written to be completed **on its own, starting fresh** —
so you can pick a single task and do just that one. Every task also shares one starter folder,
one virtual environment, and one `.env`, so if you'd rather work straight through, you can.

1. **Start with [Getting started](A0-getting-started.md)** — create your Microsoft Foundry
   project, deploy a model, get the starter code, and set up your `.env`. Every task begins
   here; if you're doing the whole lab in one sitting, you only need to do this once.
2. **Do any task.** Each task lists the setup it needs so you can start it independently. If
   you're moving straight from the previous task, a short *"Continuing from a previous task?"*
   note at the top lets you skip the repeated setup and keep going.

## Lab at a glance

Complete the **Core** task first (about **30 minutes**) — it ends with a working vision-enabled
chat app. Then expand any **Optional** tasks that interest you. The full lab, including all
optional tasks, takes about **1 hour 15 minutes**.

| Section | Task | Difficulty | Time |
| --- | --- | --- | --- |
| **Core** | [Task 1 – Ask a model about an image](A1-ask-a-model-about-an-image.md) | ▰▰▰▱▱ L300 | ~30 min |
| *Optional* | [Task 2 – Send a local image file](A2-send-a-local-image-file.md) | ▰▰▱▱▱ L200 | ~15 min |
| *Optional* | [Task 3 – Extract structured metadata with Content Understanding](A3-extract-structured-metadata.md) | ▰▰▰▱▱ L300 | ~30 min |

**Choosing your path** — pick the tasks that fit the time you have:

- **Core only (~30 min):** do Task 1.
- **Core + local files (~45 min):** add **Task 2**, which swaps the public image link for a file on disk.
- **Everything (~1h 15m):** add **Task 3**, which moves from conversational answers to structured,
  schema-driven metadata you can index and search.

## Two ways to read an image

The tasks in this lab deliberately show two different shapes of the same idea, and knowing when to
reach for each is the real lesson:

- In **Task 1** and **Task 2**, you send an image to a **chat model** and get a free-form,
  conversational answer. This is ideal when a human is asking the question, and every question is
  different — "what is this?", "is it ripe?", "what would I cook with it?".
- In **Task 3**, you send an image to a **Content Understanding analyzer** and get a **structured
  result** that always has the same fields. This is what you want when a *system* is asking, and
  you need thousands of images described the same way so you can index and search them.

Same photograph, two very different outputs — one for people, one for pipelines.

## Summary

Across this lab you:

- Sent an **image and a prompt** to a multimodal model with the Responses API and read the answer.
- (Optionally) **base64-encoded a local file** into a data URL so the model could read an image
  that isn't published anywhere.
- (Optionally) built a **Content Understanding analyzer** with a custom schema and called it from
  Python to generate consistent descriptions and tags for a library of images.

Together these cover both halves of visual analysis: answering a person's question about one
image, and describing a whole library consistently enough to search.

## Clean up

If you're finished, delete the resources you created to avoid unnecessary Azure costs.

1. In the [Azure portal](https://portal.azure.com), navigate to the resource group that contains your Foundry resource.
1. On the toolbar, select **Delete resource group**, enter the resource group name, and confirm.

> If you completed Task 3, the same resource group also contains the storage account you created
> for Content Understanding — deleting the resource group removes it too.
