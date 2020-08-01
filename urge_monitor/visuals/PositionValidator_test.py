import unittest
from . import helpers

class PositionValidatorTest(unittest.TestCase):
    def test_validatePosition_withInvalidPosition_raisesError(self):
        validator = helpers.PositionValidator()
        with self.assertRaises(AssertionError): validator.validatePosition(None)
        with self.assertRaises(AssertionError): validator.validatePosition(7)
        with self.assertRaises(AssertionError): validator.validatePosition('None')
        with self.assertRaises(AssertionError): validator.validatePosition([400])
        with self.assertRaises(AssertionError): validator.validatePosition([400, 800, 3])
        with self.assertRaises(AssertionError): validator.validatePosition([400, '800'])

    def test_validatePosition_withValidPosition_passes(self):
        validator = helpers.PositionValidator()
        validator.validatePosition([400, 800])
        validator.validatePosition((400, 800))
        validator.validatePosition((1.5, -6.3))

if __name__ == '__main__':
    unittest.main()
