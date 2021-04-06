import unittest
from urge_monitor.devices.PulseOutput import PulseOutput, createPulseOutput, PulseOutputNone, PulseOutputParallel

class PulseOutputFactoryMethodTest(unittest.TestCase):
    def test_NoOutPulse_createsPulseOutputNone(self):
        pulseConfig = {'pulse': {'send_out_pulse': False, 'simulation': True}}
        outputObject = createPulseOutput(pulseConfig)
        self.assertIsInstance(outputObject, (PulseOutput, PulseOutputNone))
        self.assertEqual(outputObject.getDataValue(), 0)

        pulseConfig = {'pulse': {'send_out_pulse': False, 'simulation': False}}
        outputObject = createPulseOutput(pulseConfig)
        self.assertIsInstance(outputObject, (PulseOutput, PulseOutputNone))
        self.assertEqual(outputObject.getDataValue(), 0)

    def test_OutPulseSimulation_createsPulseOutputNone(self):
        pulseConfig = {'pulse': {'send_out_pulse': True, 'simulation': True},
            'out_pulse': {'data': 127}}
        outputObject = createPulseOutput(pulseConfig)
        self.assertIsInstance(outputObject, (PulseOutput, PulseOutputNone))

    def test_OutPulse_createsPulseOutputParallel(self):
        pulseConfig = {'pulse': {'send_out_pulse': True, 'simulation': False},
            'out_pulse': {'address': 0xCFF8, 'data': 127,'duration': 0.001}}
        outputObject = createPulseOutput(pulseConfig)
        self.assertIsInstance(outputObject, (PulseOutput, PulseOutputParallel))


class PulseOutputParallelTest(unittest.TestCase):

    def test_OutPulseInit_initialDataValue(self):
        pulseConfig = {'pulse': {'send_out_pulse': True, 'simulation': False},
            'out_pulse': {'address': 0xCFF8, 'data': 127,'duration': 0.001}}
        outputObject = createPulseOutput(pulseConfig)
        self.assertEqual(outputObject.getDataValue(), 127)

    def test_OutPulseInit_withoutOutPulseConfiguration_fails(self):
        pulseConfig = {'pulse': {'send_out_pulse': True, 'simulation': False}}
        with self.assertRaises(AssertionError): outputObject = createPulseOutput(pulseConfig)

    def test_OutPulseInit_withInvalidDataConfiguration_fails(self):
        pulseConfig = {'pulse': {'send_out_pulse': True, 'simulation': False},
            'out_pulse': {'address': 0xCFF8, 'data': -999,'duration': 0.001}}
        with self.assertRaises(AssertionError): outputObject = createPulseOutput(pulseConfig)

    def test_OutPulseInit_withInvalidDurationConfiguration_fails(self):
        pulseConfig = {'pulse': {'send_out_pulse': True, 'simulation': False},
            'out_pulse': {'address': 0xCFF8, 'data': 127,'duration': -0.001}}
        with self.assertRaises(AssertionError): outputObject = createPulseOutput(pulseConfig)

    def test_OutPulseInit_withInvalidAddressConfiguration_fails(self):
        pulseConfig = {'pulse': {'send_out_pulse': True, 'simulation': False},
            'out_pulse': {'address': "0xCFF8", 'data': 127,'duration': 0.001}}
        with self.assertRaises(AssertionError): outputObject = createPulseOutput(pulseConfig)


if __name__ == '__main__':
    unittest.main()
