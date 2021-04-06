import unittest
from urge_monitor.devices.PulseListener import *

class PulseListenerFactoryMethodTest(unittest.TestCase):
    def __buildConfiguration(self, interface, simulation):
        if isinstance(interface, str):
            return {'pulse': {'interface': interface, 'simulation': simulation}, interface.lower(): {}}
        else:
            return {'pulse': {'interface': interface, 'simulation': simulation}}

    def test_MissingInterface_createsPulseListenerNone(self):
        pulseConfig = self.__buildConfiguration(None, False)
        outputObject = createPulseListener(pulseConfig, None)
        self.assertIsInstance(outputObject, (PulseListener, NonePulseListener))

    def test_InterfaceNone_createsPulseListenerNone(self):
        pulseConfig = self.__buildConfiguration('None', False)
        outputObject = createPulseListener(pulseConfig, None)
        self.assertIsInstance(outputObject, (PulseListener, NonePulseListener))

    def test_InterfaceParallel_createsPulseListenerParallel(self):
        pulseConfig = self.__buildConfiguration('Parallel', False)
        outputObject = createPulseListener(pulseConfig, None)
        self.assertIsInstance(outputObject, (PulseListener, ParallelPulseListener))

    def test_InterfaceSerial_createsPulseListenerSerial(self):
        pulseConfig = self.__buildConfiguration('Serial', False)
        outputObject = createPulseListener(pulseConfig, None)
        self.assertIsInstance(outputObject, (PulseListener, SerialPulseListener))

    def test_InterfaceKeyboard_createsPulseListenerKeyboard(self):
        pulseConfig = self.__buildConfiguration('Keyboard', False)
        outputObject = createPulseListener(pulseConfig, None)
        self.assertIsInstance(outputObject, (PulseListener, KeyboardPulseListener))

    def test_ActiveSimulation_createsSimulatedPulseListener(self):
        pulseConfig = self.__buildConfiguration('Keyboard', True)
        outputObject = createPulseListener(pulseConfig, None)
        self.assertIsInstance(outputObject, (PulseListener, SimulatedPulseListener))

    def test_InterfaceWithoutRequiredConfiguration_raisesConfigError(self):
        pulseConfig = {'pulse': {'interface': 'parallel', 'simulation': False}}
        with self.assertRaises(AssertionError): createPulseListener(pulseConfig, None)


if __name__ == '__main__':
    unittest.main()
