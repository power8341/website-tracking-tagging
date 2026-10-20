-- Rule 1: every event name must be in the tracking plan.
SELECT event_name, COUNT(*) AS events
FROM events
WHERE event_name NOT IN ('page_view', 'cta_clicked', 'pricing_plan_selected', 'signup_started',
                         'signup_step_completed', 'signup_completed', 'form_error', 'demo_requested')
GROUP BY event_name
ORDER BY events DESC;
