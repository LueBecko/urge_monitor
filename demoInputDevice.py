# -*- coding: utf-8 -*-

from psychopy import core, visual, gui
from urge_monitor import InputDevice

deviceDialog = gui.Dlg(title="Select InputDevice demo")
deviceDialog.addText('Make sure the selected device is present')
deviceDialog.addField('Device:', choices=['InputDeviceMousePosAbs',
                                   'InputDeviceMousePosRel',
                                   'InputDeviceMouseWheel',
                                   'InputDeviceAuto',
                                   'InputDeviceJoystick',
                                   'InputDeviceJoystickAbsolut',
                                   'InputDeviceKeyboard',
                                   'InputDeviceKeyboardHub'])
deviceDialog.show()  # show dialog and wait for OK or Cancel
if deviceDialog.OK:  # then the user pressed OK
    selectedDevice = str(deviceDialog.data[0])
    print("selected device: " + selectedDevice)

window = visual.Window()
valueLabel = visual.TextStim(window, text=str(0.5), color=(-1, -1, -1))

device_creator = {
    'InputDeviceMousePosAbs':
        lambda: InputDevice.InputDeviceMousePosAbs(window),
    'InputDeviceMousePosRel':
        lambda: InputDevice.InputDeviceMousePosRel(win=window, sensitivity=1),
    'InputDeviceMouseWheel':
        lambda: InputDevice.InputDeviceMouseWheel(win=window, sensitivity=0.01),
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

device = device_creator[selectedDevice]()

cl = core.Clock()
plotclock_increment = 1.0 / 10.0
plotclock = core.Clock()

uval = 0.5
while cl.getTime() <= 10.0:
    if plotclock.getTime() >= 0.0:  # update plot
        device.readValue()
        uval = device.getValue()
        valueLabel.setText(str(uval))
        plotclock.add(plotclock_increment)

    valueLabel.draw()
    window.flip()

window.close()
