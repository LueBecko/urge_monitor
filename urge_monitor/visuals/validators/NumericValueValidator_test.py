import unittest
from .NumericValueValidator import NumericValueValidator

class NumericValueValidatorTest(unittest.TestCase):
    def test_validate_integer_passes(self):
        NumericValueValidator().validate(123)

    def test_validate_float_passes(self):
        NumericValueValidator().validate(123.4)

    def test_validate_invalideValues_raisesError(self):
        validator = NumericValueValidator()
        with self.assertRaises(AssertionError): validator.validate(None)
        with self.assertRaises(AssertionError): validator.validate('invalid')
        with self.assertRaises(AssertionError): validator.validate([])
        with self.assertRaises(AssertionError): validator.validate(())

if __name__ == '__main__':
    unittest.main()
