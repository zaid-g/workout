import os
import time
import datetime

def ding():
    os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga&")

def start_next_set(i, exercise):
    if exercise == "warmup":
        print("*** Get ready! ***")
        return
    print(f"***{exercise} set {i + 1}. Go! ***")
    if i == 0:  # first set
        for i in range(4):
            ding()
            time.sleep(0.3)
    else:
        for i in range(2):
            ding()
            time.sleep(0.3)

workout = [["warmup", 50, 1], ["pullups", 180, 5], ["pushups", 180, 5], ["squats/planks", 180, 2]]
#workout = [["warmup", 2, 1], ["pullups", 4, 3], ["pushups", 4, 2], ["squats/planks", 4, 1]] # debug

ding()

new_exercise_flag = True
for i, exercise in enumerate(workout):
    ii = 0
    while ii < exercise[2]:
        if not new_exercise_flag:
            start_next_set(ii, exercise[0])
        else:
            start_next_set(ii, exercise[0])
        if i == len(workout) - 1 and ii == exercise[2] - 1:
            exit()
        time.sleep(exercise[1])
        ii += 1
        new_exercise_flag = False
    new_exercise_flag = True

# sleep so process ID is held until program termination
while True:
    time.sleep(10000)
