from . import UrgeEventListener
from ..devices import PulseOutput

def applyFiringPattern(pulseOutputDevice, pulseConfiguration, dataHandler):
    ''' configure the given datahandler with respect to the configured firing pattern '''
    if ('firing_pattern' in pulseConfiguration['pulse'] and
        pulseConfiguration['pulse']['firing_pattern'] == PulseOutput.PulseFiringPattern.ON_URGE_RECORD):
        dataHandler.registerUrgeRecordListener(UrgeEventPulseSender(pulseOutputDevice))

class UrgeEventPulseTransformator:
    ''' descirbes how to transform the internal urge value to a parallel out pulse value '''
    def __init__(self, low, high):
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
    def __init__(self, pulseOutput):
        assert isinstance(pulseOutput, PulseOutput.PulseOutput)
        self.__pulseOutput = pulseOutput
        self.__transformator__ = UrgeEventPulseTransformator(1, 255)

    def onEvent(self, urgeValue, recTime, lag, buttons):
        self.__pulseOutput.setDataValue(self.__transformator__.transform(urgeValue))
        self.__pulseOutput.sendPulse()

    def close(self):
        pass
