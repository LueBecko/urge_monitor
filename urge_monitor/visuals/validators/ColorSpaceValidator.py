from .AbstractValidator import AbstractValidator

class ColorSpaceValidator(AbstractValidator):
    '''used to validate color space values'''

    def validate(self, value):
        assert isinstance(value, str)
        assert value.lower() in ['rgb', 'rgb255', 'hsv']
