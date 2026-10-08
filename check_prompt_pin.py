import hashlib
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

PIN_FILE = PROJECT_ROOT / "prompts" / "pin.json"


def calculate_sha256(
    file_path: Path,
) -> str:

    return hashlib.sha256(file_path.read_bytes()).hexdigest()


def main():

    with open(
        PIN_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        pin = json.load(file)

    prompt_file = PROJECT_ROOT / "prompts" / pin["prompt_file"]

    if not prompt_file.exists():

        print("PROMPT PIN CHECK: FAILED")

        print(f"Prompt file does not exist: " f"{prompt_file}")

        sys.exit(1)

    actual_sha = calculate_sha256(prompt_file)

    expected_sha = pin["prompt_sha256"]

    print()
    print("=" * 70)
    print("PROMPT PIN CHECK")
    print("=" * 70)

    print(f"Prompt version: " f"{pin['prompt_version']}")

    print(f"Prompt file: " f"{pin['prompt_file']}")

    print(f"Expected SHA: " f"{expected_sha}")

    print(f"Actual SHA:   " f"{actual_sha}")

    if actual_sha != expected_sha:

        print()
        print("PROMPT PIN CHECK: FAILED")

        print("The prompt contents changed " "without updating pin.json.")

        sys.exit(1)

    print()
    print("PROMPT PIN CHECK: PASSED")

    sys.exit(0)


if __name__ == "__main__":
    main()
