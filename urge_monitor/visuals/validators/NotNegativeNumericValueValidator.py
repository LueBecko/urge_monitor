from .AbstractValidator import AbstractValidator
from .NumericValueValidator import NumericValueValidator

class NotNegativeNumericValueValidator(AbstractValidator):
    '''validates that a given value is numeric and positive or zero'''

    def __init__(self):
        self.__numericValidator = NumericValueValidator()

    def validate(self, value):
        self.__numericValidator.validate(value)
        assert value >= 0
