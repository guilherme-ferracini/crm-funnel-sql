"""Fictional CRM data for an investment advisory office: leads and their stage history.
Fixed seed, so committed CSVs and tests always agree."""

from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

OUT = Path(__file__).parents[1] / "data"
random.seed(7)

CHANNELS = {"referral": 0.55, "events": 0.40, "website": 0.25, "paid_social": 0.15}   # base quality
ADVISORS = {"Ana": 1.15, "Bruno": 1.0, "Carla": 0.85, "Diego": 1.05}                 # skill factor
STAGES = ["lead", "contacted", "meeting", "proposal", "won"]
DAYS = {"lead": 2, "contacted": 6, "meeting": 9, "proposal": 12}


def main() -> None:
    OUT.mkdir(exist_ok=True)
    leads, history = [], []
    start = datetime(2026, 4, 1)
    for i in range(1, 1201):
        channel = random.choices(list(CHANNELS), weights=[2, 2, 4, 5])[0]
        advisor = random.choice(list(ADVISORS))
        created = start + timedelta(days=random.randint(0, 182))
        leads.append([i, channel, advisor, created.date().isoformat()])
        t = created
        history.append([i, "lead", t.date().isoformat()])
        quality = CHANNELS[channel] * ADVISORS[advisor]
        for prev, nxt in zip(STAGES[:-1], STAGES[1:]):
            p = min(0.95, {"contacted": 0.85, "meeting": 0.45, "proposal": 0.6, "won": 0.55}[nxt] * (0.6 + quality))
            if random.random() > p:
                if prev != "lead":
                    t += timedelta(days=max(1, int(random.expovariate(1 / DAYS[prev]))))
                    history.append([i, "lost", t.date().isoformat()])
                break
            t += timedelta(days=max(1, int(random.expovariate(1 / DAYS[prev]))))
            history.append([i, nxt, t.date().isoformat()])

    with (OUT / "leads.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["lead_id", "channel", "advisor", "created_on"])
        w.writerows(leads)
    with (OUT / "stage_history.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["lead_id", "stage", "entered_on"])
        w.writerows(history)
    print(f"{len(leads)} leads, {len(history)} stage changes -> {OUT}")


if __name__ == "__main__":
    main()
