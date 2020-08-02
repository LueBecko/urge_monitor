import unittest
from . import UrgeIndicator

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

    def setScale(self, scale):
        pass

class UrgeIndicatorTest(unittest.TestCase):
    def setUp(self):
        self.window = WindowStub()
        self.config = {}

    def test_validateVisualConfig_withValidConfig_passes(self):
        UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['pos'] = [1.0, 1.0]
        UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['bg_height'] = 12
        UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['bg_width'] = 3
        UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['bg_col'] = (255, 255, 127)
        UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['bg_frame_col'] = (127, 255, 127)
        UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['bg_frame_width'] = 3
        UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['fg_height'] = 2
        UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['fg_width'] = 3
        UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['fg_col'] = (255, 127, 127)
        UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['fg_frame_col'] = (127, 127, 127)
        UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['fg_frame_width'] = 3
        UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['fg_opacity'] = 0.5
        UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['fg_opacity'] = 1
        UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['fg_opacity'] = 0
        UrgeIndicator.UrgeIndicator(self.window, self.config)

    def test_validateResolution_withInvalidPosition_raisesError(self):
        self.config['pos'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicator.UrgeIndicator(self.window, self.config)

    def test_validateResolution_withInvalidBGHeight_raisesError(self):
        self.config['bg_height'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicator.UrgeIndicator(self.window, self.config)

    def test_validateResolution_withInvalidBGWidth_raisesError(self):
        self.config['bg_width'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicator.UrgeIndicator(self.window, self.config)

    def test_validateResolution_withInvalidBGCol_raisesError(self):
        self.config['bg_col'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicator.UrgeIndicator(self.window, self.config)

    def test_validateResolution_withInvalidBGFrameCol_raisesError(self):
        self.config['bg_frame_col'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicator.UrgeIndicator(self.window, self.config)

    def test_validateResolution_withInvalidBGFrameWidth_raisesError(self):
        self.config['bg_frame_width'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['bg_frame_width'] = 0.5
        with self.assertRaises(AssertionError): UrgeIndicator.UrgeIndicator(self.window, self.config)

    def test_validateResolution_withInvalidFGHeight_raisesError(self):
        self.config['fg_height'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicator.UrgeIndicator(self.window, self.config)

    def test_validateResolution_withInvalidFGWidth_raisesError(self):
        self.config['fg_width'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicator.UrgeIndicator(self.window, self.config)

    def test_validateResolution_withInvalidFGCol_raisesError(self):
        self.config['fg_col'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicator.UrgeIndicator(self.window, self.config)

    def test_validateResolution_withInvalidFGFrameCol_raisesError(self):
        self.config['fg_frame_col'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicator.UrgeIndicator(self.window, self.config)

    def test_validateResolution_withInvalidFGFrameWidth_raisesError(self):
        self.config['fg_frame_width'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['fg_frame_width'] = 0.5
        with self.assertRaises(AssertionError): UrgeIndicator.UrgeIndicator(self.window, self.config)

    def test_validateResolution_withInvalidFGOpacity_raisesError(self):
        self.config['fg_opacity'] = 'invalid'
        with self.assertRaises(AssertionError): UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['fg_opacity'] = 1.5
        with self.assertRaises(AssertionError): UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.config['fg_opacity'] = -2.0
        with self.assertRaises(AssertionError): UrgeIndicator.UrgeIndicator(self.window, self.config)

    def test_hasConfigurationItemDefault_forDefinedDefaultValues_returnTrue(self):
        urgeIndicator = UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.assertFalse(urgeIndicator.hasConfigurationItemDefault('NOTHING'))
        self.assertTrue(urgeIndicator.hasConfigurationItemDefault('pos'))
        self.assertTrue(urgeIndicator.hasConfigurationItemDefault('bg_height'))
        self.assertTrue(urgeIndicator.hasConfigurationItemDefault('bg_width'))
        self.assertTrue(urgeIndicator.hasConfigurationItemDefault('bg_col'))
        self.assertTrue(urgeIndicator.hasConfigurationItemDefault('bg_frame_col'))
        self.assertTrue(urgeIndicator.hasConfigurationItemDefault('bg_frame_width'))
        self.assertTrue(urgeIndicator.hasConfigurationItemDefault('fg_height'))
        self.assertTrue(urgeIndicator.hasConfigurationItemDefault('fg_width'))
        self.assertTrue(urgeIndicator.hasConfigurationItemDefault('fg_col'))
        self.assertTrue(urgeIndicator.hasConfigurationItemDefault('fg_frame_col'))
        self.assertTrue(urgeIndicator.hasConfigurationItemDefault('fg_frame_width'))
        self.assertTrue(urgeIndicator.hasConfigurationItemDefault('fg_opacity'))

    def test_getConfigurationItemDefault_getsDefaultValues(self):
        urgeIndicator = UrgeIndicator.UrgeIndicator(self.window, self.config)
        self.assertEqual(urgeIndicator.getConfigurationItemDefault('NOTHING'), None)
        self.assertEqual(urgeIndicator.getConfigurationItemDefault('pos'), [0.0, 0.0])
        self.assertEqual(urgeIndicator.getConfigurationItemDefault('bg_height'), 7)
        self.assertEqual(urgeIndicator.getConfigurationItemDefault('bg_width'), 1)
        self.assertEqual(urgeIndicator.getConfigurationItemDefault('bg_col'), [127, 127, 127])
        self.assertEqual(urgeIndicator.getConfigurationItemDefault('bg_frame_col'), [127, 127, 127])
        self.assertEqual(urgeIndicator.getConfigurationItemDefault('bg_frame_width'), 2)
        self.assertEqual(urgeIndicator.getConfigurationItemDefault('fg_height'), 0.5)
        self.assertEqual(urgeIndicator.getConfigurationItemDefault('fg_width'), 1.25)
        self.assertEqual(urgeIndicator.getConfigurationItemDefault('fg_col'), [95, 95, 95])
        self.assertEqual(urgeIndicator.getConfigurationItemDefault('fg_frame_col'), [95, 95, 95])
        self.assertEqual(urgeIndicator.getConfigurationItemDefault('fg_frame_width'), 2)
        self.assertEqual(urgeIndicator.getConfigurationItemDefault('fg_opacity'), 1)

    def test_createVertices_alwaysCreates4VerticesDescribingARectWithCenter0(self):
        # this tests a private methode (sure about that?)
        urgeIndicator = UrgeIndicator.UrgeIndicator(self.window, self.config)
        result = urgeIndicator._UrgeIndicator__createVertices(4, 9)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)
        self.assertIn([2.0, 4.5], result)
        self.assertIn([-2.0, 4.5], result)
        self.assertIn([2.0, -4.5], result)
        self.assertIn([-2.0, -4.5], result)

    def test_updateUrge_withValidUrgeValue_ChangesPosAccordingToUrgeValue(self):
        urgeIndicator = UrgeIndicator.UrgeIndicator(self.window, self.config)
        # this tests private properties, which are only directly observable thru rendering
        urgeIndicator.updateUrge(0)
        self.assertTrue((urgeIndicator._UrgeIndicator__indicatorBar.pos == [0.0, -3.5]).all())
        urgeIndicator.updateUrge(1.0)
        self.assertTrue((urgeIndicator._UrgeIndicator__indicatorBar.pos == [0.0, 3.5]).all())
        urgeIndicator.updateUrge(0.5)
        self.assertTrue((urgeIndicator._UrgeIndicator__indicatorBar.pos == [0.0, 0.0]).all())

if __name__ == '__main__':
    unittest.main()
