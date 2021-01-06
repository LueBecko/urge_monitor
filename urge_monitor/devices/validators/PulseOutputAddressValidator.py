
class PulseOutputAddressValidator:
    '''validates address value of out-pulse configuration'''

    def validate(self, value):
        assert isinstance(value, int)
        assert value >= 0
