from .AbstractValidator import AbstractValidator

class IntegerValidator(AbstractValidator):
    '''used to validate if value is a int'''

    def validate(self, value):
        assert isinstance(value, int)
