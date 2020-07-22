#!/bin/bash

ENVIRONMENT_FOLDER=".venv"

## setup python3 environment - Ubuntu style (needs sudo rights)
apt install libusb-1.0-0-dev portaudio19-dev libasound2-dev # sound suport for PTB bindings
apt install python3-venv
apt install python3-pip
apt install python3-pygame
apt install libgtk-3-dev

# deactivate a present venv first
#deactivate

# checks if env already exists: is yes delete and rebuild
if [ -d "$ENVIRONMENT_FOLDER" ]; then
  python3 -m venv --clear "$ENVIRONMENT_FOLDER"
  rm -r "$ENVIRONMENT_FOLDER/"
fi

# create virtual environment
#python3 -m venv "$ENVIRONMENT_FOLDER"

# activate virtual environment (set +x in case this was not set correctly by the setup)
activate () {
   . $ENVIRONMENT_FOLDER/bin/activate
}

#chmod +x "$ENVIRONMENT_FOLDER/bin/activate"
#activate

# install psychopy via pip
pip3 install psychopy

pip3 install -U \
   -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04 \
   wxPython

#pip3 install -U PTB
pip3 install psychtoolbox

# environement is also used in development, not neccessary fpr runtime
pip3 install -U pylint