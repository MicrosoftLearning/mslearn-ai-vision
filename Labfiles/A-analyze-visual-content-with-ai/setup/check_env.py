"""
Preflight check for the Wide World Importers visual analysis lab.

Each task in this lab can be completed on its own. Before you start a task,
run this script from the starter `Python` folder (the folder you opened in
VS Code) to confirm your .env file has everything that task needs:

    python ../setup/check_env.py --task 1

It never changes anything - it only reads your .env and tells you what (if
anything) is missing, so you can fix it before running the task.

Tasks and what they need:

    Task 1  (code)   OPENAI_ENDPOINT, MODEL_DEPLOYMENT_NAME
    Task 2  (code)   OPENAI_ENDPOINT, MODEL_DEPLOYMENT_NAME
    Task 3  (code)   CONTENT_UNDERSTANDING_ENDPOINT, ANALYZER_ID
"""

import argparse
import os
from pathlib import Path

def _parse_env_text(text):
    """Parse .env text the way python-dotenv does, reporting problems.

    Returns (values, problems). `problems` holds human-readable strings for
    conditions that break the learner's app even though the file "looks" fine.

    The important subtlety is quoting. A quoted value may run past the end of
    its line. python-dotenv discards the malformed statement and then resumes:
    if no later line closes the quote it drops only that setting, but if one
    does, the settings in between are swallowed into that value and lost.
    This parser reproduces that behaviour exactly: reporting a tidier result
    than the runtime would be a false positive.

    Escape handling is asymmetric, and measured against python-dotenv rather
    than assumed: double quotes decode the full set, single quotes decode only
    the delimiter and the backslash itself, and everything else stays literal.
    The close-quote SEARCH honors escapes for both styles.
    """
    double_escapes = {"a": "\a", "b": "\b", "f": "\f", "v": "\v",
                      "n": "\n", "r": "\r", "t": "\t",
                      '"': '"', "'": "'", "\\": "\\"}
    single_escapes = {"'": "'", "\\": "\\"}
    values = {}
    problems = []
    position = 0
    line_number = 1
    length = len(text)

    while position < length:
        end_of_line = text.find("\n", position)
        if end_of_line == -1:
            end_of_line = length
        statement_line = line_number
        statement_start = position
        stripped = text[position:end_of_line].strip()

        if not stripped or stripped.startswith("#"):
            position = end_of_line + 1
            line_number += 1
            continue

        offset = 0
        if stripped.startswith("export "):
            offset = text.index("export ", position) - position + len("export ")

        equals = text.find("=", position + offset, end_of_line)
        if equals == -1:
            # python-dotenv records a bare key with no "=" as None.
            values[stripped] = None
            position = end_of_line + 1
            line_number += 1
            continue

        key = text[position + offset:equals].strip()
        cursor = equals + 1
        while cursor < end_of_line and text[cursor] in " \t":
            cursor += 1

        if cursor < length and text[cursor] in "'\"":
            quote = text[cursor]
            decoder = double_escapes if quote == '"' else single_escapes
            cursor += 1
            value_start = cursor
            chars = []
            closed = False
            spanned_lines = False
            while cursor < length:
                char = text[cursor]
                if char == "\\" and cursor + 1 < length:
                    # A backslash escape hides the next character from the
                    # close-quote search for BOTH quote styles; the per-quote
                    # decoder above controls which pairs are actually decoded.
                    following = text[cursor + 1]
                    chars.append(decoder.get(following, "\\" + following))
                    cursor += 2
                    continue
                if char == quote:
                    closed = True
                    cursor += 1
                    break
                if char == "\n":
                    spanned_lines = True
                    line_number += 1
                chars.append(char)
                cursor += 1

            if not closed:
                # python-dotenv is escape-aware while a value PARSES, but raw
                # while RECOVERING from a quote that never closes: an escaped
                # quote on a later line still ends the broken statement. So if
                # the escape-aware scan found no close anywhere, retry raw.
                problems.append(
                    "line {0}: unterminated quote ({1})".format(
                        statement_line, key)
                )
                raw_close = text.find(quote, value_start)
                if raw_close == -1:
                    # Nothing closes it at all: drop this statement only.
                    position = end_of_line + 1
                else:
                    # Everything up to that raw quote is swallowed into the
                    # broken statement; resume on the following line.
                    after = text.find("\n", raw_close)
                    position = length if after == -1 else after + 1
                line_number = statement_line + text.count(
                    "\n", statement_start, position)
                continue

            rest_end = text.find("\n", cursor)
            if rest_end == -1:
                rest_end = length
            trailing = text[cursor:rest_end].strip()
            if spanned_lines:
                problems.append(
                    "line {0}: unterminated quote ({1})".format(
                        statement_line, key)
                )
            if trailing and not trailing.startswith("#"):
                # python-dotenv cannot parse the statement and drops it.
                pass
            else:
                values[key] = "".join(chars)
            position = rest_end + 1
            line_number += 1
        else:
            raw = text[cursor:end_of_line]
            values[key] = raw.split(" #")[0].strip()
            position = end_of_line + 1
            line_number += 1

    return values, problems


