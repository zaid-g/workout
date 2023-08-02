import pandas as pd
import time
import numpy as np
import datetime
from matplotlib import pyplot as plt
import json
import os


hist = pd.read_csv("history.csv")

exercises = {0: "pushups", 1: "pullups", 2: "squats", 3: "planks"}

today = datetime.date.today()
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
            hist.loc[len(hist)] = row
        print("✅✅✅\n")
        os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga&")
    except KeyboardInterrupt:
        print("\nExiting without saving...")
        exit()
    except Exception as exc:
        print(f"❌❌❌ERROR: invalid format: {exc}")
        os.system("paplay /usr/share/sounds/freedesktop/stereo/suspend-error.oga&")

# write
hist.to_csv("history.csv", index=False)

# %% -------- [calculate score for each person and exercise] ----------:

scores = pd.DataFrame(columns=["date", "person", "exercise", "score", "score_type"])

grouped = list(hist.groupby(["person", "exercise", "date"]))
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


# %% -------- [plot results] ----------:

subplots = scores.groupby(["person", "exercise"])
subplots = [group.reset_index() for _, group in subplots]

plt.clf()
plt.cla()
fig, ax = plt.subplots(
    nrows=int(len(subplots) ** 0.5 + 1), ncols=int(len(subplots) ** 0.5 + 1), figsize=(12,12)
)
ax_flat = ax.flatten()

i = 0
for subplot in subplots:
    subsubplots = subplot.groupby("score_type")
    subsubplots = [group.reset_index() for _, group in subsubplots]
    for subsubplot in subsubplots:
        x = subsubplot.date
        y = subsubplot.score
        label = subsubplot.iloc[0].score_type
        ax_flat[i].plot(x, y,  '-.', label=label)
        ax_flat[i].set_ylabel("score")
        ax_flat[i].title.set_text(
            f"{subplot.iloc[0].person}, {subplot.iloc[0].exercise}"
        )
        ax_flat[i].legend(loc="upper left")
        ax_flat[i].grid(linestyle='-')
    i += 1

plt.tight_layout()
plt.savefig("figure.png")
os.system("firefox figure.png")
time.sleep(1)
os.system("rm figure.png")
