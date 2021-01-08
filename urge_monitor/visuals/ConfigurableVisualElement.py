from abc import ABC, abstractmethod

class ConfigurableVisualElement(ABC):
    '''provides default values for configuration values and validation of values'''

    __configuration: {}

    def __init__(self, configuration):
        assert isinstance(configuration, dict)
        self.__configuration = configuration
        self.validateConfiguration()

    def getConfigurationValue(self, item):
        '''extracts the configuration item value from given configuration and uses default values if not present'''
        return self.__configuration.get(item, self.getConfigurationItemDefault(item))

    def hasConfigurationItemDefault(self, item):
        '''test if a defautl value is provided for this element'''
        return self.getConfigurationItemDefault(item) is not None

    @abstractmethod
    def getConfigurationItemDefault(self, item):
        '''access default configuration value'''
        pass

    @abstractmethod
    def validateConfiguration(self):
        '''validate the configurtion values in focus
        Note: call getConfigurationValue to access configuration values. Automatically validates possible default values.
        '''
        pass
