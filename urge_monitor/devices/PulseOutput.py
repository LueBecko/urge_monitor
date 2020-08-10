from psychopy import core
from psychopy import parallel
from psychopy import logging

from abc import ABC, abstractmethod

class PulseOutput(ABC):
    '''use to send send pulses'''

    __data__: 0

    @abstractmethod
    def initDevice(self):
        '''initialize the specified device'''
        pass

    @abstractmethod
    def sendPulse(self):
        '''send a pulse'''
        pass

    def setDataValue(self, value):
        self.__data__ = value

    def getDataValue(self):
        return self.__data__

class PulseOutputParallel(PulseOutput):
    '''send pulses via parallel port'''

    def __init__(self, config):
        self.__address__ = config['out_pulse']['address']
        self.setDataValue(config['out_pulse']['data'])
        self.__duration__ = config['out_pulse']['duration']

    def initDevice(self):
        self.__port__ = parallel.ParallelPort(address=self.__address__)
        self.__port__.setData(0)

    def sendPulse(self):
        self.__port__.setData(self.getDataValue())
        core.wait(secs=self.__duration__, hogCPUperiod=self.__duration__)
        self.__port__.setData(0)

class PulseOutputSimulation(PulseOutput):
    '''simulates sending pulses for testing purpose. Simulated pulses are written to log'''

    def __init__(self, config):
        self.setDataValue(config['out_pulse']['data'])

    def initDevice(self):
        pass

    def sendPulse(self):
        logging.info("sending simulated pulse with data " + str(self.getDataValue()))

class PulseOutputNone(PulseOutput):
    '''no pulse are send. Passive class for no out pulse configuration'''
    def initDevice(self):
        pass

    def sendPulse(self):
        pass

def createPulseOutput(pulseConfig):
    if pulseConfig['pulse']['send_out_pulse']:
        if pulseConfig['pulse']['simulation']:
            return PulseOutputSimulation(pulseConfig)
        else:
            return PulseOutputParallel(pulseConfig)
    else:
        return PulseOutputNone()