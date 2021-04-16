# Urge-Monitor

## What does it do?

Urge-Monitor is an experimental setup which meassures the urge associated with ticks as continouos self-report.

## How to run Urge-Monitor

Urge-Monitor builds onto PsychoPy3.

### Run on Linux

The provided script ```setup-environment.sh``` creates a virtual environment with all necessary dependencies.

The script ```run.sh``` starts the Urge-Monitor from the virtual environment.

### Run on Windows

Setup (Lübeck) 
 * install Psychopy (tested on [PsychoPy 2021.1.2](https://github.com/psychopy/psychopy/releases/tag/2021.1.2))
 * Check/adjust path to psychopy python in ```run.bat``` and ```run_dummy.bat``` (usually: ```"C:\Program Files\PsychoPy3\python.exe"```)

### Parallel Port drivers

Urge-Monitor supports sending pulses to exterior systems via parallel port (e.g. for EEG systems). It builds on the low latency PsychoPy solution.

To run an experiment with parallel port usage on a windows system you need it install one of the following drivers: ```inpout32```, ```inpoutx64``` or ```dlportio```.
