import unittest
from urge_monitor.visuals import helpers

class ColorspaceTransformatorTest(unittest.TestCase):

    def test_rgb255_to_rgb_validValue(self):
        transformator = helpers.ColorspaceTransformator()
        self.assertEqual(transformator.colorspace_to_colorspace('rgb255', 'rgb', (0,0,0)), (-1.0,-1.0,-1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb255', 'rgb', (255,0,0)), (1.0,-1.0,-1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb255', 'rgb', (255,255,255)), (1.0,1.0,1.0))

    def test_rgb255_to_rgb_invalidValue(self):
        transformator = helpers.ColorspaceTransformator()
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb255', 'rgb', None)
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb255', 'rgb', 'wrong')
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb255', 'rgb', (0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb255', 'rgb', (-1,0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb255', 'rgb', (5000,0,0))

    def test_rgb255_to_rgb255_validValue(self):
        transformator = helpers.ColorspaceTransformator()
        self.assertEqual(transformator.colorspace_to_colorspace('rgb255', 'rgb255', (0,0,0)), (0,0,0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb255', 'rgb255', (255,127,0)), (255,127,0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb255', 'rgb255', (255,255,255)), (255,255,255))

    def test_rgb255_to_rgb255_invalidValue(self):
        transformator = helpers.ColorspaceTransformator()
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb255', 'rgb255', None)
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb255', 'rgb255', 'wrong')
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb255', 'rgb255', (0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb255', 'rgb255', (-1,0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb255', 'rgb255', (5000,0,0))

    def test_rgb255_to_hsv_validValue(self):
        transformator = helpers.ColorspaceTransformator()
        self.assertEqual(transformator.colorspace_to_colorspace('rgb255', 'hsv', (0,0,0)), (0,0,0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb255', 'hsv', (255,0,0)), (0,1.0,1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb255', 'hsv', (127,0,0)), (0,1.0,0.4980392156862745))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb255', 'hsv', (0,255,0)), (120,1.0,1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb255', 'hsv', (0,127,0)), (120,1.0,0.4980392156862745))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb255', 'hsv', (0,0,255)), (240,1.0,1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb255', 'hsv', (0,0,127)), (240,1.0,0.4980392156862745))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb255', 'hsv', (255,127,0)), (29.88235294117647,1.0,1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb255', 'hsv', (255,127,127)), (0,0.5019607843137255,1.0))

    def test_rgb255_to_hsv_invalidValue(self):
        transformator = helpers.ColorspaceTransformator()
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb255', 'hsv', None)
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb255', 'hsv', 'wrong')
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb255', 'hsv', (0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb255', 'hsv', (-1,0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb255', 'hsv', (5000,0,0))

    def test_rgb_to_rgb255_validValue(self):
        transformator = helpers.ColorspaceTransformator()
        self.assertEqual(transformator.colorspace_to_colorspace('rgb', 'rgb255', (0.0,0.0,0.0)), (127,127,127))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb', 'rgb255', (1.0,0.5,-1.0)), (255,191,0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb', 'rgb255', (1.0,1.0,1.0)), (255,255,255))

    def test_rgb_to_rgb255_invalidValue(self):
        transformator = helpers.ColorspaceTransformator()
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb', 'rgb255', None)
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb', 'rgb255', 'wrong')
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb', 'rgb255', (0.0,0.0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb', 'rgb255', (-10.0,0.0,0.0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb', 'rgb255', (7.0,0.0,0.0))

    def test_rgb_to_rgb_validValue(self):
        transformator = helpers.ColorspaceTransformator()
        self.assertEqual(transformator.colorspace_to_colorspace('rgb', 'rgb', (0.0,0.0,0.0)), (0.0,0.0,0.0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb', 'rgb', (1.0,0.5,-1.0)), (1.0,0.5,-1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb', 'rgb', (1.0,1.0,1.0)), (1.0,1.0,1.0))

    def test_rgb_to_rgb_invalidValue(self):
        transformator = helpers.ColorspaceTransformator()
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb', 'rgb', None)
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb', 'rgb', 'wrong')
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb', 'rgb', (0.0,0.0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb', 'rgb', (-10.0,0.0,0.0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb', 'rgb', (7.0,0.0,0.0))

    def test_rgb_to_hsv_validValue(self):
        transformator = helpers.ColorspaceTransformator()
        self.assertEqual(transformator.colorspace_to_colorspace('rgb', 'hsv', (-1.0,-1.0,-1.0)), (0,0,0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb', 'hsv', (1.0,-1.0,-1.0)), (0,1.0,1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb', 'hsv', (0.0,-1.0,-1.0)), (0,1.0,0.5))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb', 'hsv', (-1.0,1.0,-1.0)), (120,1.0,1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb', 'hsv', (-1.0,0.0,-1.0)), (120,1.0,0.5))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb', 'hsv', (-1.0,-1.0,1.0)), (240,1.0,1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb', 'hsv', (-1.0,-1.0,0.0)), (240,1.0,0.5))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb', 'hsv', (1.0,0.0,-1.0)), (30,1.0,1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('rgb', 'hsv', (1.0,0.0,0.0)), (0,0.5,1.0))

    def test_rgb_to_hsv_invalidValue(self):
        transformator = helpers.ColorspaceTransformator()
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb', 'hsv', None)
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb', 'hsv', 'wrong')
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb', 'hsv', (0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb', 'hsv', (-2.0,0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('rgb', 'hsv', (5000,0,0))

    def test_hsv_to_rgb_validValue(self):
        transformator = helpers.ColorspaceTransformator()
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb', (0,0,0)), (-1.0,-1.0,-1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb', (0,1.0,1.0)), ( 1.0,-1.0,-1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb', (0,1.0,0.5)), ( 0.0,-1.0,-1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb', (120,1.0,1.0)), (-1.0, 1.0,-1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb', (120,1.0,0.5)), (-1.0, 0.0,-1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb', (240,1.0,1.0)), (-1.0,-1.0, 1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb', (240,1.0,0.5)), (-1.0,-1.0, 0.0))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb', (30,1.0,1.0)), ( 1.0, 0.0,-1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb', (0,0.5,1.0)), ( 1.0, 0.0, 0.0))

    def test_hsv_to_rgb_invalidValue(self):
        transformator = helpers.ColorspaceTransformator()
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb', None)
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb', 'wrong')
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb', (0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb', (-2,0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb', (5000,0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb', (0,7,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb', (0,-2,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb', (0,0,7))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb', (0,0,-2))

    def test_hsv_to_rgb255_validValue(self):
        transformator = helpers.ColorspaceTransformator()
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb255', (0,0,0)), (0,0,0))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb255', (0,1.0,1.0)), (255,0,0))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb255', (0,1.0,0.5)), (127,0,0))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb255', (120,1.0,1.0)), (0,255,0))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb255', (120,1.0,0.5)), (0,127,0))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb255', (240,1.0,1.0)), (0,0,255))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb255', (240,1.0,0.5)), (0,0, 127))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb255', (30,1.0,1.0)), (255,127,0))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'rgb255', (0,0.5,1.0)), (255,127,127))

    def test_hsv_to_rgb255_invalidValue(self):
        transformator = helpers.ColorspaceTransformator()
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb255', None)
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb255', 'wrong')
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb255', (0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb255', (-2,0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb255', (5000,0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb255', (0,7,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb255', (0,-2,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb255', (0,0,7))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'rgb255', (0,0,-2))

    def test_hsv_to_hsv_validValue(self):
        transformator = helpers.ColorspaceTransformator()
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'hsv', (0.0,0.0,0.0)), (0.0,0.0,0.0))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'hsv', (180,0.5,1.0)), (180,0.5,1.0))
        self.assertEqual(transformator.colorspace_to_colorspace('hsv', 'hsv', (360,1.0,1.0)), (360,1.0,1.0))

    def test_hsv_to_hsv_invalidValue(self):
        transformator = helpers.ColorspaceTransformator()
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'hsv', None)
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'hsv', 'wrong')
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'hsv', (0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'hsv', (-2,0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'hsv', (5000,0,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'hsv', (0,7,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'hsv', (0,-2,0))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'hsv', (0,0,7))
        with self.assertRaises(AssertionError): transformator.colorspace_to_colorspace('hsv', 'hsv', (0,0,-2))

if __name__ == '__main__':
    unittest.main()
