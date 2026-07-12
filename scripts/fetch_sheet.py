"""
One-off script: download the public "LORS SYRIA" Google Sheet and save
a local CSV copy of each tab for inspection.

Google's bulk /export?format=xlsx endpoint is blocked for this environment,
so each sheet tab is fetched individually via the gviz CSV endpoint instead.

`headers=0` is required: gviz auto-detects a "header" row count from the
data and, on this sheet, mis-guesses 367 header rows — collapsing that
many real rows (the entire Alfa Romeo..GMC section) into a single garbled
column-label string and dropping them from the actual CSV rows entirely.
Forcing headers=0 makes gviz treat every row as data.

Usage:
    .venv/bin/python scripts/fetch_sheet.py
"""

import pathlib

import requests

SHEET_ID = "1orxWJjMS1UlauD8Y2PRyO-REkEi2pS5aTrIZx_52RPM"
SHEET_NAMES = ["Лист1", "Лист2", "Лист3", "Лист4", "Лист5", "Лист6"]
GVIZ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq"

DATA_DIR = pathlib.Path(__file__).resolve().parent.parent / "data"


def fetch_sheet_csv(sheet_name: str) -> bytes:
    params = {"tqx": "out:csv", "sheet": sheet_name, "headers": "0"}
    response = requests.get(GVIZ_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.content


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)

    for name in SHEET_NAMES:
        content = fetch_sheet_csv(name)
        if not content.strip():
            print(f"{name}: empty, skipped")
            continue
        csv_path = DATA_DIR / f"{name}.csv"
        csv_path.write_bytes(content)
        n_lines = content.count(b"\n") + 1
        print(f"saved {csv_path} (~{n_lines} lines)")


if __name__ == "__main__":
    main()
