import hashlib
import json
from pathlib import Path

import yaml
from fastapi import FastAPI

PROJECT_ROOT = Path(__file__).resolve().parent

PIN_FILE = PROJECT_ROOT / "prompts" / "pin.json"

CONFIG_FILE = PROJECT_ROOT / "config" / "triage.yaml"


app = FastAPI(
    title="AfyaPlus Versioned Prompt API",
    version="1.2.0",
)


def calculate_sha256(
    file_path: Path,
) -> str:

    text = file_path.read_text(encoding="utf-8")

    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")

    return hashlib.sha256(normalized_text.encode("utf-8")).hexdigest()


def load_pin():

    with open(
        PIN_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def load_config():

    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return yaml.safe_load(file)


@app.get("/health")
def health():

    pin = load_pin()

    config = load_config()

    prompt_file = PROJECT_ROOT / "prompts" / pin["prompt_file"]

    actual_sha = calculate_sha256(prompt_file)

    return {
        "status": "ok",
        "service": config["service"]["name"],
        "release_version": config["release"]["version"],
        "model": config["model"]["name"],
        "prompt_version": pin["prompt_version"],
        "prompt_file": pin["prompt_file"],
        "prompt_sha256_expected": pin["prompt_sha256"],
        "prompt_sha256_actual": actual_sha,
        "prompt_sha_match": (actual_sha == pin["prompt_sha256"]),
        "mcp_version": config["mcp"]["logistics_version"],
    }
