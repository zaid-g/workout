import pandas as pd
import sys
import math
import time
import numpy as np
import datetime
from matplotlib import pyplot as plt
import json
import os

# %% -------- [functions] ----------:


def compute_exercise_groups(hist_sets, workout=None):
    """if workout=None, overall scores. if given non-null values, will match
    number of sets in each exercise to compute scores"""
    scores = pd.DataFrame(columns=["date", "person", "exercise", "score", "score_type"])
    grouped = list(hist_sets.groupby(["person", "exercise", "date"]))
    grouped = [
        group.sort_values(by="reps", ascending=False).reset_index()
        for _, group in grouped
    ]
    for group in grouped:
        if workout == None:
            magnitude = sum(group.reps**2) ** 0.5
            sum_ = sum(group.reps)
        else:
            exercise = group.loc[0, "exercise"]
            magnitude = sum(group.reps[0 : workout[exercise]] ** 2) ** 0.5
            sum_ = sum(group.reps[0 : workout[exercise]])
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
    exercise_groups = scores.groupby(["person", "exercise"])
    exercise_groups = [group.reset_index() for _, group in exercise_groups]
    return exercise_groups


def compute_weight_groups(hist_sets):
    weight_groups = hist_weights.groupby(["person"])
    weight_groups = [group.reset_index() for _, group in weight_groups]
    return weight_groups


def compute_target_reps_sum(exercise_groups, workout):
    targets = []
    for exercise_group in exercise_groups:
        person = exercise_group.person.iloc[0]
        exercise = exercise_group.exercise.iloc[0]
        max_score_sum = int(
            max(exercise_group[exercise_group.score_type == "sum"].score)
        )
        max_score_magnitude = max(
            exercise_group[exercise_group.score_type == "magnitude"].score
        )
        target_score_sum = max_score_sum + 1
        set_targets = [int(target_score_sum / workout[exercise])] * workout[exercise]
        remainder = target_score_sum % workout[exercise]
        for i in range(1, remainder + 1):
            set_targets[-i] += 1
        targets.append(
            (person, exercise, set_targets, max_score_sum, max_score_magnitude)
        )
    targets = pd.DataFrame(
        targets, columns=["person", "exercise", "reps", "sum", "magnitude"]
    ).sort_values(by=["person", "exercise"])
    return targets


# %% -------- [TUI] ----------:


exercises = {0: "pushups", 1: "pullups", 2: "squats", 3: "planks"}
# define workout (number of sets for each exercise)
workout = {"pushups": 5, "pullups": 5, "squats": 2, "planks": 2}
if len(sys.argv) == 2:
    if sys.argv[1] == "c" or sys.argv[1] == "C":  # cut
        workout = {"pushups": 3, "pullups": 3, "squats": 1, "planks": 1}

hist_sets = pd.read_csv("history_sets.csv")

# compute what needs to be achieved to beat max by 1 rep
target_reps = compute_target_reps_sum(
    compute_exercise_groups(hist_sets, workout), workout
)
print(
    f"\n*** Target Reps *** \n\n {target_reps[['person', 'exercise', 'reps']]}\n\n*** Let's go! ***\n"
)

hist_weights = pd.read_csv("history_weight.csv").drop_duplicates(
    ["date", "person"], keep="last"
)

today = str(datetime.date.today())
print(
    f"Insert weight example: `wz165` to insert for user z a weight of 165 lbs.\nInsert sets example: `0z5,10,3,4` for {exercises[0]}, user z (one character), and reps 5,10,3,4.\nEnter 's' to save & quit.\n{json.dumps(exercises, indent=4)}\n"
)
while True:
    try:
        x = input()
        if x == "s":
            try:
                os.system(
                    "paplay /usr/share/sounds/freedesktop/stereo/service-logout.oga&"
                )
            except:
                print("Audio playback not available")
            break
        if x[0] == "w":
            person = x[1].lower()
            assert person.isalpha()
            weight = float(x[2:])
            row = {
                "date": today,
                "person": person,
                "weight": weight,
            }
            hist_weights.loc[len(hist_weights)] = row
        else:
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
        # print("✅✅✅")
        try:
            os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga&")
        except:
            print("Audio playback not available")
    except KeyboardInterrupt:
        print("\nExiting without saving...")
        exit()
    except Exception as exc:
        print(f"❌❌❌ERROR: invalid format: {exc}")
        try:
            os.system("paplay /usr/share/sounds/freedesktop/stereo/suspend-error.oga&")
        except:
            print("Audio playback not available")

# write to history
hist_sets.sort_values(by=["date", "person", "exercise"], inplace=True)
hist_weights.sort_values(by=["date", "person"], inplace=True)
hist_sets.to_csv("history_sets.csv", index=False)
hist_weights.drop_duplicates(["date", "person"], keep="last").to_csv(
    "history_weight.csv", index=False
)


# %% -------- [plot set and weight groups] ----------:

exercise_groups = compute_exercise_groups(hist_sets)
weight_groups = compute_weight_groups(hist_weights)

fig, ax = plt.subplots(
    nrows=math.ceil((len(exercise_groups) + len(weight_groups)) ** 0.5),
    ncols=math.ceil((len(exercise_groups) + len(weight_groups)) ** 0.5),
    figsize=(12, 12),
)
ax_flat = ax.flatten()

# plot sets
for i, subplot in enumerate(exercise_groups):
    subsubplots = subplot.groupby("score_type")
    subsubplots = [group.reset_index() for _, group in subsubplots]
    for subsubplot in subsubplots:
        x = subsubplot.date
        y = subsubplot.score
        label = subsubplot.iloc[0].score_type
        ax_flat[i].plot(
            pd.to_datetime(x), y, "-.", marker="o", label=label, markersize=4
        )
        person = subsubplot.loc[0, "person"]
        exercise = subsubplot.loc[0, "exercise"]
        score_type = subsubplot.loc[0, "score_type"]
        # check to see if successfully beat max for workout
        if (
            y.iloc[-1]
            > target_reps[
                (target_reps["exercise"] == exercise)
                & (target_reps["person"] == person)
            ].iloc[0][score_type]
        ):
            ax_flat[i].plot(
                pd.to_datetime(x.iloc[-1]),
                y.iloc[-1],
                marker="*",
                color="g",
                markersize=11.5,
            )
    ax_flat[i].set_ylabel("score")
    ax_flat[i].title.set_text(f"{subplot.iloc[0].person}, {subplot.iloc[0].exercise}")
    ax_flat[i].grid(linestyle="-")
    ax_flat[i].legend(loc="upper left")
    ax_flat[i].tick_params(axis="x", rotation=90)

# plot weight
for i, subplot in enumerate(weight_groups):
    x = subplot.date
    y = subplot.weight
    label = "weight"
    ax_flat[i + len(exercise_groups)].plot(
        pd.to_datetime(x), y, "-.", marker="s", label=label
    )
    ax_flat[i + len(exercise_groups)].set_ylabel("weight")
    ax_flat[i + len(exercise_groups)].title.set_text(
        f"{subplot.iloc[0].person}, weight (lbs)"
    )
    ax_flat[i + len(exercise_groups)].grid(linestyle="-")
    ax_flat[i + len(exercise_groups)].legend(loc="upper left")
    ax_flat[i + len(exercise_groups)].tick_params(axis="x", rotation=90)

plt.tight_layout()
plt.savefig("figure.png")
try:
    os.system("firefox figure.png")
except:
    print("Firefox not available to view image <figure.png>. Image saved.")
