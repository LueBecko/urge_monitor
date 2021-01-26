# -*- coding: utf-8 -*-

from psychopy.iohub import launchHubServer
from . import InputDevice

class InputListener:
    '''listener for input device events. Allows registration specific input events/key presses to listen to'''

    def __init__(self, configuration, window):
        self.__device = InputDevice.CreateInputDevice(configuration, window)
        self.__isKeyboard__ = str(configuration['device']).lower().startswith('keyboard')
        # prepare keyboard for reading other keys
        self.__keyList__ = []
        self.__lastKeys__ = []
        self.__keyInd__ = {}
        self.__keyBuf__ = []
        if self.__isKeyboard__:
            self.RegisterKey(configuration['key_up'])
            self.RegisterKey(configuration['key_down'])
        else:
            self.__io__ = launchHubServer()
            self.__keyboard = self.__io__.devices.keyboard #?
            self.__io__.clearEvents(b'all')                #?

    def __del__(self):
        if not self.__isKeyboard__:
            self.__io__.quit()

    def ReadUrge(self):
        self.__device.readValue()
        if self.__isKeyboard__:
            #?for key in self.__device.lastKeys:
            #?    self.__keyBuf__[self.__keyInd__[key]] = 1
            self.__lastKeys__ = self.__device.lastKeys #?
        else:
            #self.__lastKeys__ = [k for k in self.__keyList__
            #    if k in self.__io__.devices.keyboard.state]
            #for key in self.__lastKeys__:
            #    self.__keyBuf__[self.__keyInd__[key]] = 1
            self.__lastKeys__ = {k: self.__keyboard.state[k]
                                 for k in self.__keyList__ if k in self.__keyboard.state}

        for key in self.__lastKeys__:
             self.__keyBuf__[self.__keyInd__[key]] = 1

    def GetUrge(self):
        return self.__device.getValue()

    def RegisterKey(self, key):
        if self.__isKeyboard__:
            self.__device.keylist.append(key)
        self.__keyList__.append(key)
        self.__keyInd__[key] = len(self.__keyList__) - 1
        self.__keyBuf__ = [0] * len(self.__keyList__)

    def UnregisterKey(self, key):
        try:  # to avoid error if key is not in list
            if self.__isKeyboard__:
                self.__device.keylist.remove(key)
            else:
                self.__keyList__.remove(key)
            # rebuild keyInd
            self.__keyInd__ = {}
            for i in range(len(self.__keyList__)):
                self.__keyInd__[self.__keyList__[i]] = i
            self.__keyBuf__ = [0] * len(self.__keyList__)
        except:
            pass

    def GetPressedKeys(self):
        if self.__isKeyboard__:
            return self.__device.lastKeys
        else:
            return self.__lastKeys__

    def GetBufferedKeys(self):
        buf = self.__keyBuf__
        self.__keyBuf__ = [0] * len(self.__keyList__)
        return buf
