#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Define the script filename
SCRIPT_NAME="main.py"

# Construct the path to the script file
SCRIPT_PATH="$SCRIPT_DIR/$SCRIPT_NAME"

# Check the OS and construct the command accordingly
if [ "$(uname)" == "Darwin" ]; then
    command="python3 $SCRIPT_PATH"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    command="python3 $SCRIPT_PATH"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    command="python $SCRIPT_PATH"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    command="python $SCRIPT_PATH"
else
    echo "Unsupported OS"
    exit 1
fi

# Run the command
eval "$command"
