import unittest
from urge_monitor.data.UrgeEventPulseSender import *
from urge_monitor.devices.PulseOutput import PulseOutputNone

class UrgeEventPulseSenderConstructorTest(unittest.TestCase):
    def test_constructorWithInvalidParameter_raisesError(self):
        with self.assertRaises(AssertionError): UrgeEventPulseSender(None)
        with self.assertRaises(AssertionError): UrgeEventPulseSender("Illegal")
        with self.assertRaises(AssertionError): UrgeEventPulseSender(7)

    def test_constructorWithOulseOutputParameter_createsObject(self):
        self.assertIsInstance(UrgeEventPulseSender(PulseOutputNone()), UrgeEventPulseSender)

class UrgeEventPulseSenderTransformationTest(unittest.TestCase):
    sut = UrgeEventPulseSender(PulseOutputNone())

    def test_ransformUrgeValueIntoPulseWithMinimumUrge_returns1(self):
        self.assertEqual(1 ,self.sut.transformUrgeValueIntoPulse(0));

    def test_ransformUrgeValueIntoPulseWithMaximumUrge_returns255(self):
        self.assertEqual(255 ,self.sut.transformUrgeValueIntoPulse(1));

    def test_ransformUrgeValueIntoPulseWithMedianUrge_returns128(self):
        self.assertEqual(128 ,self.sut.transformUrgeValueIntoPulse(0.5));


if __name__ == '__main__':
    unittest.main()
