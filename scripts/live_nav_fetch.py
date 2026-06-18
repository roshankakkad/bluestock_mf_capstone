"""Fetch live NAV history for selected mutual fund schemes from mfapi.in.

The script stores one CSV per scheme in data/raw. Network errors are handled per
scheme so that a temporary failure does not stop the complete fetch process.
"""

from pathlib import Path
import pandas as pd
import requests

RAW_DIR = Path("data/raw")
SCHEMES = {
    "HDFC_Top100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_LargeCap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841,
}


def fetch_scheme_nav(name: str, code: int) -> Path:
    """Fetch NAV history for one scheme and save it as a raw CSV file."""
    url = f"https://api.mfapi.in/mf/{code}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data.get("data", []))
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RAW_DIR / f"{name}_live_nav.csv"
    df.to_csv(output_path, index=False)
    return output_path


def main() -> None:
    """Fetch all configured live NAV datasets."""
    for name, code in SCHEMES.items():
        try:
            output_path = fetch_scheme_nav(name, code)
            print(f"Saved {output_path}")
        except Exception as exc:  # noqa: BLE001 - keep the batch running per scheme.
            print(f"Skipped {name}: {exc}")


if __name__ == "__main__":
    main()
