-- Rule 2: required parameters must be present.
SELECT event_name, 'plan_name' AS missing_parameter, COUNT(*) AS events
FROM events
WHERE event_name IN ('signup_started', 'signup_completed') AND COALESCE(plan_name, '') = ''
GROUP BY event_name
UNION ALL
SELECT event_name, 'signup_id', COUNT(*)
FROM events
WHERE event_name = 'signup_completed' AND COALESCE(signup_id, '') = ''
GROUP BY event_name;
