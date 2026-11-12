-- Overall funnel: leads reaching each stage and conversion from the previous stage
WITH reached AS (
    SELECT stage, COUNT(DISTINCT lead_id) AS leads
    FROM stage_history
    WHERE stage <> 'lost'
    GROUP BY stage
),
ordered AS (
    SELECT
        stage,
        leads,
        CASE stage WHEN 'lead' THEN 1 WHEN 'contacted' THEN 2 WHEN 'meeting' THEN 3
                   WHEN 'proposal' THEN 4 WHEN 'won' THEN 5 END AS step
    FROM reached
)
SELECT
    step,
    stage,
    leads,
    ROUND(100.0 * leads / LAG(leads) OVER (ORDER BY step), 1)              AS conv_from_prev_pct,
    ROUND(100.0 * leads / FIRST_VALUE(leads) OVER (ORDER BY step), 1)      AS conv_from_lead_pct
FROM ordered
ORDER BY step;
