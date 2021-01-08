import unittest
from urge_monitor.devices.validators.PulseOutputDurationValidator import PulseOutputDurationValidator

class PulseOutputDurationValidatorTest(unittest.TestCase):
    def setUp(self):
        self.validator = PulseOutputDurationValidator()

    def test_validate_withInvalidType_raises(self):
        with self.assertRaises(AssertionError): self.validator.validate(None)
        with self.assertRaises(AssertionError): self.validator.validate('something')
        with self.assertRaises(AssertionError): self.validator.validate([])
        with self.assertRaises(AssertionError): self.validator.validate({})

    def test_validate_withInvalidValue_raises(self):
        with self.assertRaises(AssertionError): self.validator.validate(0)
        with self.assertRaises(AssertionError): self.validator.validate(0.0)
        with self.assertRaises(AssertionError): self.validator.validate(-0.001)
        with self.assertRaises(AssertionError): self.validator.validate(-1)
        with self.assertRaises(AssertionError): self.validator.validate(-999)

    def test_validate_withValidValue_passes(self):
        self.validator.validate(1)
        self.validator.validate(999)
        self.validator.validate(0.001)
        self.validator.validate(1.555)

if __name__ == '__main__':
    unittest.main()
