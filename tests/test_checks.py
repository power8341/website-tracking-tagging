"""The checks must find exactly the bugs placed in a tiny export."""
import csv

from src.run_checks import run_checks

FIELDS = ["event_timestamp", "session_id", "event_name", "utm_source", "utm_medium", "utm_campaign",
          "plan_name", "signup_id", "company_size"]


def write(tmp_path, rows):
    path = tmp_path / "export.csv"
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(FIELDS)
        w.writerows(rows)
    return path


def test_checks_find_each_bug(tmp_path):
    rows = [
        # clean session
        ["2026-10-01 10:00:00", "s1", "signup_started", "google", "cpc", "brand", "basic", "", ""],
        ["2026-10-01 10:02:00", "s1", "signup_completed", "google", "cpc", "brand", "basic", "su1", "2-9"],
        # double fire + paid without campaign
        ["2026-10-01 11:00:00", "s2", "signup_started", "facebook", "paid_social", "", "premium", "", ""],
        ["2026-10-01 11:02:00", "s2", "signup_completed", "facebook", "paid_social", "", "premium", "su2", "1"],
        ["2026-10-01 11:02:01", "s2", "signup_completed", "facebook", "paid_social", "", "premium", "su2", "1"],
        # completed without started + legacy event + missing plan
        ["2026-10-01 12:00:00", "s3", "signup_completed", "(direct)", "(none)", "", "", "su3", "1"],
        ["2026-10-01 12:00:05", "s3", "SignUpComplete", "(direct)", "(none)", "", "", "", ""],
    ]
    r = run_checks(write(tmp_path, rows))
    assert r["01_unknown_events"].event_name.tolist() == ["SignUpComplete"]
    assert r["02_missing_parameters"].events.sum() == 1
    dup = r["03_duplicate_conversions"].iloc[0]
    assert dup.duplicated_signups == 1 and dup.real_signups == 3 and dup.reported_signups == 4
    assert r["04_completed_without_started"].iloc[0].without_signup_started == 1
    paid = r["05_paid_without_campaign"].set_index("utm_medium")
    assert paid.loc["paid_social", "sessions_without_campaign"] == 1
    assert paid.loc["cpc", "sessions_without_campaign"] == 0
