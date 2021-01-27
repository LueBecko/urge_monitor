from psychopy import event
from psychopy.hardware import joystick
from psychopy.iohub import launchHubServer
from abc import ABC, abstractmethod
from psychopy import logging
joystick.backend = 'pyglet'


class InputDeviceAbstract(ABC):
    '''all input devices implement this interface
    Usage:
    * To be as precise as possible you have to call readValue when the time has come.
    * Further processing with the value (e.g. loggin and updating ui can then be done by accessing the read value with getValue.
    * The input device serves as a buffer until readValue is called again.
    '''

    __deviceName = 'Device'
    _startValue = 0.5

    @abstractmethod
    def readValue(self):
        '''read the current value from the specific input device'''
        pass

    @abstractmethod
    def getValue(self):
        '''access the read value from the specific input device'''
        pass

    def resetValue(self):
        '''reset value to start value (only relevant for relative devices)'''
        pass


class InputDeviceMousePosAbs(InputDeviceAbstract):
    '''interprets the absolute y position of the mouse with respect to the application window as input.'''

    __deviceName = 'MousePosAbs'

    def __init__(self, win):
        self.__mouse = event.Mouse(visible=False, newPos=(0, 0), win=win)
        wc = win.size.copy()  # is numpy array
        wc[1] = wc[1] / 2
        self.__scale_top = self.__mouse._pix2windowUnits(wc)[1]
        wc[1] = -wc[1]
        self.__scale_bot = self.__mouse._pix2windowUnits(wc)[1]
        self.__scale_range = self.__scale_top - self.__scale_bot

    def readValue(self):
        self.p = self.__mouse.getPos()[1]

    def getValue(self):
        # min max because of occasional overshoots
        urgevalue = min(1, max(0,
            (self.p - self.__scale_bot) / self.__scale_range))
        return urgevalue

    def __del__(self):
        pass  # no deletion necessary


class InputDeviceMousePosRel(InputDeviceAbstract):
    '''interprets the relative y position of the mouse with respect to the application window as input.'''

    __deviceName = 'MousePosRel'

    def __init__(self, win, sensitivity):
        self.__mouse = event.Mouse(visible=False, newPos=(0, 0), win=win)
        self.__stepWidth = sensitivity
        self.resetValue()

    def readValue(self):
        self.p = self.__mouse.getRel()[1]

    def getValue(self):
        self.__pos = min(1.0, max(0.0, self.__pos + self.p * self.__stepWidth))
        return self.__pos

    def resetValue(self):
        self.__pos = self._startValue
        self.__mouse.getRel()    # reset relative mouse position
        self.readValue()
        self.getValue()
        logging.info('Reset value, new value: %.2f / %.2f' % (self.p, self.__pos))

    def __del__(self):
        pass  # no deletion necessary


class InputDeviceMouseWheel(InputDeviceAbstract):
    '''interprets the vertical wheel of the mouse as input. Is bound by the sensitivity.'''

    __deviceName = 'MouseWheel'

    def __init__(self, win, sensitivity):
        self.__mouse = event.Mouse(visible=False, newPos=(0, 0), win=win)
        self.__stepWidth = sensitivity
        self.resetValue()

    def readValue(self):
        self.p = self.__mouse.getWheelRel()[1]

    def getValue(self):
        self.__pos = min(1, max(0, self.__pos + self.p * self.__stepWidth))
        return self.__pos

    def resetValue(self):
        self.__mouse.getRel()    # reset relative mouse position to avoid jump at start
        self.__pos = self._startValue

    def __del__(self):
        pass  # no deletion necessary


class InputDeviceAuto(InputDeviceAbstract):
    '''generates automatic input sequences. Good for testing purposes.'''

    __deviceName = 'Auto'

    def __init__(self, sensitivity):
        self.__stepWidth = sensitivity
        self.__direction = 1.0
        self.resetValue()

    def resetValue(self):
        self.__mouse.getRel()    # reset relative mouse position to avoid jump at start
        self.__pos = self._startValue

    def readValue(self):
        self.__pos = self.__pos + self.__direction * self.__stepWidth
        if self.__pos >= 1.0:
            self.__pos = 1.0
            self.__direction = -1.0
        if self.__pos <= 0.0:
            self.__pos = 0.0
            self.__direction = 1.0

    def getValue(self):
        return self.__pos

    def __del__(self):
        pass  # no deletion necessary


