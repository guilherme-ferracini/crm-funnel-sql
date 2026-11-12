from crmfunnel.run import load, run_all

CON = load()
RESULTS = run_all(CON)


def rows(stem):
    cols, data = RESULTS[stem]
    return [dict(zip(cols, r)) for r in data]


def test_all_queries_return_rows():
    assert len(RESULTS) == 5 and all(d for _, d in RESULTS.values())


def test_funnel_is_monotonic():
    counts = [r["leads"] for r in rows("01_funnel")]
    assert counts == sorted(counts, reverse=True)
    assert rows("01_funnel")[0]["conv_from_lead_pct"] == 100.0


def test_channel_totals_match_leads():
    total = CON.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
    assert sum(r["leads"] for r in rows("02_win_rate_by_channel")) == total


def test_won_consistent_across_queries():
    won_funnel = next(r["leads"] for r in rows("01_funnel") if r["stage"] == "won")
    assert sum(r["won"] for r in rows("02_win_rate_by_channel")) == won_funnel
    assert sum(r["won"] for r in rows("03_advisor_performance")) == won_funnel
    assert sum(r["won"] for r in rows("05_monthly_cohorts")) == won_funnel


def test_days_in_stage_non_negative():
    assert all(r["avg_days"] >= 0 for r in rows("04_days_in_stage"))
