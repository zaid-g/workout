#!/bin/bash

# Run the background job in the background (timer application)
python3 timer.py &

# Store the background job's process ID (PID)
bg_pid=$!

# Define a function to clean up the background job
cleanup() {
    echo "Ctrl+C detected."
    echo "Canceling the timer program..."
    kill -TERM $bg_pid
    exit 1
}

# Set up a trap to call the cleanup function on Ctrl+C
trap cleanup INT

# Run the foreground job
python3 track.py
