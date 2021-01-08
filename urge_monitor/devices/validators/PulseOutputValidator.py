from . import PulseOutputDataValidator, PulseOutputDurationValidator, PulseOutputAddressValidator

class PulseOutputParallelValidator:
    '''validates out-pulse for parallel configuration'''

    def validate(self, value):
        assert value != None
        assert isinstance(value, dict)

        PulseOutputAddressValidator.PulseOutputAddressValidator().validate(value.get('address'))
        PulseOutputDataValidator.PulseOutputDataValidator().validate(value.get('data'))
        PulseOutputDurationValidator.PulseOutputDurationValidator().validate(value.get('duration'))

class PulseOutputSimulationValidator:
    '''validates out-pulse for simulation configuration'''

    def validate(self, value):
        assert value != None
        assert isinstance(value, dict)

        PulseOutputDataValidator.PulseOutputDataValidator().validate(value.get('data'))

