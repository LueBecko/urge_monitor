from .AbstractValidator import AbstractValidator
from .NumericValueValidator import NumericValueValidator
from .IntegerValidator import IntegerValidator

class PositionValidator(AbstractValidator):
    '''used to validate position Values'''

    def __init__(self):
        self.__numericValidator = NumericValueValidator()

    def validate(self, value):
        assert isinstance(value, (list, tuple))
        assert len(value) == 2
        self.__numericValidator.validate(value[0])
        self.__numericValidator.validate(value[1])
