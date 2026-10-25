"""Run setup and the naming workflow under one Ollama server lifecycle."""

from __future__ import annotations

import subprocess
import sys

import bootstrap
import pdf_namer


def main() -> int:
    """Prepare the model, run the configured inbox, then stop owned Ollama."""
    owned_server = None

    def remember_server(process: subprocess.Popen[bytes]) -> None:
        nonlocal owned_server
        owned_server = process

    try:
        try:
            settings = bootstrap.load_settings()
            provider_value = settings.get("model_provider", "ollama")
            if not isinstance(provider_value, str):
                raise bootstrap.BootstrapError(
                    "model_provider must be 'ollama' or 'openai-compatible'."
                )
            provider = provider_value.strip().casefold()
            if provider == "ollama":
                owned_server = bootstrap.prepare_local_model(
                    settings,
                    on_server_started=remember_server,
                )
            elif provider != "openai-compatible":
                raise bootstrap.BootstrapError(
                    "model_provider must be 'ollama' or 'openai-compatible'."
                )
        except bootstrap.BootstrapError as exc:
            print(f"\n{exc}")
            print(
                "\nModel setup did not complete. The naming app will still start; "
                "model naming may fail, but configured duplicate cleanup can run."
            )
        return pdf_namer.main(["--run"])
    finally:
        bootstrap.stop_server(owned_server)


if __name__ == "__main__":
    sys.exit(main())
