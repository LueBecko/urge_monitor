import unittest
from urge_monitor.devices.validators.PulseOutputValidator import PulseOutputSimulationValidator, PulseOutputParallelValidator

class PulseOutputSimulationValidatorTest(unittest.TestCase):
    def setUp(self):
        self.validator = PulseOutputSimulationValidator()

    def test_validate_withInvalidType_raises(self):
        with self.assertRaises(AssertionError): self.validator.validate(None)
        with self.assertRaises(AssertionError): self.validator.validate([])
        with self.assertRaises(AssertionError): self.validator.validate("something")
        with self.assertRaises(AssertionError): self.validator.validate(1)
        with self.assertRaises(AssertionError): self.validator.validate(2.5)

    def test_validate_withInvalidValue_raises(self):
        with self.assertRaises(AssertionError): self.validator.validate({'data': 999})

    def test_validate_withoutData_raises(self):
        with self.assertRaises(AssertionError): self.validator.validate({'something': 999})

    def test_validate_withValidValue_passes(self):
        self.validator.validate({'data': 127})

class PulseOutputParallelValidatorTest(unittest.TestCase):
    def setUp(self):
        self.validator = PulseOutputParallelValidator()

    def test_validate_withInvalidType_raises(self):
        with self.assertRaises(AssertionError): self.validator.validate(None)
        with self.assertRaises(AssertionError): self.validator.validate([])
        with self.assertRaises(AssertionError): self.validator.validate("something")
        with self.assertRaises(AssertionError): self.validator.validate(1)
        with self.assertRaises(AssertionError): self.validator.validate(2.5)

    def test_validate_withInvalidValue_raises(self):
        with self.assertRaises(AssertionError): self.validator.validate({'address': "0xDFF", 'data': 127, 'duration': 0.1})
        with self.assertRaises(AssertionError): self.validator.validate({'address': 0xDFF, 'data': 999, 'duration': 0.1})
        with self.assertRaises(AssertionError): self.validator.validate({'address': 0xDFF, 'data': 127, 'duration': -12})

    def test_validate_withoutData_raises(self):
        with self.assertRaises(AssertionError): self.validator.validate({'data': 127, 'duration': 0.1})
        with self.assertRaises(AssertionError): self.validator.validate({'address': 0xDFF, 'duration': 0.1})
        with self.assertRaises(AssertionError): self.validator.validate({'address': 0xDFF, 'data': 127})

    def test_validate_withValidValue_passes(self):
        self.validator.validate({'address': 0xDFF, 'data': 127, 'duration': 0.1})


if __name__ == '__main__':
    unittest.main()

