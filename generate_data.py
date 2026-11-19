"""Generates a SYNTHETIC dataset: weekly test scores of 200 students over 12 weeks."""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
rows = []
for sid in range(1, 201):
    group = rng.choice(["A", "B", "C", "D"])
    base = rng.normal(55, 12)
    trend = rng.choice([-0.3, 0.0, 0.6, 1.5], p=[0.1, 0.35, 0.35, 0.2])  # points per week
    for week in range(1, 13):
        score = np.clip(base + trend * week + rng.normal(0, 5), 0, 100)
        rows.append((sid, group, week, round(score, 1)))
pd.DataFrame(rows, columns=["student_id", "group", "week", "score"]).to_csv("data/test_scores.csv", index=False)
print("saved data/test_scores.csv")
