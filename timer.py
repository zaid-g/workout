import os
import time

def start_set():
    for i in range(3):
        os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga&")
        time.sleep(0.3)

def start_exercise():
    for i in range(1):
        os.system("paplay /usr/share/sounds/freedesktop/stereo/phone-outgoing-busy.oga&")
        time.sleep(0.3)

#workout = [["pullups", 4, 4], ["pushups", 4, 4], ["squats/planks", 4, 2]] # debug
workout = [["pullups", 180, 5], ["pushups", 180, 5], ["squats/planks", 180, 2]]

new_exercise_flag = True
for exercise in workout:
    while exercise[2] > 0:
        if not new_exercise_flag:
            start_set()
        else:
            start_exercise()
        time.sleep(exercise[1])
        exercise[2] -= 1
        new_exercise_flag = False
    new_exercise_flag = True
