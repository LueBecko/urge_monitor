#!/bin/bash

# activate virtual environment
activateVENV () {
   . $ENVIRONMENT_FOLDER/bin/activate
}

if [ -d "$ENVIRONMENT_FOLDER" ]; then
    activateVENV
fi

cd urge_monitor
python3 RunExperiment.py
