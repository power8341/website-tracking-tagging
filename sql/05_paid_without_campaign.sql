-- Rule 5: paid traffic must have a utm_campaign, otherwise spend cannot be matched to results.
SELECT utm_medium,
       COUNT(DISTINCT session_id)                                                      AS paid_sessions,
       COUNT(DISTINCT CASE WHEN COALESCE(utm_campaign, '') = '' THEN session_id END)   AS sessions_without_campaign,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN COALESCE(utm_campaign, '') = '' THEN session_id END)
             / COUNT(DISTINCT session_id), 1)                                          AS pct
FROM events
WHERE utm_medium IN ('cpc', 'paid_social')
GROUP BY utm_medium
ORDER BY utm_medium;
