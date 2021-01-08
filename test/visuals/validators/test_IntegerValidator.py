import unittest
from urge_monitor.visuals.validators.IntegerValidator import IntegerValidator

class IntegerValidatorTest(unittest.TestCase):
    def setUp(self):
        self.validator = IntegerValidator()

    def test_validate_withNonIntegers_raisesError(self):
        with self.assertRaises(AssertionError): self.validator.validate(None)
        with self.assertRaises(AssertionError): self.validator.validate(7.5)
        with self.assertRaises(AssertionError): self.validator.validate('None')
        with self.assertRaises(AssertionError): self.validator.validate([400])
        with self.assertRaises(AssertionError): self.validator.validate([400, 800, 3])

    def test_validate_withValidResolution_passes(self):
        self.validator.validate(400)
        self.validator.validate(0)
        self.validator.validate(-400)
        self.validator.validate((400))

if __name__ == '__main__':
    unittest.main()
