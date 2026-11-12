-- Advisor performance: meeting-to-win conversion is where advisors differ most
WITH flags AS (
    SELECT
        l.advisor,
        l.lead_id,
        MAX(CASE WHEN h.stage = 'meeting' THEN 1 ELSE 0 END) AS had_meeting,
        MAX(CASE WHEN h.stage = 'won'     THEN 1 ELSE 0 END) AS won
    FROM leads l
    JOIN stage_history h USING (lead_id)
    GROUP BY l.advisor, l.lead_id
)
SELECT
    advisor,
    COUNT(*)                                                    AS leads,
    SUM(had_meeting)                                            AS meetings,
    SUM(won)                                                    AS won,
    ROUND(100.0 * SUM(won) / NULLIF(SUM(had_meeting), 0), 1)    AS meeting_to_win_pct,
    RANK() OVER (ORDER BY 1.0 * SUM(won) / NULLIF(SUM(had_meeting), 0) DESC) AS rank
FROM flags
GROUP BY advisor
ORDER BY rank;
