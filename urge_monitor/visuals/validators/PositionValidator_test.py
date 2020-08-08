import unittest
from .PositionValidator import PositionValidator

class PositionValidatorTest(unittest.TestCase):
    def setUp(self):
        self.validator = PositionValidator()

    def test_validate_withInvalidPosition_raisesError(self):
        with self.assertRaises(AssertionError): self.validator.validate(None)
        with self.assertRaises(AssertionError): self.validator.validate(7)
        with self.assertRaises(AssertionError): self.validator.validate('None')
        with self.assertRaises(AssertionError): self.validator.validate([400])
        with self.assertRaises(AssertionError): self.validator.validate([400, 800, 3])
        with self.assertRaises(AssertionError): self.validator.validate([400, '800'])

    def test_validate_withValidPosition_passes(self):
        self.validator.validate([400, 800])
        self.validator.validate((400, 800))
        self.validator.validate((1.5, -6.3))

if __name__ == '__main__':
    unittest.main()
