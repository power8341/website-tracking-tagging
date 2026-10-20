# Tracking plan

Website: landing page and sign-up form of a B2B online business account (demo site in `site/`).
Goal: measure the acquisition funnel and send reliable conversions to GA4 and Meta for paid campaigns.

## Naming rules

- Event names in snake_case, verb at the end: `signup_started`, not `StartSignup`.
- Every event carries `page_type` and, when known, `utm_source`, `utm_medium`, `utm_campaign` (read from the URL on landing and kept for the session).
- No personal data in events (no email, no name, no phone). Only ids and categories.

## Events

| Event | When it fires | Parameters | GA4 | Meta Pixel |
|---|---|---|---|---|
| `page_view` | every page load | page_type, page_path | automatic | PageView |
| `cta_clicked` | click on "Open an account" | cta_location (hero, pricing, footer) | event | - |
| `pricing_plan_selected` | click on a plan card | plan_name, plan_price | event | ViewContent |
| `signup_started` | first field of the sign-up form is filled | plan_name, form_version | **key event** | Lead |
| `signup_step_completed` | each form step validated | step_number (1 to 3), step_name | event | - |
| `signup_completed` | final form submit succeeds | plan_name, company_size, signup_id | **key event** | CompleteRegistration |
| `form_error` | a field shows a validation error | field_name, error_type | event | - |
| `demo_requested` | demo form submitted | company_size | **key event** | Schedule |

## Data quality rules (checked in `sql/`)

1. Every event name must be in this plan.
2. Required parameters must be present (see table).
3. `signup_completed` must fire only once per `signup_id` (no double firing).
4. A session with `signup_completed` must also have `signup_started` before it.
5. Paid traffic (`utm_medium` = cpc or paid_social) must have a `utm_campaign`.
