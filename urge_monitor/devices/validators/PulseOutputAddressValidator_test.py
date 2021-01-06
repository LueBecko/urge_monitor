import unittest
from PulseOutputAddressValidator import PulseOutputAddressValidator

class PulseOutputAddressValidatorTest(unittest.TestCase):
    def setUp(self):
        self.validator = PulseOutputAddressValidator()

    def test_validate_withInvalidType_raises(self):
        with self.assertRaises(AssertionError): self.validator.validate(None)
        with self.assertRaises(AssertionError): self.validator.validate('something')
        with self.assertRaises(AssertionError): self.validator.validate(7.3)
        with self.assertRaises(AssertionError): self.validator.validate([])
        with self.assertRaises(AssertionError): self.validator.validate({})

    def test_validate_withInvalidValue_raises(self):
        with self.assertRaises(AssertionError): self.validator.validate(-1)
        with self.assertRaises(AssertionError): self.validator.validate(-999)

    def test_validate_withValidValue_passes(self):
        self.validator.validate(1)
        self.validator.validate(999)
        self.validator.validate(0x3BC)

if __name__ == '__main__':
    unittest.main()