def _parse_env_file(path):
    """Minimal stand-in for python-dotenv's dotenv_values().

    Kept at module level (rather than hidden inside the ImportError branch) so it
    can be imported and differential-tested directly against python-dotenv.
    """
    try:
        # utf-8-sig transparently strips a UTF-8 BOM if the editor added one.
        with open(path, "r", encoding="utf-8-sig", newline="") as handle:
            text = handle.read()
    except OSError:
        return {}
    values, _ = _parse_env_text(text)
    return values


try:
    from dotenv import dotenv_values
except ModuleNotFoundError:
    # python-dotenv is installed into the lab's virtual environment, but this
    # preflight check is meant to run BEFORE 'pip install -r requirements.txt'
    # (and possibly outside the venv), so fall back to the stdlib parser above.
    dotenv_values = _parse_env_file

# Which .env keys each task needs to run on its own.
TASK_REQUIREMENTS = {
    1: ["OPENAI_ENDPOINT", "MODEL_DEPLOYMENT_NAME"],
    2: ["OPENAI_ENDPOINT", "MODEL_DEPLOYMENT_NAME"],
    3: ["CONTENT_UNDERSTANDING_ENDPOINT", "ANALYZER_ID"],
}

# Every key this lab might read, used when merging real environment variables.
ALL_KEYS = [
    "OPENAI_ENDPOINT",
    "MODEL_DEPLOYMENT_NAME",
    "CONTENT_UNDERSTANDING_ENDPOINT",
    "ANALYZER_ID",
]

# Placeholder text shipped in .env.example - present but not yet filled in.
# NOTE: .env.example values are also read at runtime (see _example_placeholders),
# so this list is a fallback, not the source of truth.
PLACEHOLDERS = {
    "",
    "your_endpoint",
    "your_analyzer_id",
    "your_model_deployment",
    "https://your-resource-name.openai.azure.com/openai/v1/",
    "https://your-resource-name.services.ai.azure.com/",
    "<your-openai-endpoint>",
    "<your-model-deployment-name>",
}

# Keys whose .env.example value is a REAL default the learner should KEEP.
# Anything not listed here is treated as unedited template text, so add a key
# here the moment you pre-fill a working value in .env.example - otherwise a
# correctly-configured learner is told it is MISSING.
EXAMPLE_REAL_DEFAULTS = set()

# How to fix each key, shown only when it's missing.
FIX_HINTS = {
    "OPENAI_ENDPOINT": (
        "Copy the Azure OpenAI endpoint for your Foundry resource from the project "
        "home page and add the '/openai/v1/' suffix, so it looks like "
        "https://<your-resource-name>.openai.azure.com/openai/v1/ . This is NOT the "
        "project endpoint."
    ),
    "MODEL_DEPLOYMENT_NAME": (
        "Set MODEL_DEPLOYMENT_NAME to the name of the multimodal chat model you "
        "deployed (for example, gpt-4o). You can see it in the Foundry portal under "
        "your project's Deployments page."
    ),
    "CONTENT_UNDERSTANDING_ENDPOINT": (
        "Task 3 uses Azure AI Content Understanding. Copy the resource endpoint from "
        "the Code Example tab of your analyzer in Content Understanding Studio - it "
        "looks like https://<your-resource-name>.services.ai.azure.com/ . This is NOT "
        "the Azure OpenAI endpoint."
    ),
    "ANALYZER_ID": (
        "Task 3 needs the name you gave your analyzer when you selected Build analyzer "
        "in Content Understanding Studio. You can see it in the analyzer list."
    ),
}


