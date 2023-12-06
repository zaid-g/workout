import os
import sys
import time
import datetime

def ding():
    try:
        os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga&")
    except:
        print("Audio playback not available")

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

workout = [["warmup", 180, 1], ["pullups", 180, 5], ["pushups", 180, 5], ["squats/planks", 180, 2]]
if len(sys.argv) == 2:
    if sys.argv[1] == 'c'or sys.argv[1] == 'C': # cut
        workout = [["warmup", 180, 1], ["pullups", 180, 3], ["pushups", 180, 3], ["squats/planks", 180, 1]]
#workout = [["warmup", 2, 1], ["pullups", 4, 3], ["pushups", 4, 2], ["squats/planks", 4, 1]] # debug
#workout = [["warmup", 2, 1], ["pullups", 4, 3]] # debug
#workout = [["warmup", 2, 1]] # debug

ding()
print(workout)

new_exercise_flag = True
for i, exercise in enumerate(workout):
    ii = 0
    while ii < exercise[2]:
        if not new_exercise_flag:
            start_next_set(ii, exercise[0])
        else:
            start_next_set(ii, exercise[0])
        if i == len(workout) - 1 and ii == exercise[2] - 1:
            break
        time.sleep(exercise[1])
        ii += 1
        new_exercise_flag = False
    new_exercise_flag = True

print("\n\nCompleted workout!")

# sleep so PID is held until program termination, to not risk terminating an innocent process
while True:
    time.sleep(1000000)
