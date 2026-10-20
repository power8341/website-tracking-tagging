# Tracking quality report

## Unknown events

| event_name     |   events |
|:---------------|---------:|
| SignUpComplete |       23 |

## Missing parameters

| event_name     | missing_parameter   |   events |
|:---------------|:--------------------|---------:|
| signup_started | plan_name           |       47 |

## Duplicate conversions

|   duplicated_signups |   extra_events |   real_signups |   reported_signups |   pct_overcount |
|---------------------:|---------------:|---------------:|-------------------:|----------------:|
|                   50 |             50 |            674 |                724 |             7.4 |

## Completed without started

|   sessions_with_signup |   without_signup_started |   pct |
|-----------------------:|-------------------------:|------:|
|                    674 |                       49 |   7.3 |

## Paid without campaign

| utm_medium   |   paid_sessions |   sessions_without_campaign |   pct |
|:-------------|----------------:|----------------------------:|------:|
| cpc          |            1158 |                          78 |   6.7 |
| paid_social  |            1210 |                          78 |   6.4 |