class InputDeviceJoystick(InputDeviceAbstract):
    '''interprets a specified joystick axis/hat position as vertical input. To guarantee reliable data, the device should be calibrate.'''

    __deviceName = 'Joystick'

    def __init__(self, name, sensitivity, axishat, channelid):
        self.__stepWidth = sensitivity
        Joysticks = {}
        nJoy = joystick.getNumJoysticks()
        for iJoy in range(nJoy):
            J = joystick.Joystick(iJoy)
            Joysticks[J.getName()] = iJoy
            J._device.close()
        self.__joystick = joystick.Joystick(Joysticks[name])
        if axishat:
            self.__readValue = lambda self: self.readValueAxis()
            self.__deviceName += '_Axis' + str(channelid)
        else:
            self.__readValue = lambda self: self.readValueHat()
            self.__deviceName += '_Hat' + str(channelid)
        self.__channelid = channelid
        self.resetValue()

    def resetValue(self):
        self.__mouse.getRel()    # reset relative mouse position to avoid jump at start
        self.__pos = self._startValue

    def readValue(self):
        pass

    def getValue(self):
        self.__readValue(self)

    def readValueAxis(self):
        self.__pos = self.__pos + (self.__stepWidth *
                     self.__joystick.getAxis(self.__channelid))
        return self.__pos

    def readValueHat(self):
        self.__pos = self.__pos + (self.__stepWidth *
                     self.__joystick.getHat(self.__channelid))
        return self.__pos

    def __del__(self):
        self.__joystick._device.close()


class InputDeviceJoystickAbs(InputDeviceAbstract):
    '''interprets a specified joystick axis/hat changes as vertical input. To guarantee reliable data, the device should be calibrate.'''

    __deviceName = 'JoystickAbsoluteAxis'

    def __init__(self, name, sensitivity, channelid):
        self.__pos = 0.5
        self.__stepWidth = sensitivity
        Joysticks = {}
        nJoy = joystick.getNumJoysticks()
        for iJoy in range(nJoy):
            J = joystick.Joystick(iJoy)
            Joysticks[J.getName()] = iJoy
            J._device.close()
        self.__joystick = joystick.Joystick(Joysticks[name])
        self.__deviceName += '_Axis' + channelid
        self.__channelid = channelid

    def readValue(self):
        self.__pos = self.__joystick.getAxis(self.__channelid)

    def getValue(self):
        return self.__pos

    def __del__(self):
        pass  # no deletion necessary


class InputDeviceKeyboard(InputDeviceAbstract):
    '''interprets a specified keyboard keys as positional changes.'''

    __deviceName = 'Keyboard'
    lastKeys = set()
    keylist = []

    def __init__(self, sensitivity, key_up, key_down):
        self.keylist = [key_up, key_down]
        self.__sensitivity = sensitivity
        self.resetValue()

    def resetValue(self):
        self.__mouse.getRel()    # reset relative mouse position to avoid jump at start
        self.__pos = self._startValue

    def readValue(self):
        self.lastKeys.update(set(event.getKeys(keyList=self.keylist)))

    def getValue(self):
        if self.keylist[0] in self.lastKeys:
            self.__pos += self.__sensitivity
        if self.keylist[1] in self.lastKeys:
            self.__pos -= self.__sensitivity
        self.__pos = min(1.0, max(0.0, self.__pos))
        self.lastKeys = set()
        return self.__pos

    def __del__(self):
        pass  # no deletion necessary


class InputDeviceKeyboardHub(InputDeviceAbstract):
    '''interprets a specified keyboard keys as positional changes. Uses the iohub for asynchronous recording.'''

    __deviceName = 'KeyboardHub'
    lastKeys = dict()
    keylist = []

    def __init__(self, sensitivity, key_up, key_down):
        self.keylist = [key_up, key_down]
        self.__sensitivity = sensitivity
        # prepare iohub for recording
        self.__io = launchHubServer()
        self.__keyboard = self.__io.devices.keyboard
        self.__io.clearEvents('all')

        self.resetValue()

    def resetValue(self):
        self.__mouse.getRel()    # reset relative mouse position to avoid jump at start
        self.__pos = self._startValue

    def readValue(self):
        self.lastKeys.update(self.__keyboard.state)

    def getValue(self):
        if self.keylist[0] in self.lastKeys:
            self.__pos += self.__sensitivity
        if self.keylist[1] in self.lastKeys:
            self.__pos -= self.__sensitivity
        self.__pos = min(1.0, max(0.0, self.__pos))
        self.lastKeys = dict()
        return self.__pos

    def __del__(self):
        self.__io.shutdown()


def CreateInputDevice(config, window):
    device_creator = {
        'MousePosAbs':
            lambda: InputDeviceMousePosAbs(win=window),
        'MousePosRel':
            lambda: InputDeviceMousePosRel(win=window,
                sensitivity=config['sensitivity']),
        'MouseWheel':
            lambda: InputDeviceMouseWheel(win=window,
                sensitivity=config['sensitivity']),
        'Auto':
            lambda: InputDeviceAuto(sensitivity=config['sensitivity']),
        'Joystick':
            lambda: InputDeviceJoystick(
                name=config['name'], sensitivity=config['sensitivity'],
                axishat=config['axis_hat'], channelid=config['channel_id']),
        'JoystickAbs':
            lambda: InputDeviceJoystickAbs(
                name=config['name'], sensitivity=config['sensitivity'],
                channelid=config['channel_id']),
        'Keyboard':
            lambda: InputDeviceKeyboard(
                sensitivity=config['sensitivity'], key_up=config['key_up'],
                key_down=config['key_down']),
        'KeyboardHub':
            lambda: InputDeviceKeyboardHub(
                sensitivity=config['sensitivity'], key_up=config['key_up'],
                key_down=config['key_down']),
        }
    return device_creator[config['device']]()