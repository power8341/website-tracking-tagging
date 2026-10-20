# Google Tag Manager setup

How the data layer events from `site/datalayer.js` are sent to GA4 and the Meta Pixel.

## 1. Variables (Data Layer Variables)

| Variable name in GTM | Data layer key |
|---|---|
| DLV - plan_name | plan_name |
| DLV - plan_price | plan_price |
| DLV - company_size | company_size |
| DLV - signup_id | signup_id |
| DLV - step_number | step_number |
| DLV - cta_location | cta_location |
| DLV - utm_campaign | utm_campaign |

## 2. Triggers (Custom Event)

| Trigger | Event name |
|---|---|
| CE - cta_clicked | cta_clicked |
| CE - pricing_plan_selected | pricing_plan_selected |
| CE - signup_started | signup_started |
| CE - signup_step_completed | signup_step_completed |
| CE - signup_completed | signup_completed |
| CE - form_error | form_error |

## 3. Tags

| Tag | Type | Trigger | Settings |
|---|---|---|---|
| GA4 - Config | Google tag | All Pages | Measurement ID G-XXXXXXX |
| GA4 - signup_started | GA4 Event | CE - signup_started | parameters: plan_name |
| GA4 - signup_completed | GA4 Event | CE - signup_completed | parameters: plan_name, company_size, signup_id |
| GA4 - funnel events | GA4 Event | CE - cta_clicked, CE - pricing_plan_selected, CE - signup_step_completed, CE - form_error | event name: {{Event}} |
| Meta - Base | Custom HTML (Meta Pixel base code) | All Pages | Pixel ID |
| Meta - Lead | Custom HTML: fbq('track', 'Lead') | CE - signup_started | |
| Meta - CompleteRegistration | Custom HTML: fbq('track', 'CompleteRegistration', {content_name: {{DLV - plan_name}}}) | CE - signup_completed | eventID = {{DLV - signup_id}} for deduplication with the Conversions API |

## 4. GA4 key events

In GA4 Admin, mark `signup_started`, `signup_completed` and `demo_requested` as key events, so they can be imported into Google Ads.

## 5. Consent

Tags only fire after consent (Consent Mode v2): analytics_storage for GA4, ad_storage and ad_user_data for the Meta Pixel and Google Ads.

## 6. Testing

1. GTM Preview mode: open the site, fill the form, check each event and its parameters in the Tag Assistant panel.
2. GA4 DebugView: check the events arrive with the right parameters.
3. Meta Pixel Helper (browser extension): check Lead and CompleteRegistration fire once.
4. After a few days, export the GA4 events and run the SQL checks in `sql/`.
