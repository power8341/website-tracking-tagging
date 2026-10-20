"""Run the tracking data quality checks on a GA4 events export and write a report.

Usage:
    python data/generate_ga4_export.py
    python -m src.run_checks --input data/ga4_events_export.csv
"""

import argparse
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent


def run_checks(csv_path):
    con = duckdb.connect()
    con.execute(f"CREATE TABLE events AS SELECT * FROM read_csv_auto('{csv_path}', all_varchar=true)")
    return {f.stem: con.execute(f.read_text()).df() for f in sorted((ROOT / "sql").glob("*.sql"))}


def write_report(results, path):
    lines = ["# Tracking quality report", ""]
    for name, df in results.items():
        title = name.split("_", 1)[1].replace("_", " ").capitalize()
        lines += [f"## {title}", "", df.to_markdown(index=False) if not df.empty else "No issue found.", ""]
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(ROOT / "data" / "ga4_events_export.csv"))
    parser.add_argument("--report", default=str(ROOT / "reports" / "tracking_quality_report.md"))
    args = parser.parse_args()
    results = run_checks(args.input)
    for name, df in results.items():
        print(f"\n== {name} ==\n{df.to_string(index=False) if not df.empty else 'No issue found.'}")
    write_report(results, args.report)
    print(f"\nReport written to {args.report}")


if __name__ == "__main__":
    main()
