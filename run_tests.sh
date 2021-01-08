#!/bin/bash

# activate virtual environment
activateVENV () {
   . $ENVIRONMENT_FOLDER/bin/activate
}

if [ -d "$ENVIRONMENT_FOLDER" ]; then
    activateVENV
fi

python3 -m unittest discover
