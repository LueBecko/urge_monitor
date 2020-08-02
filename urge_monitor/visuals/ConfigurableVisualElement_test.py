import unittest
from .ConfigurableVisualElement import ConfigurableVisualElement

class ConfigurableVisualElementStub(ConfigurableVisualElement):

    def getConfigurationItemDefault(self, item):
        if item == 'TEST_ITEM':
            return 'TEST_VALUE'

    def validateConfiguration(self):
        '''Note: validation also validates default values due to calling getConfigurationValue'''
        assert isinstance(self.getConfigurationValue('TEST_ITEM'), str)


class UrgeIndicatorTest(unittest.TestCase):
    def test_getConfigurationItem_withDefaultValue_returnsDefaultValue(self):
        config = {}
        config['something'] = 3
        configVisualElementStub = ConfigurableVisualElementStub(config)
        
        self.assertEqual(configVisualElementStub.getConfigurationValue('something'), 3)
        self.assertEqual(configVisualElementStub.getConfigurationValue('something_else'), None)
        self.assertEqual(configVisualElementStub.getConfigurationValue('TEST_ITEM'), 'TEST_VALUE')

    def test_getConfigurationItem_withOverwrittenDeafaultValue_returnOverwrittenValue(self):
        config = {}
        config['TEST_ITEM'] = 'DIFFERENT_VALUE'
        configVisualElementStub = ConfigurableVisualElementStub(config)
        
        self.assertEqual(configVisualElementStub.getConfigurationValue('TEST_ITEM'), 'DIFFERENT_VALUE')

    def test_hasConfigurationItemDefault_WithDefaultValue_true(self):
        configVisualElementStub = ConfigurableVisualElementStub({})
        self.assertTrue(configVisualElementStub.hasConfigurationItemDefault('TEST_ITEM'))

    def test_hasConfigurationItemDefault_WithoutDefaultValue_true(self):
        configVisualElementStub = ConfigurableVisualElementStub({})
        self.assertFalse(configVisualElementStub.hasConfigurationItemDefault('OTHER_ITEM'))

if __name__ == '__main__':
    unittest.main()
