import hashlib
import json
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_prompt_pin_matches_file():

    pin_file = PROJECT_ROOT / "prompts" / "pin.json"

    with open(
        pin_file,
        "r",
        encoding="utf-8",
    ) as file:

        pin = json.load(file)

    prompt_file = PROJECT_ROOT / "prompts" / pin["prompt_file"]

    assert prompt_file.exists()

    text = prompt_file.read_text(encoding="utf-8")

    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")

    actual_sha = hashlib.sha256(normalized_text.encode("utf-8")).hexdigest()

    assert actual_sha == pin["prompt_sha256"]


def test_prompt_version_matches_config():

    pin_file = PROJECT_ROOT / "prompts" / "pin.json"

    config_file = PROJECT_ROOT / "config" / "triage.yaml"

    with open(
        pin_file,
        "r",
        encoding="utf-8",
    ) as file:

        pin = json.load(file)

    with open(
        config_file,
        "r",
        encoding="utf-8",
    ) as file:

        config = yaml.safe_load(file)

    assert pin["prompt_version"] == config["prompt"]["version"]


def test_release_versions_align():

    config_file = PROJECT_ROOT / "config" / "triage.yaml"

    with open(
        config_file,
        "r",
        encoding="utf-8",
    ) as file:

        config = yaml.safe_load(file)

    release_version = config["release"]["version"]

    prompt_version = config["prompt"]["version"]

    mcp_version = config["mcp"]["logistics_version"]

    assert release_version == prompt_version == mcp_version
