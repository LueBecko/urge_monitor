from . import UrgeEventListener
from ..devices import PulseOutput

def applyFiringPattern(pulseOutputDevice, pulseConfiguration, runConfiguration, dataHandler):
    ''' configure the given datahandler with respect to the configured firing pattern '''
    if ('firing_pattern' in pulseConfiguration['pulse'] and
        pulseConfiguration['pulse']['firing_pattern'] == PulseOutput.PulseFiringPattern.ON_URGE_RECORD):
        low = 1
        high = 255
        dataHandler.registerUrgeRecordListener(UrgeEventPulseSender(pulseOutputDevice, UrgeEventPulseTransformator(low, high)))

class UrgeEventPulseTransformator:
    ''' descirbes how to transform the internal urge value to a parallel out pulse value '''
    def __init__(self, low = 1, high = 255):
        # assert provided values
        assert isinstance(low, int)
        assert isinstance(high, int)
        assert low > 0
        assert high > low
        assert high < 256

        self.__low__ = low;
        self.__high__ = high;
        self.__range__ = high - low;

    def transform(self, urgevalue):
        return int(urgevalue * self.__range__) + self.__low__;    

class UrgeEventPulseSender(UrgeEventListener.UrgeEventListener):
    ''' sends a pulse to the specified output device when a urge event occures '''
    def __init__(self, pulseOutput, transformator = UrgeEventPulseTransformator(1, 255)):
        assert isinstance(pulseOutput, PulseOutput.PulseOutput)
        assert isinstance(transformator, UrgeEventPulseTransformator)
        self.__pulseOutput = pulseOutput
        self.__transformator__ = transformator

    def onEvent(self, urgeValue, recTime, lag, buttons):
        self.__pulseOutput.setDataValue(self.__transformator__.transform(urgeValue))
        self.__pulseOutput.sendPulse()

    def close(self):
        pass
