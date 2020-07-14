# -*- coding: utf-8 -*-

import sys
sys.path.append('../urge_report_fmri')
import InputDevice

from psychopy import core, visual, gui

myDlg = gui.Dlg(title="Select InputDevice test")
myDlg.addText('Make sure the selected device is present')
myDlg.addField('Device:', choices=['InputDeviceMousePosAbs',
                                   'InputDeviceMousePosRel',
                                   'InputDeviceMouseWheel',
                                   'InputDeviceAuto',
                                   'InputDeviceJoystick',
                                   'InputDeviceJoystickAbsolut',
                                   'InputDeviceKeyboard',
                                   'InputDeviceKeyboardHub'])
myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # then the user pressed OK
    thisInfo = myDlg.data
    print(thisInfo)

win = visual.Window()
ts = visual.TextStim(win, text=str(0.5), color=(-1, -1, -1))

device_creator = {
    'InputDeviceMousePosAbs':
        lambda: InputDevice.InputDeviceMousePosAbs(win),
    'InputDeviceMousePosRel':
        lambda: InputDevice.InputDeviceMousePosRel(win=win, sensitivity=1),
    'InputDeviceMouseWheel':
        lambda: InputDevice.InputDeviceMouseWheel(win=win, sensitivity=0.01),
    'InputDeviceAuto':
        lambda: InputDevice.InputDeviceAuto(sensitivity=0.01),
    'InputDeviceJoystick':
        lambda: InputDevice.InputDeviceJoystick(
            name='Jess Tech Dual Analog Pad',
            sensitivity=1, axishat=True, channelid=0),
    'InputDeviceKeyboard':
        lambda: InputDevice.InputDeviceKeyboard(sensitivity=0.01,
            key_up='up', key_down='down'),
    'InputDeviceKeyboardHub':
        lambda: InputDevice.InputDeviceKeyboardHub(sensitivity=0.01,
            key_up='up', key_down='down')
    }

dev = device_creator[str(thisInfo[0])]()

cl = core.Clock()
plotclock_increment = 1.0 / 10.0
plotclock = core.Clock()

uval = 0.5
while cl.getTime() <= 10.0:
    if plotclock.getTime() >= 0.0:  # update plot
        uval = dev.readValue()
        ts.setText(str(uval))
        plotclock.add(plotclock_increment)

    ts.draw()
    win.flip()

win.close()
