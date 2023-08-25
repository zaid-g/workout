#!/bin/bash

# Run the background job in the background (timer application)
python3 timer.py &

# Store the background job's process ID (PID)
bg_pid=$!

# Run the foreground job
python3 track.py

# terminate background job if finish (or ctrl-c)
kill -TERM $bg_pid
