-- Monthly cohorts: of the leads created each month, how many became clients?
SELECT
    strftime('%Y-%m', l.created_on)                                   AS cohort,
    COUNT(*)                                                           AS leads,
    SUM(CASE WHEN w.lead_id IS NOT NULL THEN 1 ELSE 0 END)             AS won,
    ROUND(100.0 * SUM(CASE WHEN w.lead_id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS win_rate_pct
FROM leads l
LEFT JOIN (SELECT DISTINCT lead_id FROM stage_history WHERE stage = 'won') w USING (lead_id)
GROUP BY cohort
ORDER BY cohort;
