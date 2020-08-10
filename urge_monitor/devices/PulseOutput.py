from psychopy import core
from psychopy import parallel
from psychopy import logging

from abc import ABC, abstractmethod

class PulseOutput(ABC):
    '''use to send send pulses'''
    @abstractmethod
    def initDevice(self):
        '''initialize the specified device'''
        pass

    @abstractmethod
    def sendPulse(self):
        '''send a pulse'''
        pass

class PulseOutputParallel(PulseOutput):
    '''send pulses via parallel port'''

    def __init__(self, config):
        self.__address__ = config['out_pulse']['address']
        self.__data__ = config['out_pulse']['data']
        self.__duration__ = config['out_pulse']['duration']

    def initDevice(self):
        self.__port__ = parallel.ParallelPort(address=self.__address__)
        self.__port__.setData(0)

    def sendPulse(self):
        self.__port__.setData(self.__data__)
        core.wait(secs=self.__duration__, hogCPUperiod=self.__duration__)
        self.__port__.setData(0)

class PulseOutputSimulation(PulseOutput):
    '''simulates sending pulses for testing purpose. Simulated pulses are written to log'''

    def __init__(self, config):
        self.__data__ = config['out_pulse']['data']

    def initDevice(self):
        pass

    def sendPulse(self):
        logging.info("sending simulated pulse with data " + str(self.__data__))

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