from . import UrgeEventListener
from ..devices import PulseOutput

def applyFiringPattern(pulseOutputDevice, pulseConfiguration, dataHandler):
    ''' configure the given datahandler with respect to the configured firing pattern '''
    if ('firing_pattern' in pulseConfiguration['pulse'] and
        pulseConfiguration['pulse']['firing_pattern'] == PulseOutput.PulseFiringPattern.ON_URGE_RECORD):
        dataHandler.registerUrgeRecordListener(UrgeEventPulseSender(pulseOutputDevice))  

class UrgeEventPulseSender(UrgeEventListener.UrgeEventListener):
    ''' sends a pulse to the specified output device when a urge event occures '''
    def __init__(self, pulseOutput):
        assert isinstance(pulseOutput, PulseOutput.PulseOutput)
        self.__pulseOutput = pulseOutput

    def onEvent(self, urgeValue, recTime, lag, buttons):
        self.__pulseOutput.setDataValue(urgeValue)
        self.__pulseOutput.sendPulse()

    def close(self):
        pass
