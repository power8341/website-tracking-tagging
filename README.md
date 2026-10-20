# Website Tracking and Tagging for Paid Acquisition

**Status: in progress**

A tracking setup for a simple website: a clear tracking plan, tags in Google Tag Manager, conversion events in GA4 and the Meta Pixel, and a data quality check to make sure the numbers can be trusted.

## Why this project

Paid acquisition campaigns are only as good as their tracking. If a sign-up event is missing or counted twice, the team spends money on the wrong channels. This project shows how to set up tracking properly and check it.

## How it works

1. Write a tracking plan: which events to track (page view, sign-up started, sign-up completed, demo requested), with their properties.
2. Build a simple test website and push events to the data layer with JavaScript.
3. Configure tags, triggers and variables in Google Tag Manager.
4. Send conversion events to GA4 and the Meta Pixel.
5. Export GA4 data and run a SQL check: missing events, duplicates, unexpected values.

## Tech stack

Google Tag Manager, GA4, JavaScript, Meta Pixel, SQL

## Progress

- [ ] Tracking plan design
- [ ] Test website with data layer events
- [x] Google Tag Manager configuration
- [ ] GA4 and Meta Pixel conversion events
- [ ] SQL data quality check

## Planned structure

```
website-tracking-tagging/
  docs/
    tracking_plan.md
  site/
    index.html
    datalayer.js
  sql/
    tracking_quality_checks.sql
  README.md
```

## Author

Saiteja Eleti - [LinkedIn](https://www.linkedin.com/in/saiteja-eleti-169028332/)
