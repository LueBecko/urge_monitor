from psychopy import core
from psychopy import parallel

from enum import Enum
from abc import ABC, abstractmethod
from .validators import PulseOutputValidator

class PulseFiringPattern(Enum):
    ''' possible configurable firing patterns of outgoing pulses '''
    NONE = 0
    ON_URGE_RECORD = 1

class PulseOutput(ABC):
    '''use to send pulses'''

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
        self.__port__ = parallel.ParallelPort(address=self.__address__)
        self.__port__.setData(self.getDataValue())

    def sendPulse(self):
        self.__port__.setData(self.getDataValue())
        core.wait(secs=self.__duration__, hogCPUperiod=self.__duration__)
        self.__port__.setData(0)

class PulseOutputNone(PulseOutput):
    '''no pulse are send. Passive class for no out pulse configuration'''

    def __init__(self):
        self.__data__ = 0

    def initDevice(self):
        pass

    def sendPulse(self):
        pass

def createPulseOutput(pulseConfig):
    if pulseConfig['pulse']['send_out_pulse'] and not pulseConfig['pulse']['simulation']:
        return PulseOutputParallel(pulseConfig.get('out_pulse'))
    else:
        return PulseOutputNone()