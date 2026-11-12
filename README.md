# CRM Funnel in SQL

[![tests](https://github.com/guilherme-ferracini/crm-funnel-sql/actions/workflows/tests.yml/badge.svg)](https://github.com/guilherme-ferracini/crm-funnel-sql/actions)

Sales funnel analytics for an investment advisory office, in plain SQL (SQLite): **stage conversion, win rate by channel, advisor performance, time in stage and monthly cohorts**. It produces a terminal report and an HTML dashboard, using only the Python standard library.

## Why this exists

I owned CRM operations and BI reporting at an investment advisory office with 6 branches. The most useful questions were never "how many leads did we get?" but "which channels bring clients, where do leads stall, and which advisor converts meetings into accounts?" This repo answers them on a fictional dataset of 1,200 leads and about 3,500 stage changes.

## What the data shows

From [`samples/report.txt`](samples/report.txt):

- **Volume is not value.** Paid social brings the most leads (441) but converts only **4.5%**. Referrals bring fewer than half as many leads and convert at **21.5%**, almost 5× better.
- **The big drop is contact → meeting** (42.6% conversion). That is where follow-up cadence matters most.
- **Advisors differ after the meeting.** Meeting-to-win ranges from 28.8% to 34.0%: a coaching conversation, not a lead-distribution problem.
- **Proposals sit 11.5 days on average** before a decision, the longest stage and a clear target for a reminder routine.

## Queries

| File | Question | SQL techniques |
|---|---|---|
| `sql/01_funnel.sql` | How many leads reach each stage? | `LAG`, `FIRST_VALUE` window functions |
| `sql/02_win_rate_by_channel.sql` | Which channel brings clients? | correlated `EXISTS` subqueries |
| `sql/03_advisor_performance.sql` | Who converts meetings best? | per-lead flags, `RANK() OVER` |
| `sql/04_days_in_stage.sql` | Where do leads stall? | `LEAD() OVER (PARTITION BY ...)` |
| `sql/05_monthly_cohorts.sql` | Is lead quality improving? | cohort grouping, `LEFT JOIN` |

## Quickstart

```bash
python -m crmfunnel                               # terminal report
python -m crmfunnel --html out/dashboard.html     # HTML dashboard
python scripts/generate_data.py                   # regenerate fictional data (fixed seed)
python -m pytest -q                               # includes cross-query consistency checks
```

The tests also check that the queries agree with each other: total wins in the funnel equal total wins by channel, by advisor and by cohort.

## Data model

```
leads(lead_id, channel, advisor, created_on)
stage_history(lead_id, stage, entered_on)   -- lead → contacted → meeting → proposal → won | lost
```

See also [ops-metrics-sql](https://github.com/guilherme-ferracini/ops-metrics-sql), which applies the same approach to an operations desk.

## License

MIT
