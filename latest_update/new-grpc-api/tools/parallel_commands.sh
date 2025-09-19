#!/bin/bash

# execute multiple commands at once
# source: https://stackoverflow.com/a/10909842

# Default is to print process names
print=true

# Check if first arg is -q
if [[ "$1" == "-q" ]]; then
    print=false
    shift # remove the -q from the arguments list
fi

if [[ "$print" == true ]]; then
    echo "Executing commands in parallel"
fi

# execute multiple commands at once
for cmd in "$@"; do {
    if [[ "$print" == true ]]; then
        echo "Process \"$cmd\" started"
    fi
    eval $cmd & pid=$!
    PID_LIST+=" $pid"
} done

trap "kill $PID_LIST" SIGINT

if [[ "$print" == true ]]; then
    echo "Parallel processes have started"
fi

wait $PID_LIST

echo

if [[ "$print" == true ]]; then
    echo "All processes have completed";
fi
