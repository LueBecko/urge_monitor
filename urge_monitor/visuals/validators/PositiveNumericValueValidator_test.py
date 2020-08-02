import unittest
from .PositiveNumericValueValidator import PositiveNumericValueValidator

class PositiveNumericValueValidatorTest(unittest.TestCase):
    def test_validate_positiveInteger_passes(self):
        PositiveNumericValueValidator().validate(123)

    def test_validate_positiveFloat_passes(self):
        PositiveNumericValueValidator().validate(123.4)

    def test_validate_invalideValues_raisesError(self):
        validator = PositiveNumericValueValidator()
        with self.assertRaises(AssertionError): validator.validate(None)
        with self.assertRaises(AssertionError): validator.validate('invalid')
        with self.assertRaises(AssertionError): validator.validate([])
        with self.assertRaises(AssertionError): validator.validate(())
        with self.assertRaises(AssertionError): validator.validate(0)
        with self.assertRaises(AssertionError): validator.validate(0.0)
        with self.assertRaises(AssertionError): validator.validate(-10)
        with self.assertRaises(AssertionError): validator.validate(-1000.0)

if __name__ == '__main__':
    unittest.main()
