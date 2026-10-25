# AI usage and data flow

The PDF renamer makes one model request per eligible PDF to suggest naming metadata. It includes the repository's naming guideline with the request. It does not give the model filesystem access or permission to run commands. The application validates the returned fields and performs configured file operations.

## Local model (default)

With model_provider set to ollama, extracted text is processed by the configured Ollama model on this computer. The app accepts only a loopback Ollama endpoint. The included default is qwen3.5:9b-q4_K_M; it is an example starting point, not a benchmark winner. The one-click launcher starts Ollama only when needed and closes only the server process it started after the run; a pre-existing Ollama server is left running. Text is sent to the Ollama server running locally and is not uploaded to the Ollama model library. Model quality and response formatting vary, so results may differ when another model is selected.

## OpenAI-compatible API (optional)

With model_provider set to openai-compatible, extracted text leaves this computer and is sent to the configured endpoint. If hosted by a third party, that service's operator receives the request. The app cannot determine whether the operator retains, logs, or reuses it; review the provider's data-handling terms before use. Set api_key_env_var to the environment-variable name for the credential, and set api_key_required according to the provider. Credentials can be stored in the ignored .env file or the process environment. When the key is unset and api_key_required is false, the app sends no bearer authorization header. A supplied key is sent as a bearer token. The endpoint must support the OpenAI-compatible chat-completions format used by the app.

## Data sent to the model

There is no privacy or redaction mode. The model receives selectable PDF text up to max_text_characters, including personal or sensitive content present in the PDF. Text is extracted in PDF page order, joined, and truncated to a contiguous prefix at the character limit; later text is omitted and may affect naming quality. Scanned pages are not OCRed; encrypted PDFs and PDFs with too little selectable text are skipped. The app does not put extracted PDF text or API keys in its local rename history.

Review the selected provider's current data-handling terms before using API mode. The model name alone does not establish capability: model performance and endpoint behavior for this workflow have not been benchmarked.
