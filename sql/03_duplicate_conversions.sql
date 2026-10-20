-- Rule 3: signup_completed must fire once per signup_id. Duplicates inflate conversions in GA4 and Meta.
WITH counts AS (
    SELECT signup_id, COUNT(*) AS times_fired
    FROM events
    WHERE event_name = 'signup_completed' AND COALESCE(signup_id, '') <> ''
    GROUP BY signup_id
)
SELECT COUNT(*) FILTER (WHERE times_fired > 1)                       AS duplicated_signups,
       SUM(times_fired) - COUNT(*)                                    AS extra_events,
       COUNT(*)                                                       AS real_signups,
       SUM(times_fired)                                               AS reported_signups,
       ROUND(100.0 * (SUM(times_fired) - COUNT(*)) / COUNT(*), 1)     AS pct_overcount
FROM counts;
