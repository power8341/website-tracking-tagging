# Website Tracking and Tagging for Paid Acquisition

A complete tracking setup for a sign-up website: a tracking plan, data layer events in JavaScript, Google Tag Manager configuration for GA4 and the Meta Pixel, and SQL checks that find tracking bugs in the GA4 export.

## Why this project

Paid acquisition campaigns are only as good as their tracking. If a sign-up is counted twice, or a paid click has no campaign name, the team moves budget to the wrong channels. This project covers the full chain: decide what to track, implement it, send it to the ad platforms, and check that the data can be trusted.

## What is inside

| Part | File | What it does |
|---|---|---|
| Tracking plan | `docs/tracking_plan.md` | 8 events, their parameters, which ones are GA4 key events and Meta conversions, naming and privacy rules |
| Demo website | `site/index.html`, `site/signup.html` | landing page with pricing plans and a 3-step sign-up form |
| Data layer | `site/datalayer.js` | pushes every event to the GTM data layer, keeps UTM parameters for the session, fires `signup_completed` only once per sign-up |
| GTM setup | `docs/gtm_setup.md` | variables, triggers and tags for GA4 and the Meta Pixel, consent mode, deduplication, test steps |
| Data quality | `sql/`, `src/run_checks.py` | 5 SQL checks on a GA4 events export, with a markdown report |

## Data layer in action

Tested in a headless browser: a visitor comes from a Google Ads link, chooses the Premium plan, forgets a field, then completes the sign-up:

```json
{"event": "signup_started", "utm_source": "google", "utm_medium": "cpc", "utm_campaign": "brand_fr", "plan_name": "premium", "form_version": "v2"}
{"event": "form_error", "field_name": "company_size", "error_type": "missing"}
{"event": "signup_step_completed", "step_number": 1, "step_name": "company"}
{"event": "signup_step_completed", "step_number": 2, "step_name": "contact"}
{"event": "signup_completed", "plan_name": "premium", "company_size": "2-9", "signup_id": "su_1792515564743"}
```

## Tracking quality checks

Run on a simulated GA4 export of 9,976 events with realistic bugs ([full report](reports/tracking_quality_report.md)):

| Check | Result | Impact |
|---|---|---|
| Unknown events | 23 `SignUpComplete` events from a forgotten legacy tag | conversions counted under two names |
| Missing parameters | 47 `signup_started` without `plan_name` | plan analysis incomplete |
| Duplicate conversions | 50 sign-ups fired twice: 724 reported for 674 real | **conversions overcounted by 7.4%**, ad platforms optimise on wrong data |
| Completed without started | 49 sessions (7.3%) | `signup_started` trigger misses some users |
| Paid traffic without campaign | 6.7% of Google Ads and 6.4% of paid social sessions | spend cannot be matched to results |

The fixes are in the implementation: `trackOnce()` prevents double firing, the event list is fixed by the tracking plan, and the Meta CompleteRegistration tag uses `signup_id` as eventID for deduplication.

## How to run

```bash
pip install -r requirements.txt

# Data quality checks
python data/generate_ga4_export.py
python -m src.run_checks
python -m pytest -q

# Demo site: open site/index.html in a browser with ?utm_source=google&utm_medium=cpc&utm_campaign=test
# and watch the [tracking] logs in the browser console.
```

To connect the site to real tools: create a free GTM container and GA4 property, replace `GTM-XXXXXXX` in the HTML files, and follow `docs/gtm_setup.md`.

## Tech stack

JavaScript, Google Tag Manager, GA4, Meta Pixel, SQL (DuckDB), Python

## Author

Saiteja Eleti - [LinkedIn](https://www.linkedin.com/in/saiteja-eleti-169028332/)
