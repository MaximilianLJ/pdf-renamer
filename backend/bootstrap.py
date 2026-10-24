"""Prepare the configured local Ollama model before the one-click run."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import urlopen


SETTINGS_PATH = Path(__file__).resolve().parent / "settings.json"
RECOMMENDED_MODEL = "qwen3.5:9b-q4_K_M"
MODEL_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}
OLLAMA_DOWNLOAD_URL = "https://ollama.com/download/windows"


class BootstrapError(Exception):
    """An actionable setup error that can be shown in the launcher window."""


def load_settings() -> dict[str, object]:
    """Load the JSON settings used by both the launcher and the naming app."""
    try:
        settings = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        raise BootstrapError("Could not read backend/settings.json.") from None
    if not isinstance(settings, dict):
        raise BootstrapError("backend/settings.json must contain a JSON object.")
    return settings


def ollama_url(settings: dict[str, object]) -> str:
    """Validate and return a loopback-only Ollama API base URL."""
    value = settings.get("model_endpoint")
    if not isinstance(value, str) or not value.strip():
        raise BootstrapError("Set model_endpoint in backend/settings.json.")
    try:
        parsed = urlsplit(value.strip())
    except ValueError:
        raise BootstrapError("Ollama must use a plain localhost URL.") from None
    if (
        parsed.scheme.lower() != "http"
        or parsed.hostname not in LOCAL_HOSTS
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or parsed.path not in {"", "/"}
    ):
        raise BootstrapError("Ollama must use a plain localhost URL.")
    try:
        port = parsed.port
    except ValueError:
        raise BootstrapError("Ollama URL contains an invalid port.") from None
    port = port if port is not None else 11434
    if not 1 <= port <= 65535:
        raise BootstrapError("Ollama URL contains an invalid port.")
    hostname = parsed.hostname or "localhost"
    host_literal = f"[{hostname}]" if ":" in hostname else hostname
    return f"http://{host_literal}:{port}"


def ollama_environment(base_url: str) -> dict[str, str]:
    """Direct Ollama CLI subprocesses to the same local server as the app."""
    environment = os.environ.copy()
    environment["OLLAMA_HOST"] = urlsplit(base_url).netloc
    return environment


def configured_model(settings: dict[str, object]) -> str:
    """Validate the configured Ollama model identifier before invoking Ollama."""
    value = settings.get("model_name")
    if not isinstance(value, str) or not MODEL_NAME.fullmatch(value.strip()):
        raise BootstrapError("model_name must be a valid Ollama model name.")
    model = value.strip()
    if "cloud" in model.casefold():
        raise BootstrapError("Choose a local Ollama model, not a cloud model.")
    return model


def server_is_ready(base_url: str) -> bool:
    """Return whether the local Ollama API is answering requests."""
    try:
        with urlopen(f"{base_url}/api/tags", timeout=2) as response:
            return response.status == 200
    except (OSError, URLError, TimeoutError):
        return False


def start_server(executable: str, base_url: str) -> None:
    """Start Ollama without opening a second console, then wait for its API."""
    if not server_is_ready(base_url):
        try:
            subprocess.Popen(
                [executable, "serve"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                env=ollama_environment(base_url),
            )
        except OSError:
            raise BootstrapError("Could not start the local Ollama server.") from None

    for _ in range(30):
        if server_is_ready(base_url):
            return
        time.sleep(1)
    raise BootstrapError("Ollama did not start. Open the Ollama app and try again.")


def find_ollama() -> str | None:
    """Find Ollama on PATH or in its usual per-user and machine install folders."""
    executable = shutil.which("ollama")
    if executable and Path(executable).is_file():
        return executable

    candidates = []
    local_app_data = os.environ.get("LOCALAPPDATA")
    program_files = os.environ.get("PROGRAMFILES", r"C:\Program Files")
    if local_app_data:
        candidates.append(Path(local_app_data) / "Programs" / "Ollama" / "ollama.exe")
    candidates.append(Path(program_files) / "Ollama" / "ollama.exe")
    return next((str(path) for path in candidates if path.is_file()), None)


def model_is_installed(executable: str, model: str, base_url: str) -> bool:
    """Check whether the exact configured model is already installed."""
    try:
        result = subprocess.run(
            [executable, "show", model],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
            env=ollama_environment(base_url),
        )
    except (OSError, subprocess.TimeoutExpired):
        raise BootstrapError("Could not check whether the configured model is installed.") from None
    return result.returncode == 0


def choose_model_to_install(configured_model: str) -> str | None:
    """Ask the user which model to install instead of guessing by model name."""
    print("\nNo model detected.")
    print(f"Configured model not found: {configured_model}")
    print(f"1. Install recommended {RECOMMENDED_MODEL}")
    print("   Download: about 6.6 GB. Plan for roughly 10 GB of free VRAM at 12K context; estimate varies.")
    print("2. Install another Ollama model (enter its model name)")
    print("3. Don't install anything")
    choice = input("Choose 1, 2, or 3: ").strip()
    if choice == "1":
        return RECOMMENDED_MODEL
    if choice == "2":
        while True:
            model = input("Ollama model name (for example, qwen3.5:9b): ").strip()
            if MODEL_NAME.fullmatch(model) and "cloud" not in model.casefold():
                return model
            print("Enter a model name using letters, numbers, dots, underscores, colons, slashes, or hyphens.")
    if choice == "3":
        print("Model installation skipped; the naming app will still open.")
        return None
    print("No model was selected; the naming app will still open.")
    return None


def install_ollama() -> str:
    """Install Ollama through its Windows Package Manager package."""
    winget = shutil.which("winget")
    if not winget:
        webbrowser.open(OLLAMA_DOWNLOAD_URL)
        raise BootstrapError(
            "Windows Package Manager was not found. Install Ollama from the opened page, then run this launcher again."
        )

    print("\nInstalling Ollama for Windows through Windows Package Manager...")
    try:
        result = subprocess.run(
            [
                winget,
                "install",
                "--id",
                "Ollama.Ollama",
                "--exact",
                "--source",
                "winget",
                "--accept-package-agreements",
                "--accept-source-agreements",
            ],
            check=False,
        )
    except OSError:
        raise BootstrapError("Could not start the Ollama installation.") from None
    if result.returncode:
        raise BootstrapError("Ollama installation did not complete. Install it manually, then run this launcher again.")
    executable = find_ollama()
    if not executable:
        raise BootstrapError("Ollama installed, but this window cannot find it yet. Close and relaunch the batch file.")
    return executable


def pull_model(executable: str, model: str, base_url: str) -> None:
    """Download one explicitly selected model through the Ollama CLI."""
    print(f"\nDownloading {model}. This may take a while the first time.")
    try:
        result = subprocess.run(
            [executable, "pull", model],
            check=False,
            env=ollama_environment(base_url),
        )
    except OSError:
        raise BootstrapError("Could not start the Ollama model download.") from None
    if result.returncode:
        raise BootstrapError("The model download failed. Check the model name, connection, and free disk space.")


def save_settings(settings: dict[str, object]) -> None:
    """Atomically save the chosen model without writing credentials."""
    temporary_path = SETTINGS_PATH.with_suffix(".tmp")
    try:
        temporary_path.write_text(
            json.dumps(settings, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary_path, SETTINGS_PATH)
    except OSError:
        try:
            temporary_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise BootstrapError("Could not save the selected model to backend/settings.json.") from None


def prepare_local_model(settings: dict[str, object]) -> None:
    """Start Ollama and make the explicitly selected model available locally."""
    base_url = ollama_url(settings)
    model = configured_model(settings)
    executable = find_ollama()
    if executable:
        start_server(executable, base_url)
        if model_is_installed(executable, model, base_url):
            return

    selected_model = choose_model_to_install(model)
    if selected_model is None:
        return
    if executable is None:
        executable = install_ollama()
        start_server(executable, base_url)
    if not model_is_installed(executable, selected_model, base_url):
        pull_model(executable, selected_model, base_url)
    settings["model_name"] = selected_model
    save_settings(settings)
    print(f"Configured model is ready: {selected_model}")


def main() -> int:
    """Prepare local inference only when Ollama is the selected provider."""
    try:
        settings = load_settings()
        provider_value = settings.get("model_provider", "ollama")
        if not isinstance(provider_value, str):
            raise BootstrapError("model_provider must be 'ollama' or 'openai-compatible'.")
        provider = provider_value.strip().casefold()
        if provider == "ollama":
            prepare_local_model(settings)
        elif provider != "openai-compatible":
            raise BootstrapError("model_provider must be 'ollama' or 'openai-compatible'.")
        return 0
    except BootstrapError as exc:
        print(f"\n{exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
