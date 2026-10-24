# PDF Renamer

A one-click Windows utility that extracts PDF text, asks a configured AI model to suggest consistent English or German filenames, previews the changes, and can move processed files to a Paperless consume destination.

## Quick start

1. Install Python 3.10 or newer. If needed, the launcher offers a user-scope Python installation through Windows Package Manager.
2. Keep or copy your Paperless shortcut into the repository root as paperless_consume.lnk. The shortcut is workstation-specific and excluded from Git.
3. Put PDFs directly in inbox/.
4. Double-click Start PDF Namer.bat.

The launcher creates a project-local .venv and installs the pinned dependencies there. This keeps the app's Python libraries separate from Python packages installed elsewhere on the computer.

With model_provider set to ollama, the first run checks for Ollama and the configured model. If Ollama is missing, choosing a model offers to install Ollama through Windows Package Manager; if that is unavailable, the launcher opens Ollama's official Windows download page. If the configured local model is missing, choose the recommended Qwen3.5 9B Q4 model, enter another Ollama model name, or skip installation. Hosted API mode skips Ollama setup.

The [current Ollama model listing](https://ollama.com/library/qwen3.5/tags) shows a download of about 6.6 GB. For this model at the default 12,288-token context, roughly 10 GB of free VRAM is a planning estimate, not a minimum or guarantee. Actual memory use varies with the Ollama version, model, context, and other GPU workloads. [Ollama can share work between GPU and system memory](https://docs.ollama.com/faq), but this may be slower and does not guarantee that a model will load or run acceptably. Model results vary, and this workflow has not been benchmarked across models.

After setup, the app processes PDFs from the configured inbox, shows a preview, applies the configured rename and move actions, and keeps an undo history in archive/. There are no send, rename, move, or duplicate confirmation prompts by default.

## Repository layout

    pdf-renamer/
    ├── inbox/                         PDFs to process; local contents ignored by Git
    ├── archive/                       Undo history; local JSONL files ignored by Git
    ├── backend/
    │   ├── bootstrap.py               First-run Ollama and model setup
    │   ├── pdf_namer.py               Extraction, model requests, and file operations
    │   └── settings.json              Human-editable provider and workflow settings
    ├── docs/
    │   ├── PDF_RENAMING_GUIDELINE.md  Naming conventions included in model requests
    │   └── policies/
    │       └── automation-policy.md   Workflow scope and file-operation boundaries
    ├── paperless_consume.lnk          Workstation shortcut; ignored by Git
    ├── Start PDF Namer.bat            One-click Windows launcher
    ├── AI_USAGE.md                    Model providers and data flow
    ├── README.md
    └── requirements.txt

## Model setup

The default uses Ollama locally with qwen3.5:9b-q4_K_M. To use another Ollama model, choose it in the first-run prompt or edit model_name in backend/settings.json. The launcher checks that exact model; it does not pick a model by matching its name.

For a hosted OpenAI-compatible service, set model_provider to openai-compatible, set model_name and model_endpoint, and configure the API key environment-variable name. If a key is required, put its value in the ignored .env file or in the process environment; backend/settings.json stores only variable names, never credential values. The endpoint must support the chat-completions request format used by the app.

Model capability claims from provider pages do not guarantee compatibility with a particular endpoint. Naming quality and response behavior depend on the selected model and service and may vary.

## Configuration

Edit backend/settings.json:

| Setting | Purpose |
|---|---|
| model_provider | ollama (local, default) or openai-compatible. |
| model_name | Exact model identifier to use. |
| model_endpoint | Ollama's local base URL or an API-compatible service base URL. |
| model_context_tokens | Context length used by local Ollama. |
| api_key_env_var | Environment-variable name containing the API credential. Set to an empty string when no key is used. |
| api_endpoint_env_var | Environment-variable name containing an API endpoint when model_endpoint is blank. |
| api_key_required | Whether API mode requires a non-empty credential. |
| input_folder | Inbox path relative to the repository root, or an absolute path. Defaults to inbox. |
| archive_folder | JSONL history folder relative to the repository root, or an absolute path. Defaults to archive. |
| archive_retention_runs | Number of newest batch history files to keep. Defaults to 7; 0 keeps history indefinitely. |
| consume_folder | Direct consume-folder path; leave blank to resolve consume_shortcut. It must differ from input_folder. |
| consume_shortcut | Shortcut path relative to the repository root, or an absolute path. |
| max_text_characters | Maximum selectable text sent per PDF. |
| auto_move_to_consume | Move successfully named PDFs to the configured destination. |
| remove_exact_duplicates | Send byte-for-byte duplicate copies to the Windows Recycle Bin. |
| confirm_before_* | Optional prompts for sending, renaming, moving, and duplicate cleanup. All default to false. |

For API mode, set the provider, model name, endpoint, and key settings in backend/settings.json. Copy .env.example to .env and add the provider's values using the configured environment-variable names. The .env file is excluded from Git.

When api_key_required is false, an unset key is allowed and the app omits the bearer authorization header. If a key value is present, it is still sent as a bearer token. The API integration does not provide other custom authentication headers.

All confirmation settings default to false. If confirm_before_send is enabled and the prompt is declined, the run stops before file changes. Duplicate-only batches make no model request and follow confirm_before_deduplicate instead.

## Processing details

- Reads selectable text from PDFs directly in the inbox; no OCR or PDF decryption.
- Uses SHA-256 to identify byte-for-byte duplicates. Redundant copies go to the Windows Recycle Bin when enabled.
- Validates model fields, normalizes filename components, and adds a suffix if a destination name already exists.
- Keeps a JSONL history file per changed batch in archive/. Undo the latest batch from the menu, or run the following command from the repository root:

        .venv\Scripts\python.exe backend\pdf_namer.py --undo
- Rename and move intents are flushed to history before file changes and include SHA-256 identities. Undo checks those hashes and the recorded consume destination.
- The shortcut, PDFs, credentials, virtual environment, and archive records are excluded from Git.

See AI_USAGE.md, docs/PDF_RENAMING_GUIDELINE.md, and docs/policies/automation-policy.md for details.
