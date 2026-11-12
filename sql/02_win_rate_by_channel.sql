-- Which acquisition channel brings clients, not just leads?
SELECT
    l.channel,
    COUNT(*)                                                                      AS leads,
    SUM(CASE WHEN EXISTS (SELECT 1 FROM stage_history h WHERE h.lead_id = l.lead_id AND h.stage = 'meeting') THEN 1 ELSE 0 END) AS meetings,
    SUM(CASE WHEN EXISTS (SELECT 1 FROM stage_history h WHERE h.lead_id = l.lead_id AND h.stage = 'won') THEN 1 ELSE 0 END)     AS won,
    ROUND(100.0 * SUM(CASE WHEN EXISTS (SELECT 1 FROM stage_history h WHERE h.lead_id = l.lead_id AND h.stage = 'won') THEN 1 ELSE 0 END)
          / COUNT(*), 1)                                                          AS win_rate_pct
FROM leads l
GROUP BY l.channel
ORDER BY win_rate_pct DESC;
