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
    Calculate a platform-independent SHA-256.

    Windows normally uses CRLF line endings,
    while Linux/GitHub Actions normally uses LF.

    We normalize all line endings to LF before hashing
    so the same prompt produces the same SHA everywhere.
    """

    text = file_path.read_text(encoding="utf-8")

    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")

    return hashlib.sha256(normalized_text.encode("utf-8")).hexdigest()


def main():

    with open(
        PIN_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        pin = json.load(file)

    prompt_file = PROMPTS_DIR / pin["prompt_file"]

    if not prompt_file.exists():

        raise FileNotFoundError(f"Prompt file not found: " f"{prompt_file}")

    sha256 = calculate_sha256(prompt_file)

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

    print(f"Prompt version: " f"{pin['prompt_version']}")

    print(f"Prompt file: " f"{pin['prompt_file']}")

    print(f"SHA-256: " f"{sha256}")


if __name__ == "__main__":
    main()
