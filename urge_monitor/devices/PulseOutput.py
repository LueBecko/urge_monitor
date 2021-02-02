from psychopy import core
from psychopy import parallel
from psychopy import logging

from enum import Enum
from abc import ABC, abstractmethod
from .validators import PulseOutputValidator

class PulseFiringPattern(Enum):
    ''' possible configurable firing patterns of outgoing pulses '''
    NONE = 0
    ON_URGE_RECORD = 1

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
        PulseOutputValidator.PulseOutputParallelValidator().validate(config)

        self.__address__ = config['address']
        self.setDataValue(config['data'])
        self.__duration__ = config['duration']

    def initDevice(self):
        logging.info("initialising parallel out-pulse device (initial data = " + str(self.getDataValue()) + ")")
        self.__port__ = parallel.ParallelPort(address=self.__address__)
        self.__port__.setData(self.getDataValue())

    def sendPulse(self):
        logging.info("sending pulse with data " + str(self.getDataValue()))
        self.__port__.setData(self.getDataValue())
        core.wait(secs=self.__duration__, hogCPUperiod=self.__duration__)
        self.__port__.setData(0)

class PulseOutputSimulation(PulseOutput):
    '''simulates sending pulses for testing purpose. Simulated pulses are written to log'''

    def __init__(self, config):
        PulseOutputValidator.PulseOutputSimulationValidator().validate(config)

        self.setDataValue(config['data'])

    def initDevice(self):
        logging.info("initialising simulation out-pulse device (initial data = " + str(self.getDataValue()) + ")")

    def sendPulse(self):
        logging.info("sending simulated pulse with data " + str(self.getDataValue()))

class PulseOutputNone(PulseOutput):
    '''no pulse are send. Passive class for no out pulse configuration'''

    def __init__(self):
        self.__data__ = 0

    def initDevice(self):
        pass

    def sendPulse(self):
        pass

def createPulseOutput(pulseConfig):
    if pulseConfig['pulse']['send_out_pulse']:
        if pulseConfig['pulse']['simulation']:
            return PulseOutputSimulation(pulseConfig.get('out_pulse'))
        else:
            return PulseOutputParallel(pulseConfig.get('out_pulse'))
    else:
        return PulseOutputNone()