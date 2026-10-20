"""Create a simulated GA4 events export (one row per event) with realistic tracking bugs.

Bugs added on purpose, so the SQL checks have something to find:
- signup_completed fired twice for some sign-ups (double click before the fix)
- an old event name still sent by a forgotten tag ("SignUpComplete")
- missing plan_name on some signup_started events
- paid traffic without utm_campaign
- signup_completed without signup_started in the same session
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(7)
OUT = Path(__file__).parent / "ga4_events_export.csv"
SOURCES = [("google", "cpc", "brand_fr"), ("google", "organic", None), ("facebook", "paid_social", "lookalike_q4"),
           ("(direct)", "(none)", None), ("partner_blog", "referral", None)]
PLANS = ["basic", "standard", "premium"]


def main():
    rows, start = [], datetime(2026, 10, 1)
    for s in range(6000):
        session_id = f"s{s:05d}"
        source, medium, campaign = random.choice(SOURCES)
        if medium in ("cpc", "paid_social") and random.random() < 0.06:
            campaign = None  # bug: campaign missing on paid traffic
        ts = start + timedelta(minutes=random.randint(0, 60 * 24 * 19))
        plan = random.choice(PLANS)

        def add(event, **params):
            nonlocal ts
            ts += timedelta(seconds=random.randint(5, 120))
            rows.append({"event_timestamp": ts.isoformat(sep=" "), "session_id": session_id, "event_name": event,
                         "utm_source": source, "utm_medium": medium, "utm_campaign": campaign or "",
                         "plan_name": params.get("plan_name", ""), "signup_id": params.get("signup_id", ""),
                         "company_size": params.get("company_size", "")})

        add("page_view")
        if random.random() < 0.35:
            add("cta_clicked")
        if random.random() < 0.20:
            started = random.random() > 0.08
            if started:
                add("signup_started", plan_name="" if random.random() < 0.05 else plan)
            if random.random() < 0.55:
                signup_id = f"su_{s:05d}"
                size = random.choice(["1", "2-9", "10-49", "50+"])
                add("signup_completed", plan_name=plan, signup_id=signup_id, company_size=size)
                if random.random() < 0.07:
                    add("signup_completed", plan_name=plan, signup_id=signup_id, company_size=size)  # double fire
                if random.random() < 0.03:
                    add("SignUpComplete")  # legacy tag still live
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"{OUT.name}: {len(rows)} events")


if __name__ == "__main__":
    main()
