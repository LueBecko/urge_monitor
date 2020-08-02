import unittest
from .UrgeIndicatorScalesText import UrgeIndicatorScalesText

# TODO: migrate stubs to test helpers class
class MonitorStub:
    def getWidth(self):
        return 1024

    def getSizePix(self):
        return [1024, 512]

    def getDistance(self):
        return 60

class WindowStub:
    def __init__(self):
        self.colorSpace = 'rgb255'
        self._toDraw = []
        self._toDrawDepths = []
        self._setCurrent = lambda : None
        self._haveShaders = False
        self.monitor = MonitorStub()
        self.useFBO = False
        self.units = 'deg'
        self.blendMode = 'avg'
        self.winType = 'pyglet'

    def setScale(self, scale):
        pass

class UrgeIndicatorScalesTextTest(unittest.TestCase):
    def setUp(self):
        self.window = WindowStub()
        self.config = {}

    def test_hasConfigurationItemDefault_forDefinedDefaultValues_returnTrue(self):
        urgeIndicatorScalesText = UrgeIndicatorScalesText(self.window, self.config)
        self.assertFalse(urgeIndicatorScalesText.hasConfigurationItemDefault('NOTHING'))
        self.assertTrue(urgeIndicatorScalesText.hasConfigurationItemDefault('pos'))
        self.assertTrue(urgeIndicatorScalesText.hasConfigurationItemDefault('bg_width'))
        self.assertTrue(urgeIndicatorScalesText.hasConfigurationItemDefault('bg_height'))
        self.assertTrue(urgeIndicatorScalesText.hasConfigurationItemDefault('scales_text_col'))
        self.assertTrue(urgeIndicatorScalesText.hasConfigurationItemDefault('scales_text'))
        self.assertTrue(urgeIndicatorScalesText.hasConfigurationItemDefault('scales_text_pos'))
        self.assertTrue(urgeIndicatorScalesText.hasConfigurationItemDefault('scales_text_size'))
        self.assertTrue(urgeIndicatorScalesText.hasConfigurationItemDefault('scales_widthl'))
        self.assertTrue(urgeIndicatorScalesText.hasConfigurationItemDefault('scales_widthr'))

    def test_getConfigurationItemDefault_getsDefaultValues(self):
        urgeIndicatorScalesText = UrgeIndicatorScalesText(self.window, self.config)
        self.assertEqual(urgeIndicatorScalesText.getConfigurationItemDefault('NOTHING'), None)
        self.assertEqual(urgeIndicatorScalesText.getConfigurationItemDefault('pos'), [0.0, 0.0])
        self.assertEqual(urgeIndicatorScalesText.getConfigurationItemDefault('bg_width'), 1)
        self.assertEqual(urgeIndicatorScalesText.getConfigurationItemDefault('bg_height'), 7)
        self.assertEqual(urgeIndicatorScalesText.getConfigurationItemDefault('scales_text_col'), [255, 255, 255])
        self.assertEqual(urgeIndicatorScalesText.getConfigurationItemDefault('scales_text'), [])
        self.assertEqual(urgeIndicatorScalesText.getConfigurationItemDefault('scales_text_pos'), [])
        self.assertEqual(urgeIndicatorScalesText.getConfigurationItemDefault('scales_text_size'), [])
        self.assertEqual(urgeIndicatorScalesText.getConfigurationItemDefault('scales_widthl'), 0.25)
        self.assertEqual(urgeIndicatorScalesText.getConfigurationItemDefault('scales_widthr'), 0.25)

    def test_validateConfiguration_withValidConfig_passes(self):
        UrgeIndicatorScalesText(self.window, self.config)
        self.config['pos'] = [1.0, 1.0]
        UrgeIndicatorScalesText(self.window, self.config)
        self.config['scales_text_col'] = [127, 255, 0]
        UrgeIndicatorScalesText(self.window, self.config)
        self.config['scales_widthl'] = 0.5
        UrgeIndicatorScalesText(self.window, self.config)
        self.config['scales_widthr'] = 0.25
        UrgeIndicatorScalesText(self.window, self.config)
        self.config['scales_text'] = ['low', '', 'high']
        self.config['scales_text_pos'] = ['a', 'b', 'c']
        self.config['scales_text_size'] = [10, 15, 20]
        UrgeIndicatorScalesText(self.window, self.config)
        self.config['bg_width'] = 2
        UrgeIndicatorScalesText(self.window, self.config)
        self.config['bg_height'] = 9
        UrgeIndicatorScalesText(self.window, self.config)

    def test_validateConfiguration_withInvalidPosition_raisesError(self):
        self.config['pos'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicatorScalesText(self.window, self.config)

    def test_validateConfiguration_withInvalidBGHeight_raisesError(self):
        self.config['bg_height'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicatorScalesText(self.window, self.config)

    def test_validateConfiguration_withInvalidBGWidth_raisesError(self):
        self.config['bg_width'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicatorScalesText(self.window, self.config)

    def test_validateConfiguration_withInvalidScalesTextColor_raisesError(self):
        self.config['scales_text_col'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicatorScalesText(self.window, self.config)

    def test_validateConfiguration_withInvalidScalesWidthLeft_raisesError(self):
        self.config['scales_widthl'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicatorScalesText(self.window, self.config)
        self.config['scales_widthl'] = -1
        with self.assertRaises(AssertionError): UrgeIndicatorScalesText(self.window, self.config)
        self.config['scales_widthl'] = 0.0
        with self.assertRaises(AssertionError): UrgeIndicatorScalesText(self.window, self.config)

    def test_validateConfiguration_withInvalidScalesWidthRight_raisesError(self):
        self.config['scales_widthr'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicatorScalesText(self.window, self.config)
        self.config['scales_widthr'] = -1
        with self.assertRaises(AssertionError): UrgeIndicatorScalesText(self.window, self.config)
        self.config['scales_widthr'] = 0.0
        with self.assertRaises(AssertionError): UrgeIndicatorScalesText(self.window, self.config)

    def test_validateConfiguration_withInvalidScalesText_raisesError(self):
        self.config['scales_text'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicatorScalesText(self.window, self.config)
        self.config['scales_text'] = [12, 3.14, 'something']
        with self.assertRaises(AssertionError): UrgeIndicatorScalesText(self.window, self.config)

if __name__ == '__main__':
    unittest.main()
