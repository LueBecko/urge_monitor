import unittest
from urge_monitor.data.UrgeValueTransformator import UrgeValueTransformator

class UrgeValueTransformatorTest(unittest.TestCase):
    def test_constructorValidParameters_createsObject(self):
        self.assertIsInstance(UrgeValueTransformator(1, 255), UrgeValueTransformator);

    def test_constructorInvalidParameters_raises(self):
        with self.assertRaises(AssertionError): UrgeValueTransformator(0.5, 100)
        with self.assertRaises(AssertionError): UrgeValueTransformator('low', 100)
        with self.assertRaises(AssertionError): UrgeValueTransformator(1, 100.5)
        with self.assertRaises(AssertionError): UrgeValueTransformator(1, 'high')

        with self.assertRaises(AssertionError): UrgeValueTransformator(0, 100)
        with self.assertRaises(AssertionError): UrgeValueTransformator(1, 256)

        with self.assertRaises(AssertionError): UrgeValueTransformator(256, 1)

    def test_transformMinimumUrgeValue_returnsLow(self):
        sut = UrgeValueTransformator(100, 199);
        self.assertEqual(100 ,sut.transform(0));

    def test_transformMaximumUrgeValue_returnsHigh(self):
        sut = UrgeValueTransformator(100, 199);
        self.assertEqual(199 ,sut.transform(1));

    def test_transformMediumUrgeValue_returnsMiddle(self):
        sut = UrgeValueTransformator(100, 199);
        self.assertEqual(149 ,sut.transform(0.5));


if __name__ == '__main__':
    unittest.main()
