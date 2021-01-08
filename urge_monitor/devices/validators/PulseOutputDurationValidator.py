
class PulseOutputDurationValidator:
    '''validates duration value of out-pulse configuration'''

    def validate(self, value):
        assert isinstance(value, (int, float))
        assert value > 0.0
