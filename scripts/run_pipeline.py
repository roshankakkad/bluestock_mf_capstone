"""Master execution script for the Bluestock mutual fund capstone pipeline.

Run this file from the project root to execute the main reproducible workflow:
1. Profile raw CSV files.
2. Clean data and load SQLite tables.
3. Optionally fetch live NAV data when network access is available.
"""

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_step(command: list[str], label: str) -> None:
    """Run one pipeline command and stop if it fails."""
    print(f"--- {label} ---")
    subprocess.run(command, cwd=PROJECT_ROOT, check=True)


def main() -> None:
    """Parse options and execute the capstone pipeline."""
    parser = argparse.ArgumentParser(description="Run Bluestock MF capstone pipeline")
    parser.add_argument("--fetch-live-nav", action="store_true", help="Fetch live NAV files from mfapi.in")
    args = parser.parse_args()

    run_step([sys.executable, "scripts/data_ingestion.py"], "Raw data profiling")
    if args.fetch_live_nav:
        run_step([sys.executable, "scripts/live_nav_fetch.py"], "Live NAV fetch")
    run_step([sys.executable, "scripts/day2_clean_load.py"], "Clean data and load SQLite")
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
