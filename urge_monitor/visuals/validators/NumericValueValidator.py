from .AbstractValidator import AbstractValidator

class NumericValueValidator(AbstractValidator):
    '''validates that a given value is numeric'''
    
    def validate(self, value):
        assert isinstance(value, (int, float))