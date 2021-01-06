import unittest
import PulseOutput

class PulseOutputFactoryMethodTest(unittest.TestCase):
    def test_NoOutPulse_createsPulseOutputNone(self):
        pulseConfig = {'pulse': {'send_out_pulse': False, 'simulation': True}}
        outputObject = PulseOutput.createPulseOutput(pulseConfig)
        self.assertIsInstance(outputObject, (PulseOutput.PulseOutput, PulseOutput.PulseOutputNone))

        pulseConfig = {'pulse': {'send_out_pulse': False, 'simulation': False}}
        outputObject = PulseOutput.createPulseOutput(pulseConfig)
        self.assertIsInstance(outputObject, (PulseOutput.PulseOutput, PulseOutput.PulseOutputNone))

    def test_OutPulseSimulation_createsPulseOutputSimulation(self):
        pulseConfig = {'pulse': {'send_out_pulse': True, 'simulation': True},
            'out_pulse': {'address': 0xCFF8, 'data': 127,'duration': 0.001}}
        outputObject = PulseOutput.createPulseOutput(pulseConfig)
        self.assertIsInstance(outputObject, (PulseOutput.PulseOutput, PulseOutput.PulseOutputSimulation))
        self.assertEqual(outputObject.getDataValue(), 127)

    def test_OutPulseSimulation_withInvalidDataConfiguration_fails(self):
        pulseConfig = {'pulse': {'send_out_pulse': True, 'simulation': True},
            'out_pulse': {'address': 0xCFF8, 'data': -999,'duration': 0.001}}
        with self.assertRaises(AssertionError): outputObject = PulseOutput.createPulseOutput(pulseConfig)

    def test_OutPulse_createsPulseOutputParallel(self):
        pulseConfig = {'pulse': {'send_out_pulse': True, 'simulation': False},
            'out_pulse': {'address': 0xCFF8, 'data': 127,'duration': 0.001}}
        outputObject = PulseOutput.createPulseOutput(pulseConfig)
        self.assertIsInstance(outputObject, (PulseOutput.PulseOutput, PulseOutput.PulseOutputParallel))
        self.assertEqual(outputObject.getDataValue(), 127)

    def test_OutPulse_withInvalidDataConfiguration_fails(self):
        pulseConfig = {'pulse': {'send_out_pulse': True, 'simulation': False},
            'out_pulse': {'address': 0xCFF8, 'data': -999,'duration': 0.001}}
        with self.assertRaises(AssertionError): outputObject = PulseOutput.createPulseOutput(pulseConfig)

    def test_OutPulse_withInvalidDurationConfiguration_fails(self):
        pulseConfig = {'pulse': {'send_out_pulse': True, 'simulation': False},
            'out_pulse': {'address': 0xCFF8, 'data': 127,'duration': -0.001}}
        with self.assertRaises(AssertionError): outputObject = PulseOutput.createPulseOutput(pulseConfig)

    def test_OutPulse_withInvalidAddressConfiguration_fails(self):
        pulseConfig = {'pulse': {'send_out_pulse': True, 'simulation': False},
            'out_pulse': {'address': "0xCFF8", 'data': 127,'duration': 0.001}}
        with self.assertRaises(AssertionError): outputObject = PulseOutput.createPulseOutput(pulseConfig)

if __name__ == '__main__':
    unittest.main()
