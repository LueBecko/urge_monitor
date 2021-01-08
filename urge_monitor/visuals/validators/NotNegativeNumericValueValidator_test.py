import unittest
from .NotNegativeNumericValueValidator import NotNegativeNumericValueValidator

class NotNegativeNumericValueValidatorTest(unittest.TestCase):
    def setUp(self):
        self.validator = NotNegativeNumericValueValidator()

    def test_validate_positiveInteger_passes(self):
        self.validator.validate(123)

    def test_validate_positiveFloat_passes(self):
        self.validator.validate(123.4)

    def test_validate_zero_passes(self):
        self.validator.validate(0)
        self.validator.validate(0.0)

    def test_validate_invalideValues_raisesError(self):
        with self.assertRaises(AssertionError): self.validator.validate(None)
        with self.assertRaises(AssertionError): self.validator.validate('invalid')
        with self.assertRaises(AssertionError): self.validator.validate([])
        with self.assertRaises(AssertionError): self.validator.validate(())
        with self.assertRaises(AssertionError): self.validator.validate(-10)
        with self.assertRaises(AssertionError): self.validator.validate(-1000.0)

if __name__ == '__main__':
    unittest.main()
