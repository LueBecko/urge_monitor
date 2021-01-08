import unittest
from urge_monitor.visuals.validators.ResolutionValidator import ResolutionValidator

class ResolutionValidatorTest(unittest.TestCase):
    def setUp(self):
        self.validator = ResolutionValidator()

    def test_validate_withInvalidResolution_raisesError(self):
        with self.assertRaises(AssertionError): self.validator.validate(None)
        with self.assertRaises(AssertionError): self.validator.validate(7)
        with self.assertRaises(AssertionError): self.validator.validate('None')
        with self.assertRaises(AssertionError): self.validator.validate([400, 800, 3])
        with self.assertRaises(AssertionError): self.validator.validate([400, '800'])
        with self.assertRaises(AssertionError): self.validator.validate([400, 800.5])
        with self.assertRaises(AssertionError): self.validator.validate([400, -800])
        with self.assertRaises(AssertionError): self.validator.validate([-400, 800])
        with self.assertRaises(AssertionError): self.validator.validate([0, 800])
        with self.assertRaises(AssertionError): self.validator.validate([400, 0])

    def test_validate_withValidResolution_passes(self):
        self.validator.validate([400, 800])
        self.validator.validate((400, 800))
        self.validator.validate((400, 1))
        self.validator.validate((1, 1))

if __name__ == '__main__':
    unittest.main()