def _env_quote_problems(path):
    """Quote problems in the .env, detected independently of which parser is used.

    Runs the stdlib scanner even when python-dotenv is available, so the
    diagnosis is identical on both code paths.
    """
    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as handle:
            text = handle.read()
    except OSError:
        return []
    _, problems = _parse_env_text(text)
    return problems


def _file_has_bom(path):
    """True if the .env begins with a UTF-8 BOM.

    This matters because a BOM becomes part of the FIRST setting's name:
    python-dotenv reads it as "\ufeffOPENAI_ENDPOINT", so the app's
    os.getenv("OPENAI_ENDPOINT") returns None even though the file looks
    correct. A BOM'd .env genuinely does not work, so this must be reported
    to the learner - never silently normalized away.
    """
    try:
        with open(path, "rb") as handle:
            return handle.read(3) == b"\xef\xbb\xbf"
    except OSError:
        return False


def find_env_file():
    """Return the .env next to the lab's Python folder, wherever this is run from."""
    here = Path(__file__).resolve().parent
    candidates = [
        Path.cwd() / ".env",
        here.parent / "Python" / ".env",
        here.parent / ".env",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    # Default to the Python-folder location even if it doesn't exist yet.
    return here.parent / "Python" / ".env"


def load_values(env_path):
    """Merge real environment variables over .env file values (env wins)."""
    values = {}
    if env_path.exists():
        # INTENTIONAL DIVERGENCE - do not "fix" this to match python-dotenv.
        # A .env saved by some Windows editors starts with a UTF-8 BOM, which
        # python-dotenv glues onto the first key name ("\ufeffOPENAI_ENDPOINT").
        # Stripping it here is what makes the key list readable and makes both
        # parser paths agree. A parity check WILL flag this as a difference;
        # removing it does not improve correctness, it just hides the problem.
        # Safety comes from _file_has_bom() reporting the BOM and main()
        # exiting non-zero, not from matching the library here.
        values.update({
            k.lstrip("\ufeff"): v
            for k, v in dotenv_values(env_path).items()
            if v is not None
        })
    for key in ALL_KEYS:
        if os.environ.get(key):
            values[key] = os.environ[key]
    return values


def _example_placeholders(env_path):
    """Values shipped in .env.example are placeholders by definition.

    Reading them at runtime means this check cannot rot the way an exact-match
    list does: if .env.example is edited, its new values are still recognised
    as unedited. PLACEHOLDERS below stays as a fallback for values that were
    never in the example file.

    CONSTRAINT: values for keys listed in EXAMPLE_REAL_DEFAULTS are skipped,
    because those are real defaults a learner is meant to keep. Unioning them
    blindly would report a correctly-configured learner as MISSING - trading a
    false positive for a false negative that blocks someone who is ready.
    """
    example = Path(env_path).parent / ".env.example"
    return {
        value.strip()
        for key, value in _parse_env_file(str(example)).items()
        if value and value.strip() and key not in EXAMPLE_REAL_DEFAULTS
    }


def _is_endpoint_key(key):
    """Endpoint settings are always URLs, whatever the template text says."""
    return key.endswith("_ENDPOINT") or key.endswith("_URL")


def _looks_like_url(value):
    """Cheap shape test - enough to reject template text and wrong pastes.

    Deliberately permissive about the host so a local proxy such as
    http://localhost:8080 still passes.
    """
    value = value.strip()
    if " " in value:
        return False
    for scheme in ("https://", "http://"):
        if value.startswith(scheme):
            return len(value) > len(scheme)
    return False


def _wrong_shape(key, value):
    """Why a filled-in value is the wrong KIND of value, or None if it's fine.

    Shape rules beat keyword lists: template wording is unbounded
    (ENDPOINT_GOES_HERE, __ENDPOINT__, FILL_IN_ENDPOINT ...) but the shape of a
    setting is fixed. This also catches the mistake a keyword list never can -
    a real value pasted into the wrong setting.
    """
    if _is_endpoint_key(key):
        if not _looks_like_url(value):
            return ("This doesn't look like an endpoint - it must start with "
                    "https:// . Check you haven't pasted a resource name or a "
                    "model deployment name here.")
    elif _looks_like_url(value):
        return ("This should be a bare name, not a URL. Check you haven't "
                "pasted an endpoint here.")
    return None


def is_set(values, key, extra_placeholders=None):
    """A key counts as set if it's present, not a placeholder, and right-shaped."""
    value = (values.get(key) or "").strip()
    if not value:
        return False
    known = PLACEHOLDERS if not extra_placeholders else PLACEHOLDERS | extra_placeholders
    if value in known:
        return False
    return _wrong_shape(key, value) is None


def main():
    parser = argparse.ArgumentParser(
        description="Check that your .env has what a given lab task needs."
    )
    parser.add_argument(
        "--task",
        type=int,
        choices=sorted(TASK_REQUIREMENTS),
        required=True,
        help="Which task you're about to start (1-3).",
    )
    args = parser.parse_args()

    env_path = find_env_file()
    values = load_values(env_path)
    required = TASK_REQUIREMENTS[args.task]

    print(f"Checking readiness for Task {args.task}")
    print(f"Reading: {env_path}{'' if env_path.exists() else '  (not found yet)'}")
    print()

    example_placeholders = _example_placeholders(env_path)
    missing = [key for key in required
               if not is_set(values, key, example_placeholders)]
    has_bom = env_path.exists() and _file_has_bom(env_path)
    quote_problems = _env_quote_problems(env_path) if env_path.exists() else []

    for key in required:
        if is_set(values, key, example_placeholders):
            mark = "OK "
        elif _wrong_shape(key, (values.get(key) or "").strip()) and \
                (values.get(key) or "").strip() not in \
                (PLACEHOLDERS | example_placeholders):
            mark = "WRONG"
        else:
            mark = "MISSING"
        print(f"  [{mark}] {key}")

    if has_bom:
        print("  [PROBLEM] .env starts with a UTF-8 BOM")
    for problem in quote_problems:
        print(f"  [PROBLEM] .env {problem}")

    if not missing and not has_bom and not quote_problems:
        print()
        print(f"You're ready to start Task {args.task}.")
        return 0

    print()
    print("Fix the following before starting this task:")
    for key in missing:
        reason = _wrong_shape(key, (values.get(key) or "").strip())
        if reason and (values.get(key) or "").strip() not in \
                (PLACEHOLDERS | example_placeholders):
            print(f"\n  {key}\n    {reason}")
        else:
            print(f"\n  {key}\n    {FIX_HINTS.get(key, 'Add this key to your .env file.')}")

    if has_bom:
        print()
        print("  .env encoding")
        print("    Your .env was saved as 'UTF-8 with BOM' (Notepad does this by")
        print("    default). The BOM becomes part of the first setting's name, so the")
        print("    app reads that setting as empty even though the file looks correct.")
        print("    Re-save as plain UTF-8: in VS Code, click the encoding indicator in")
        print("    the status bar, choose 'Save with Encoding', then 'UTF-8'")
        print("    (NOT 'UTF-8 with BOM').")

    if quote_problems:
        print()
        print("  .env quoting")
        print("    The line listed above opens a quote that is never closed, so that")
        print("    setting is dropped - and depending on where the next quote appears,")
        print("    the settings after it can be swallowed into that value and dropped")
        print("    too. That is why a setting can look correct in the file and still")
        print("    read as empty. Close the quote on that line.")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
