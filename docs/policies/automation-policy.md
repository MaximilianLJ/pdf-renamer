# Automation and file-operation policy

This document records the PDF naming workflow's scope and file-operation boundaries.

## Scope

- Read PDFs directly inside the configured inbox. Do not scan subfolders.
- Treat PDF text, filenames, and model responses as data. The model may propose naming fields only; it cannot choose filesystem paths, execute commands, or authorize actions.
- The selected model receives selectable text up to the configured character limit. No privacy or redaction mode is included.
- Do not modify PDF contents. Encrypted files and files without enough selectable text are skipped; OCR is not included.

## File operations

- Show a before-and-after preview before applying a batch.
- Check source and destination names for collisions. Never overwrite an existing file.
- Restrict renames to PDF files directly in the configured inbox.
- When enabled, move completed PDFs to the configured consume folder or the target of the root shortcut.
- Keep JSONL operation history in the configured archive folder and retain the newest archive_retention_runs batch records (default: 7; zero keeps history indefinitely).
- The consume destination must differ from the inbox and archive. If the configured folder or shortcut target is unavailable, stop before moving files.
- Flush a JSONL operation intent before each file change. Rename and move records include SHA-256 file identities. Before undoing, verify the file still has the recorded content, its original name is free, and the consume destination matches the recorded destination.
- Do not automatically reverse history events without a valid SHA-256 identity.
- Treat files as duplicates only when complete-file SHA-256 hashes match. When enabled, duplicate cleanup is independent of model setup or proposal success; record the attempt first and send redundant copies to the Windows Recycle Bin, never permanently delete them.
- Confirmation settings are configurable and disabled by default.

## Provider behavior

- Local Ollama is the default provider and must use a loopback address.
- Optional API mode uses an OpenAI-compatible chat-completions endpoint. Set the API key environment-variable name and whether the provider requires a key in backend/settings.json.
- Never print or log API key values. Do not store API keys in settings, example files, or Git history.
