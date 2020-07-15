# -*- coding: utf-8 -*-

from psychopy import event
from psychopy.hardware import joystick
from psychopy.iohub.client import launchHubServer
joystick.backend = 'pyglet'


class InputDeviceAbstract(object):

    __deviceName = 'Device'

    def readValue(self):
        raise NotImplementedError('abstract')

    def getValue(self):
        raise NotImplementedError('abstract')


class InputDeviceMousePosAbs(InputDeviceAbstract):

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
        #urgevalue = min(1, max(0,
            #(p - self.__scale_bot) / self.__scale_range - 0.5))
        urgevalue = min(1, max(0,
            (self.p - self.__scale_bot) / self.__scale_range))
        return urgevalue

    def __del__(self):
        pass  # no deletion necessary


class InputDeviceMousePosRel(InputDeviceAbstract):

    __deviceName = 'MousePosRel'

    def __init__(self, win, sensitivity):
        self.__mouse = event.Mouse(visible=False, newPos=(0, 0), win=win)
        self.__pos = 0.5
        self.__stepWidth = sensitivity

    def readValue(self):
        pass

    def getValue(self):
        p = self.__mouse.getRel()[1]
        self.__pos = min(1.0, max(0.0, self.__pos + p * self.__stepWidth))
        return self.__pos

    def __del__(self):
        pass  # no deletion necessary


class InputDeviceMouseWheel(InputDeviceAbstract):

    __deviceName = 'MouseWheel'

    def __init__(self, win, sensitivity):
        self.__mouse = event.Mouse(visible=False, newPos=(0, 0), win=win)
        self.__pos = 0.5
        self.__stepWidth = sensitivity

    def readValue(self):
        pass

    def getValue(self):
        p = self.__mouse.getWheelRel()[1]
        self.__pos = min(1, max(0, self.__pos + p * self.__stepWidth))
        return self.__pos

    def __del__(self):
        pass  # no deletion necessary


class InputDeviceAuto(InputDeviceAbstract):

    __deviceName = 'Automatic'

    def __init__(self, sensitivity):
        self.__pos = 0.5
        self.__stepWidth = sensitivity
        self.__direction = 1.0

    def readValue(self):
        pass

    def getValue(self):
        self.__pos = self.__pos + self.__direction * self.__stepWidth
        if self.__pos >= 1.0:
            self.__pos = 1.0
            self.__direction = -1.0
        if self.__pos <= 0.0:
            self.__pos = 0.0
            self.__direction = 1.0
        return self.__pos

    def __del__(self):
        pass  # no deletion necessary


class InputDeviceJoystick(InputDeviceAbstract):

    __deviceName = 'Joystick'

    def __init__(self, name, sensitivity, axishat, channelid):
        self.__pos = 0.5
        self.__stepWidth = sensitivity
        Joysticks = {}
        nJoy = joystick.getNumJoysticks()
        for iJoy in range(nJoy):
            J = joystick.Joystick(iJoy)
            Joysticks[J.getName()] = iJoy
            J._device.close()
        #print Joysticks.keys()
        self.__joystick = joystick.Joystick(Joysticks[name])
        if axishat:
            self.__readValue = lambda self: self.readValueAxis()
            self.__deviceName += '_Axis' + str(channelid)
        else:
            self.__readValue = lambda self: self.readValueHat()
            self.__deviceName += '_Hat' + str(channelid)
        self.__channelid = channelid

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
        pass

    def getValue(self):
        self.__pos = self.__joystick.getAxis(self.__channelid)
        return self.__pos

    def __del__(self):
        pass  # no deletion necessary


class InputDeviceKeyboard(InputDeviceAbstract):

    __deviceName = 'Keyboard'
    lastKeys = set()
    keylist = []

    def __init__(self, sensitivity, key_up, key_down):
        self.keylist = [key_up, key_down]
        self.__sensitivity = sensitivity
        self.__pos = 0.5
        #self.lastKeys = set()

    def readValue(self):
        self.lastKeys.update(set(event.getKeys(keyList=self.keylist)))

    def getValue(self):
        if self.keylist[0] in self.lastKeys:
            self.__pos += self.__sensitivity
        if self.keylist[1] in self.lastKeys:
            self.__pos -= self.__sensitivity
        self.__pos = min(1.0, max(0.0, self.__pos))
        #event.clearEvents(eventType='keyboard')
        self.lastKeys = set()
        return self.__pos

    def __del__(self):
        pass  # no deletion necessary


class InputDeviceKeyboardHub(InputDeviceAbstract):

    __deviceName = 'KeyboardHub'
    lastKeys = dict()
    keylist = []

    def __init__(self, sensitivity, key_up, key_down):
        self.keylist = [key_up, key_down]
        self.__sensitivity = sensitivity
        self.__pos = 0.5
        # prepare iohub for recording
        self.__io = launchHubServer()
        self.__keyboard = self.__io.devices.keyboard
        self.__io.clearEvents('all')

    def readValue(self):
        self.lastKeys.update(self.__keyboard.state)
        #print self.lastKeys

    def getValue(self):
        if self.keylist[0] in self.lastKeys:
            self.__pos += self.__sensitivity
        if self.keylist[1] in self.lastKeys:
            self.__pos -= self.__sensitivity
        self.__pos = min(1.0, max(0.0, self.__pos))
        #event.clearEvents(eventType='keyboard')
        self.lastKeys = dict()
        return self.__pos

    def __del__(self):
        self.__io.shutdown()


def CreateInputDevice(C, win):
    #__assert_input__(C)
    device_creator = {
        'MousePosAbs':
            lambda: InputDeviceMousePosAbs(win=win),
        'MousePosRel':
            lambda: InputDeviceMousePosRel(win=win,
                sensitivity=C['sensitivity']),
        'MouseWheel':
            lambda: InputDeviceMouseWheel(win=win,
                sensitivity=C['sensitivity']),
        'Auto':
            lambda: InputDeviceAuto(sensitivity=C['sensitivity']),
        'Joystick':
            lambda: InputDeviceJoystick(
                name=C['name'], sensitivity=C['sensitivity'],
                axishat=C['axis_hat'], channelid=C['channel_id']),
        'JoystickAbs':
            lambda: InputDeviceJoystickAbs(
                name=C['name'], sensitivity=C['sensitivity'],
                channelid=C['channel_id']),
        'Keyboard':
            lambda: InputDeviceKeyboard(
                sensitivity=C['sensitivity'], key_up=C['key_up'],
                key_down=C['key_down']),
        'KeyboardHub':
            lambda: InputDeviceKeyboardHub(
                sensitivity=C['sensitivity'], key_up=C['key_up'],
                key_down=C['key_down']),
        }
    return device_creator[C['device']]()