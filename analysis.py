"""Analyzes weekly test scores: finds students with strong progress and students with no progress."""
import numpy as np, pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/test_scores.csv")

def slope(g):
    return np.polyfit(g["week"], g["score"], 1)[0]  # score change per week

stats = df.groupby(["student_id", "group"]).apply(slope, include_groups=False).rename("weekly_progress").reset_index()
first = df[df.week <= 3].groupby("student_id").score.mean().rename("start_avg")
last = df[df.week >= 10].groupby("student_id").score.mean().rename("end_avg")
stats = stats.join(first, on="student_id").join(last, on="student_id")
stats["change"] = stats.end_avg - stats.start_avg

def label(x):
    if x >= 1.0: return "High progress (reward)"
    if x <= 0.2: return "No progress (needs support)"
    return "Steady progress"
stats["category"] = stats.weekly_progress.apply(label)
stats.round(2).to_csv("data/student_categories.csv", index=False)

summary = stats.category.value_counts()
print(summary)
print("\nAverage change in score by group:\n", stats.groupby("group").change.mean().round(1))

fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
summary.plot.barh(ax=ax[0], color=["#1f3a5f", "#7f9bc0", "#c0504d"][:len(summary)])
ax[0].set_title("Students by progress category"); ax[0].set_xlabel("Number of students")
avg = df.groupby("week").score.mean()
ax[1].plot(avg.index, avg.values, marker="o", color="#1f3a5f")
ax[1].set_title("Average score by week"); ax[1].set_xlabel("Week"); ax[1].set_ylabel("Score")
plt.tight_layout(); plt.savefig("images/results.png", dpi=150)
