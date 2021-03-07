import unittest
from urge_monitor.visuals import helpers

class ColorValidatorTest(unittest.TestCase):

    def test_validateColor_withInvalidColorSpace_raises(self):
        validator = helpers.ColorValidator()
        with self.assertRaises(AssertionError): validator.validateColor(None, (0,0,0))
        with self.assertRaises(AssertionError): validator.validateColor(7, (0,0,0))
        with self.assertRaises(AssertionError): validator.validateColor('None', (0,0,0))


    def test_validateColor_withValidRGB_passes(self):
        validator = helpers.ColorValidator()
        validator.validateColor('rgb', (0,0,0))
        validator.validateColor('rgb', (-1,0,1))
        validator.validateColor('rgb', (-1.0,-0.5,0.999))


    def test_validateColor_withInvalidRGB_raises(self):
        validator = helpers.ColorValidator()
        with self.assertRaises(AssertionError): validator.validateColor('rgb', None)
        with self.assertRaises(AssertionError): validator.validateColor('rgb', (-100,0,1))
        with self.assertRaises(AssertionError): validator.validateColor('rgb', (0.0,1.0))
        with self.assertRaises(AssertionError): validator.validateColor('rgb', (-1.0,-0.5,'0.999'))

    def test_validateColor_withValidRGB255_passes(self):
        validator = helpers.ColorValidator()
        validator.validateColor('rgb255', (0,0,0))
        validator.validateColor('rgb255', (0,127,255))
        validator.validateColor('rgb255', (255,255,255))

    def test_validateColor_withInvalidRGB255_raises(self):
        validator = helpers.ColorValidator()
        with self.assertRaises(AssertionError): validator.validateColor('rgb255', None)
        with self.assertRaises(AssertionError): validator.validateColor('rgb255', (-100,0,1))
        with self.assertRaises(AssertionError): validator.validateColor('rgb255', (16,32))
        with self.assertRaises(AssertionError): validator.validateColor('rgb255', (16,32,'64'))

    def test_validateColor_withValidHSV_passes(self):
        validator = helpers.ColorValidator()
        validator.validateColor('hsv', (0,0,0))
        validator.validateColor('hsv', (360,1,1))
        validator.validateColor('hsv', (180,0.5,0.333))

    def test_validateColor_withInvalidHSV_raises(self):
        validator = helpers.ColorValidator()
        with self.assertRaises(AssertionError): validator.validateColor('hsv', None)
        with self.assertRaises(AssertionError): validator.validateColor('hsv', (-1,0,0))
        with self.assertRaises(AssertionError): validator.validateColor('hsv', (0,-1,0))
        with self.assertRaises(AssertionError): validator.validateColor('hsv', (0,0,-1))
        with self.assertRaises(AssertionError): validator.validateColor('hsv', (90,1))
        with self.assertRaises(AssertionError): validator.validateColor('hsv', (90,1,'0.5'))


if __name__ == '__main__':
    unittest.main()
