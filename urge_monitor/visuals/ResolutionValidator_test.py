import unittest
from . import helpers

class ResolutionValidatorTest(unittest.TestCase):
    def test_validateResolution_withInvalidResolution_raisesError(self):
        validator = helpers.ResolutionValidator()
        with self.assertRaises(AssertionError): validator.validateResolution(None)
        with self.assertRaises(AssertionError): validator.validateResolution(7)
        with self.assertRaises(AssertionError): validator.validateResolution('None')
        with self.assertRaises(AssertionError): validator.validateResolution([400, 800, 3])
        with self.assertRaises(AssertionError): validator.validateResolution([400, '800'])
        with self.assertRaises(AssertionError): validator.validateResolution([400, 800.5])
        with self.assertRaises(AssertionError): validator.validateResolution([400, -800])
        with self.assertRaises(AssertionError): validator.validateResolution([-400, 800])
        with self.assertRaises(AssertionError): validator.validateResolution([0, 800])
        with self.assertRaises(AssertionError): validator.validateResolution([400, 0])

    def test_validateResolution_withValidResolution_passes(self):
        validator = helpers.ResolutionValidator()
        validator.validateResolution([400, 800])
        validator.validateResolution((400, 800))
        validator.validateResolution((400, 1))
        validator.validateResolution((1, 1))

if __name__ == '__main__':
    unittest.main()
