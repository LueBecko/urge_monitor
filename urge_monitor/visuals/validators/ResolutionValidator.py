from .AbstractValidator import AbstractValidator
from .PositiveNumericValueValidator import PositiveNumericValueValidator
from .IntegerValidator import IntegerValidator

class ResolutionValidator(AbstractValidator):
    '''used to validate Resolution Values'''

    def __init__(self):
        self.__positiveNumericValidator = PositiveNumericValueValidator()
        self.__integerValidator = IntegerValidator()

    def validate(self, value):
        assert isinstance(value, (list, tuple))
        assert len(value) == 2
        self.__integerValidator.validate(value[0])
        self.__integerValidator.validate(value[1])
        self.__positiveNumericValidator.validate(value[0])
        self.__positiveNumericValidator.validate(value[1])
