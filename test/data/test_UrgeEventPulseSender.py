import unittest
from urge_monitor.data.UrgeEventPulseSender import UrgeEventPulseSender
from urge_monitor.devices.PulseOutput import PulseOutputNone

class UrgeEventPulseSenderTest(unittest.TestCase):
    def test_constructorWithInvalidParameterPulseOutput_raisesError(self):
        with self.assertRaises(AssertionError): UrgeEventPulseSender(None)
        with self.assertRaises(AssertionError): UrgeEventPulseSender("Illegal")
        with self.assertRaises(AssertionError): UrgeEventPulseSender(7)

    def test_constructorWithPulseOutputParameter_createsObject(self):
        self.assertIsInstance(UrgeEventPulseSender(PulseOutputNone()), UrgeEventPulseSender)

    def test_onEventSendsTransformedUrgeValue(self):
        pulseOutputStub = PulseOutputNone()
        sut = UrgeEventPulseSender(pulseOutputStub)

        sut.onEvent(1, 1.5, 0.01, [])
        self.assertEqual(1, pulseOutputStub.__data__);

        sut.onEvent(128, 1.5, 0.01, [])
        self.assertEqual(128, pulseOutputStub.__data__);

        sut.onEvent(255, 1.5, 0.01, [])
        self.assertEqual(255, pulseOutputStub.__data__);

if __name__ == '__main__':
    unittest.main()
