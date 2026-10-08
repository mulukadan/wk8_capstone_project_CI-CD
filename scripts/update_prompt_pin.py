import hashlib
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROMPTS_DIR = PROJECT_ROOT / "prompts"

PIN_FILE = PROMPTS_DIR / "pin.json"


def calculate_sha256(
    file_path: Path,
) -> str:
    """
    Calculate SHA-256 for a file.

    This gives us a unique fingerprint
    for the exact prompt contents.
    """

    content = file_path.read_bytes()

    return hashlib.sha256(
        content
    ).hexdigest()


def main():

    with open(
        PIN_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        pin = json.load(file)

    prompt_file = (
        PROMPTS_DIR
        / pin["prompt_file"]
    )

    if not prompt_file.exists():

        raise FileNotFoundError(
            f"Prompt file not found: "
            f"{prompt_file}"
        )

    sha256 = calculate_sha256(
        prompt_file
    )

    pin["prompt_sha256"] = sha256

    with open(
        PIN_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            pin,
            file,
            indent=2,
        )

    print(
        f"Prompt version: "
        f"{pin['prompt_version']}"
    )

    print(
        f"Prompt file: "
        f"{pin['prompt_file']}"
    )

    print(
        f"SHA-256: "
        f"{sha256}"
    )


if __name__ == "__main__":
    main()