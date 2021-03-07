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
    pulseOutputStub = PulseOutputNone()
    sut = UrgeEventPulseSender(pulseOutputStub)

    def test_onEventSendsTransformedValue(self):
        self.sut.onEvent(0, 1.5, 0.01, [])
        self.assertEqual(1, self.pulseOutputStub.__data__);

        self.sut.onEvent(0.5, 1.5, 0.01, [])
        self.assertEqual(128, self.pulseOutputStub.__data__);

        self.sut.onEvent(1, 1.5, 0.01, [])
        self.assertEqual(255, self.pulseOutputStub.__data__);

class UrgeEventPulseTransformatorTest(unittest.TestCase):
    def test_constructorValidParameters_passes(self):
        UrgeEventPulseTransformator(1, 255);

    def test_constructorInvalidParameters_raises(self):
        with self.assertRaises(AssertionError): UrgeEventPulseTransformator(0.5, 100)
        with self.assertRaises(AssertionError): UrgeEventPulseTransformator('low', 100)
        with self.assertRaises(AssertionError): UrgeEventPulseTransformator(1, 100.5)
        with self.assertRaises(AssertionError): UrgeEventPulseTransformator(1, 'high')

        with self.assertRaises(AssertionError): UrgeEventPulseTransformator(0, 100)
        with self.assertRaises(AssertionError): UrgeEventPulseTransformator(1, 256)

        with self.assertRaises(AssertionError): UrgeEventPulseTransformator(256, 1)

    def test_transformMinimumUrgeValue_returnsLow(self):
        sut = UrgeEventPulseTransformator(100, 199);
        self.assertEqual(100 ,sut.transform(0));

    def test_transformMaximumUrgeValue_returnsHigh(self):
        sut = UrgeEventPulseTransformator(100, 199);
        self.assertEqual(199 ,sut.transform(1));

    def test_transformMediumUrgeValue_returnsMiddle(self):
        sut = UrgeEventPulseTransformator(100, 199);
        self.assertEqual(149 ,sut.transform(0.5));

if __name__ == '__main__':
    unittest.main()
