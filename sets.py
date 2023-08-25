import pandas as pd
import math
import time
import numpy as np
import datetime
from matplotlib import pyplot as plt
import json
import os


hist_sets = pd.read_csv("history_sets.csv")
hist_weight = pd.read_csv("history_weight.csv")

exercises = {0: "pushups", 1: "pullups", 2: "squats", 3: "planks"}

today = str(datetime.date.today())
while True:
    try:
        x = input(
            f"Example format: `0z5,10,3,4` for {exercises[0]}, user z, and reps 5,10,3,4.\nEnter 's' to save & quit.\n{json.dumps(exercises, indent=4)}\n"
        )
        if x == "s":
            os.system("paplay /usr/share/sounds/freedesktop/stereo/service-logout.oga&")
            break
        exercise = exercises[int(x[0])]
        person = x[1].lower()
        assert person.isalpha()
        reps = x[2:]
        reps = reps.split(",")
        reps = [int(rep) for rep in reps]
        for rep in reps:
            row = {
                "date": today,
                "person": person,
                "exercise": exercise,
                "reps": rep,
            }
            hist_sets.loc[len(hist_sets)] = row
        print("✅✅✅\n")
        os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga&")
    except KeyboardInterrupt:
        print("\nExiting without saving...")
        exit()
    except Exception as exc:
        print(f"❌❌❌ERROR: invalid format: {exc}")
        os.system("paplay /usr/share/sounds/freedesktop/stereo/suspend-error.oga&")

# write
hist_sets.sort_values(by=["date", "person", "exercise"], inplace=True)
hist_weight.sort_values(by=["date", "person"], inplace=True)
hist_sets.to_csv("history_sets.csv", index=False)
hist_weight.to_csv("history_weight.csv", index=False)

# %% -------- [calculate score for each person and exercise] ----------:

scores = pd.DataFrame(columns=["date", "person", "exercise", "score", "score_type"])

grouped = list(hist_sets.groupby(["person", "exercise", "date"]))
grouped = [group.reset_index() for _, group in grouped]

for group in grouped:
    magnitude = sum(group.reps**2) ** 0.5
    sum_ = sum(group.reps)
    scores.loc[len(scores)] = {
        "date": group.iloc[0].date,
        "person": group.iloc[0].person,
        "exercise": group.iloc[0].exercise,
        "score": magnitude,
        "score_type": "magnitude",
    }
    scores.loc[len(scores)] = {
        "date": group.iloc[0].date,
        "person": group.iloc[0].person,
        "exercise": group.iloc[0].exercise,
        "score": sum_,
        "score_type": "sum",
    }


# %% -------- [plot] ----------:

weight_subplots = hist_weight.groupby(["person"])
weight_subplots = [group.reset_index() for _, group in weight_subplots]
sets_subplots = scores.groupby(["person", "exercise"])
sets_subplots = [group.reset_index() for _, group in sets_subplots]

fig, ax = plt.subplots(
    nrows=math.ceil((len(sets_subplots) + len(weight_subplots)) ** 0.5),
    ncols=math.ceil((len(sets_subplots) + len(weight_subplots)) ** 0.5),
    figsize=(12, 12),
)
ax_flat = ax.flatten()

# plot sets
for i, subplot in enumerate(sets_subplots):
    subsubplots = subplot.groupby("score_type")
    subsubplots = [group.reset_index() for _, group in subsubplots]
    for subsubplot in subsubplots:
        x = subsubplot.date
        y = subsubplot.score
        label = subsubplot.iloc[0].score_type
        if y.iloc[-1] == max(y):
            ax_flat[i].plot(pd.to_datetime(x.iloc[:-1]), y.iloc[:-1], "-.", marker="s", label=label)
            ax_flat[i].plot(pd.to_datetime(x.iloc[-1]), y.iloc[-1], marker="*", color='g', markersize=11.0)
        else:
            ax_flat[i].plot(pd.to_datetime(x), y, "-.", marker="s", label=label)
    ax_flat[i].set_ylabel("score")
    ax_flat[i].title.set_text(f"{subplot.iloc[0].person}, {subplot.iloc[0].exercise}")
    ax_flat[i].grid(linestyle="-")
    ax_flat[i].legend(loc="upper left")
    ax_flat[i].tick_params(axis="x", rotation=90)

# plot weight
for i, subplot in enumerate(weight_subplots):
    x = subplot.date
    y = subplot.weight
    label = "weight"
    ax_flat[i + len(sets_subplots)].plot(
        pd.to_datetime(x), y, "-.", marker="s", label=label
    )
    ax_flat[i + len(sets_subplots)].set_ylabel("weight")
    ax_flat[i + len(sets_subplots)].title.set_text(f"{subplot.iloc[0].person}, weight (lbs)")
    ax_flat[i + len(sets_subplots)].grid(linestyle="-")
    ax_flat[i + len(sets_subplots)].legend(loc="upper left")
    ax_flat[i + len(sets_subplots)].tick_params(axis="x", rotation=90)

plt.tight_layout()
plt.savefig("figure.png")
os.system("firefox figure.png")
time.sleep(1)
os.system("rm figure.png")
