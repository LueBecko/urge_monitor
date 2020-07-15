#!/bin/bash

## needs python3, python3-venv, pip3 and gtk+3.0 (libgtk-3-dev)

ENVIRONMENT_FOLDER=".venv"

# deactivate a present env first
deactivate

# checks if env already exists: is yes delete and rebuild
if [ -d "$ENVIRONMENT_FOLDER" ]; then
  python3 -m venv --clear "$ENVIRONMENT_FOLDER"
  rm -r "$ENVIRONMENT_FOLDER/"
fi

# create virtual environment
python3 -m venv "$ENVIRONMENT_FOLDER"

# activate virtual environment (set +x in case this was not set correctly by the setup)
activate () {
   . $ENVIRONMENT_FOLDER/bin/activate
}

chmod +x "$ENVIRONMENT_FOLDER/bin/activate"
activate

# install psychopy via pip
pip3 install psychopy

   pip3 install -U \
      -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04 \
      wxPython
      