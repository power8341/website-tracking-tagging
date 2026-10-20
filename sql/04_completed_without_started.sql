-- Rule 4: a session with signup_completed must also have signup_started before it.
WITH s AS (
    SELECT session_id,
           MIN(CASE WHEN event_name = 'signup_started'   THEN CAST(event_timestamp AS TIMESTAMP) END) AS started_at,
           MIN(CASE WHEN event_name = 'signup_completed' THEN CAST(event_timestamp AS TIMESTAMP) END) AS completed_at
    FROM events
    GROUP BY session_id
)
SELECT COUNT(*) FILTER (WHERE completed_at IS NOT NULL)                                            AS sessions_with_signup,
       COUNT(*) FILTER (WHERE completed_at IS NOT NULL AND (started_at IS NULL OR started_at > completed_at)) AS without_signup_started,
       ROUND(100.0 * COUNT(*) FILTER (WHERE completed_at IS NOT NULL AND (started_at IS NULL OR started_at > completed_at))
             / NULLIF(COUNT(*) FILTER (WHERE completed_at IS NOT NULL), 0), 1)                     AS pct
FROM s;
