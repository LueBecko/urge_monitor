
## needs python3, python3-venv and pip3

# create virtual environment
python3 -m venv .venv

# activate virtual environment
source .venv/bin/activate

# install psychopy via pip
# (note: this needs to load all dependencies for psychopy, which are a lot.
# This may cause pip to throw an error. Therefore installation is broken down in several smaller steps that pip can handle)
pip3 install numpy
pip3 install scipy
pip3 install pandas
pip3 install psychopy



