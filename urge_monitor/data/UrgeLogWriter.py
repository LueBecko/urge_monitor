from .UrgeEventListener import UrgeEventListener
from psychopy import logging

class UrgeLogWriter(UrgeEventListener):
    ''' writes every recorded urge event to the main log '''

    def onEvent(self, urgeValue, recTime, lag, buttons):
        logging.info("recording urge with data " + str(urgeValue))

    def close(self):
        pass
