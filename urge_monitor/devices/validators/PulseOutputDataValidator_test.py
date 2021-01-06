import unittest
from PulseOutputDataValidator import PulseOutputDataValidator

class PulseOutputDataValidatorTest(unittest.TestCase):
    def setUp(self):
        self.validator = PulseOutputDataValidator()

    def test_validate_withInvalidType_raises(self):
        with self.assertRaises(AssertionError): self.validator.validate(None)
        with self.assertRaises(AssertionError): self.validator.validate('something')
        with self.assertRaises(AssertionError): self.validator.validate(0.7777)
        with self.assertRaises(AssertionError): self.validator.validate([])
        with self.assertRaises(AssertionError): self.validator.validate({})

    def test_validate_withInvalidValue_raises(self):
        with self.assertRaises(AssertionError): self.validator.validate(-1)
        with self.assertRaises(AssertionError): self.validator.validate(-999)
        with self.assertRaises(AssertionError): self.validator.validate(256)
        with self.assertRaises(AssertionError): self.validator.validate(999)

    def test_validate_withValidValue_passes(self):
        self.validator.validate(0)
        self.validator.validate(1)
        self.validator.validate(10)
        self.validator.validate(100)
        self.validator.validate(200)
        self.validator.validate(255)

if __name__ == '__main__':
    unittest.main()
