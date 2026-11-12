-- How long do leads sit in each stage before moving on (or being lost)?
WITH transitions AS (
    SELECT
        lead_id,
        stage,
        entered_on,
        LEAD(entered_on) OVER (PARTITION BY lead_id ORDER BY entered_on,
            CASE stage WHEN 'lead' THEN 1 WHEN 'contacted' THEN 2 WHEN 'meeting' THEN 3
                       WHEN 'proposal' THEN 4 ELSE 5 END) AS left_on
    FROM stage_history
)
SELECT
    stage,
    COUNT(*)                                                    AS transitions,
    ROUND(AVG(julianday(left_on) - julianday(entered_on)), 1)   AS avg_days,
    MAX(julianday(left_on) - julianday(entered_on))             AS max_days
FROM transitions
WHERE left_on IS NOT NULL
GROUP BY stage
ORDER BY CASE stage WHEN 'lead' THEN 1 WHEN 'contacted' THEN 2 WHEN 'meeting' THEN 3 ELSE 4 END;
