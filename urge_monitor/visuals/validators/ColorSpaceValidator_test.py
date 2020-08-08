import unittest
from .ColorSpaceValidator import ColorSpaceValidator

class ColorSpaceValidatorTest(unittest.TestCase):
    def setUp(self):
        self.validator = ColorSpaceValidator()

    def test_validate_withInvalidColorSpace_raises(self):
        with self.assertRaises(AssertionError): self.validator.validate(None)
        with self.assertRaises(AssertionError): self.validator.validate(7)
        with self.assertRaises(AssertionError): self.validator.validate('None')

    def test_validate_withValidColorSpace_passes(self):
        self.validator.validate('rgb')
        self.validator.validate('rgb255')
        self.validator.validate('hsv')
        self.validator.validate('RGB')
        self.validator.validate('rGb255')
        self.validator.validate('HsV')

if __name__ == '__main__':
    unittest.main()
