
class PulseOutputDataValidator:
    '''validates data value of out-pulse configuration'''

    def validate(self, value):
        assert isinstance(value, int)
        assert value >= 0
        assert value < 256
