import os
import time

def start_set():
    for i in range(2):
        os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga&")
        time.sleep(0.3)

def start_exercise():
    for i in range(4):
        os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga&")
        time.sleep(0.3)

workout = [["pullups", 180, 5], ["pushups", 180, 5], ["squats/planks", 180, 2]]
# workout = [["pullups", 4, 2], ["pushups", 4, 2], ["squats/planks", 4, 1]] # debug

time.sleep(30)

new_exercise_flag = True
for i, exercise in enumerate(workout):
    while exercise[2] > 0:
        if not new_exercise_flag:
            start_set()
        else:
            start_exercise()
        if i == len(workout) - 1 and exercise[2] == 1:
            exit()
        time.sleep(exercise[1])
        exercise[2] -= 1
        new_exercise_flag = False
    new_exercise_flag = True
