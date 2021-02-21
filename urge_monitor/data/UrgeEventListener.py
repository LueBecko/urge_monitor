from abc import ABC, abstractmethod

class UrgeEventListener(ABC):
    '''gets fired after an urge was recorded. Add any action you like'''
    @abstractmethod
    def onEvent(self, urgeValue, recTime, lag, buttons):
        pass

    @abstractmethod
    def close(self):
        pass
