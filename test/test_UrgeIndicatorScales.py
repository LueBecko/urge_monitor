import unittest
from urge_monitor.visuals.UrgeIndicatorScales import UrgeIndicatorScales

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

    def setScale(self, scale):
        pass

class UrgeIndicatorScalesTest(unittest.TestCase):
    def setUp(self):
        self.window = WindowStub()
        self.config = {}

    def test_hasConfigurationItemDefault_forDefinedDefaultValues_returnTrue(self):
        urgeIndicatorScales = UrgeIndicatorScales(self.window, self.config)
        self.assertFalse(urgeIndicatorScales.hasConfigurationItemDefault('NOTHING'))
        self.assertTrue(urgeIndicatorScales.hasConfigurationItemDefault('pos'))
        self.assertTrue(urgeIndicatorScales.hasConfigurationItemDefault('scales_col'))
        self.assertTrue(urgeIndicatorScales.hasConfigurationItemDefault('scales_thickness'))
        self.assertTrue(urgeIndicatorScales.hasConfigurationItemDefault('scales_widthl'))
        self.assertTrue(urgeIndicatorScales.hasConfigurationItemDefault('scales_widthr'))
        self.assertTrue(urgeIndicatorScales.hasConfigurationItemDefault('scales_text'))
        self.assertTrue(urgeIndicatorScales.hasConfigurationItemDefault('bg_width'))
        self.assertTrue(urgeIndicatorScales.hasConfigurationItemDefault('bg_height'))

    def test_getConfigurationItemDefault_getsDefaultValues(self):
        urgeIndicatorScales = UrgeIndicatorScales(self.window, self.config)
        self.assertEqual(urgeIndicatorScales.getConfigurationItemDefault('NOTHING'), None)
        self.assertEqual(urgeIndicatorScales.getConfigurationItemDefault('pos'), [0.0, 0.0])
        self.assertEqual(urgeIndicatorScales.getConfigurationItemDefault('scales_col'), [255, 255, 255])
        self.assertEqual(urgeIndicatorScales.getConfigurationItemDefault('scales_thickness'), 4)
        self.assertEqual(urgeIndicatorScales.getConfigurationItemDefault('scales_widthl'), 0.25)
        self.assertEqual(urgeIndicatorScales.getConfigurationItemDefault('scales_widthr'), 0.25)
        self.assertEqual(urgeIndicatorScales.getConfigurationItemDefault('scales_text'), [])
        self.assertEqual(urgeIndicatorScales.getConfigurationItemDefault('bg_width'), 1)
        self.assertEqual(urgeIndicatorScales.getConfigurationItemDefault('bg_height'), 7)

    def test_validateConfiguration_withValidConfig_passes(self):
        UrgeIndicatorScales(self.window, self.config)
        self.config['pos'] = [1.0, 1.0]
        UrgeIndicatorScales(self.window, self.config)
        self.config['scales_col'] = [127, 255, 0]
        UrgeIndicatorScales(self.window, self.config)
        self.config['scales_thickness'] = 2
        UrgeIndicatorScales(self.window, self.config)
        self.config['scales_widthl'] = 0.5
        UrgeIndicatorScales(self.window, self.config)
        self.config['scales_widthr'] = 0.25
        UrgeIndicatorScales(self.window, self.config)
        self.config['scales_text'] = ['low', '', 'high']
        UrgeIndicatorScales(self.window, self.config)
        self.config['bg_width'] = 2
        UrgeIndicatorScales(self.window, self.config)
        self.config['bg_height'] = 9
        UrgeIndicatorScales(self.window, self.config)

    def test_validateConfiguration_withInvalidPosition_raisesError(self):
        self.config['pos'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicatorScales(self.window, self.config)

    def test_validateConfiguration_withInvalidScalesColor_raisesError(self):
        self.config['scales_col'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicatorScales(self.window, self.config)

    def test_validateConfiguration_withInvalidScalesThickness_raisesError(self):
        self.config['scales_thickness'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicatorScales(self.window, self.config)
        self.config['scales_thickness'] = -1
        with self.assertRaises(AssertionError): UrgeIndicatorScales(self.window, self.config)
        self.config['scales_thickness'] = 0.0
        with self.assertRaises(AssertionError): UrgeIndicatorScales(self.window, self.config)

    def test_validateConfiguration_withInvalidScalesWidthLeft_raisesError(self):
        self.config['scales_widthl'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicatorScales(self.window, self.config)
        self.config['scales_widthl'] = -1
        with self.assertRaises(AssertionError): UrgeIndicatorScales(self.window, self.config)

    def test_validateConfiguration_withInvalidScalesWidthRight_raisesError(self):
        self.config['scales_widthr'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicatorScales(self.window, self.config)
        self.config['scales_widthr'] = -1
        with self.assertRaises(AssertionError): UrgeIndicatorScales(self.window, self.config)

    def test_validateConfiguration_withInvalidScalesText_raisesError(self):
        self.config['scales_text'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicatorScales(self.window, self.config)
        self.config['scales_text'] = [12, 3.14, 'something']
        with self.assertRaises(AssertionError): UrgeIndicatorScales(self.window, self.config)

    def test_validateConfiguration_withInvalidBackgroundBarWidth_raisesError(self):
        self.config['bg_width'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicatorScales(self.window, self.config)

    def test_validateConfiguration_withInvalidBackgroundBarHeight_raisesError(self):
        self.config['bg_height'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicatorScales(self.window, self.config)

if __name__ == '__main__':
    unittest.main()
