from abc import ABC, abstractmethod

class AbstractValidator(ABC):
    '''abstract interface for validation classes'''
    @abstractmethod
    def validate(self, value):
        pass
