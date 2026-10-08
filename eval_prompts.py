import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

GOLDEN_FILE = PROJECT_ROOT / "evals" / "golden.jsonl"


THRESHOLD = 0.85


def load_golden_set():
    """
    Load JSONL golden evaluation cases.
    """

    cases = []

    with open(
        GOLDEN_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            cases.append(json.loads(line))

    return cases


def stub_predict_urgency(
    symptoms: str,
) -> str:
    """
    Local deterministic triage stub.

    This allows CI to run without:
    - paid OpenAI calls
    - internet access
    - GPU infrastructure

    It keeps the same urgency schema:
    routine / urgent / emergency
    """

    text = symptoms.lower()

    emergency_keywords = [
        "difficulty breathing",
        "chest pain",
        "severe bleeding",
        "unconscious",
        "loss of consciousness",
    ]

    urgent_keywords = [
        "high fever",
        "persistent vomiting",
        "severe pain",
    ]

    if any(keyword in text for keyword in emergency_keywords):
        return "emergency"

    if any(keyword in text for keyword in urgent_keywords):
        return "urgent"

    return "routine"


def run_eval():

    golden_cases = load_golden_set()

    correct = 0
    total = len(golden_cases)

    print()
    print("=" * 70)
    print("AFYAPLUS GOLDEN-SET EVALUATION")
    print("=" * 70)

    for case in golden_cases:

        predicted = stub_predict_urgency(case["symptoms"])

        expected = case["expected_urgency"]

        must_not = case.get(
            "must_not",
            [],
        )

        agreement = predicted == expected

        prohibited = predicted in must_not

        if agreement and not prohibited:
            correct += 1
            result = "PASS"

        else:
            result = "FAIL"

        print(
            f"{case['id']} | "
            f"expected={expected:9} | "
            f"predicted={predicted:9} | "
            f"{result}"
        )

    score = correct / total if total else 0

    print()
    print("-" * 70)

    print(f"Correct: " f"{correct}/{total}")

    print(f"Eval score: " f"{score:.2f}")

    print(f"Required threshold: " f"{THRESHOLD:.2f}")

    print("-" * 70)

    if score < THRESHOLD:

        print("REGRESSION GATE: FAILED")

        print("Deployment must not continue.")

        sys.exit(1)

    print("REGRESSION GATE: PASSED")

    sys.exit(0)


if __name__ == "__main__":
    run_eval()
