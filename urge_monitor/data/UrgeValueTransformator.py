
class UrgeValueTransformator:
    ''' transforms the internal input urge value to the data range in which it will be reported '''
    def __init__(self, low = 1, high = 255):
        # assert provided values
        assert isinstance(low, int)
        assert isinstance(high, int)
        assert low > 0
        assert high > low
        assert high < 256

        self.__low__ = low;
        self.__high__ = high;
        self.__range__ = high - low;

    def transform(self, urgevalue):
        return int(urgevalue * self.__range__) + self.__low__;    
