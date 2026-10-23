
import json
from pathlib import Path
from datetime import datetime

RESULTS_FILE = Path("data/results/study_results.json")


def save_result(result):
    """Save a study or quiz result without deleting previous results."""
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    try:
        with RESULTS_FILE.open("r", encoding="utf-8") as file:
            results = json.load(file)

        if not isinstance(results, list):
            results = []

    except (FileNotFoundError, json.JSONDecodeError):
        results = []

    result["timestamp"] = datetime.now().isoformat(timespec="seconds")
    result["data_source"] = "simulated"

    results.append(result)

    with RESULTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)
