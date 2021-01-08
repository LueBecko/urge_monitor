from .AbstractValidator import AbstractValidator
from .NumericValueValidator import NumericValueValidator

class PositiveNumericValueValidator(AbstractValidator):
    '''validates that a given value is numeric and positive'''

    def __init__(self):
        self.__numericValidator = NumericValueValidator()

    def validate(self, value):
        self.__numericValidator.validate(value)
        assert value > 0
