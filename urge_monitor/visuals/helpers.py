# TODO: split in several single class files and move them to a sub package validation

class ResolutionValidator:
    '''used to validate Resolution Values'''
    def validateResolution(self, resolution):
        assert isinstance(resolution, (list, tuple))
        assert len(resolution) == 2
        assert isinstance(resolution[0], int)
        assert isinstance(resolution[1], int)
        assert resolution[0] > 0
        assert resolution[1] > 0

class PositionValidator:
    '''used to validate Position Values'''
    def validatePosition(self, position):
        assert isinstance(position, (list, tuple))
        assert len(position) == 2
        assert isinstance(position[0], (int, float))
        assert isinstance(position[1], (int, float))

class ColorValidator:
    '''used to validate Color Space and Color Values'''
    def __assert_color_rgb255__(self, col):
        assert isinstance(col, (list, tuple))
        assert len(col) == 3
        assert isinstance(col[0], (int, float))
        assert isinstance(col[1], (int, float))
        assert isinstance(col[2], (int, float))
        assert col[0] >= 0 and col[0] <= 255
        assert col[1] >= 0 and col[1] <= 255
        assert col[2] >= 0 and col[2] <= 255

    def __assert_color_rgb__(self, col):
        assert isinstance(col, (list, tuple))
        assert len(col) == 3
        assert isinstance(col[0], (int, float))
        assert isinstance(col[1], (int, float))
        assert isinstance(col[2], (int, float))
        assert col[0] >= -1 and col[0] <= 1
        assert col[1] >= -1 and col[1] <= 1
        assert col[2] >= -1 and col[2] <= 1

    def __assert_color_hsv__(self, col):
        assert isinstance(col, (list, tuple))
        assert len(col) == 3
        assert isinstance(col[0], (int, float))
        assert isinstance(col[1], (int, float))
        assert isinstance(col[2], (int, float))
        assert col[0] >= 0 and col[0] <= 360  # hue
        assert col[1] >= 0 and col[1] <= 1  # saturation
        assert col[2] >= 0 and col[2] <= 1  # value

    __validations = {'rgb': lambda self, col: self.__assert_color_rgb__(col),
                    'rgb255': lambda self, col: self.__assert_color_rgb255__(col),
                    'hsv': lambda self, col: self.__assert_color_hsv__(col)}

    def validateColor(self, colorSpace, colorValue):
        self.validateColorSpace(colorSpace)
        self.__validations[colorSpace.lower()](self, colorValue)

    def validateColorSpace(self, colorSpace):
        assert isinstance(colorSpace, str)
        assert colorSpace.lower() in ['rgb', 'rgb255', 'hsv']


class ColorspaceTransformator:
    '''transforms colors from one color space to another (only supported colorspaces)'''
    def __rgb_to_rgb255(self, col):
        return tuple([int(255 * (v + 1.0) / 2.0) for v in col])

    def __rgb_to_hsv(self, col):
        col01 = [(v + 1.0) / 2.0 for v in col]
        cmax = max(col01)
        cmin = min(col01)
        delta = cmax - cmin
        # hue
        if delta == 0:
            hue = 0
        elif col01[0] == cmax:
            hue = 60.0 * (((col01[1] - col01[2]) / delta) % 6)
        elif col01[1] == cmax:
            hue = 60.0 * (((col01[2] - col01[0]) / delta) + 2)
        elif col01[2] == cmax:
            hue = 60.0 * (((col01[0] - col01[1]) / delta) + 4)
        # sat
        if cmax == 0:
            sat = 0
        else:
            sat = delta / cmax
        # value
        value = cmax
        # return
        return (hue, sat, value)

    def __rgb255_to_rgb(self, col):
        return tuple([-1.0 + 2.0 * float(v) / 255.0 for v in col])

    def __rgb255_to_hsv(self, col):
        col01 = [v / 255.0 for v in col]
        cmax = max(col01)
        cmin = min(col01)
        delta = cmax - cmin
        # hue
        if delta == 0:
            hue = 0
        elif col01[0] == cmax:
            hue = 60.0 * (((col01[1] - col01[2]) / delta) % 6)
        elif col01[1] == cmax:
            hue = 60.0 * (((col01[2] - col01[0]) / delta) + 2)
        elif col01[2] == cmax:
            hue = 60.0 * (((col01[0] - col01[1]) / delta) + 4)
        # sat
        if cmax == 0:
            sat = 0
        else:
            sat = delta / cmax
        # value
        value = cmax
        # return
        return (hue, sat, value)

    def __hsv_to_rgb(self, col):
        C = col[1] * col[2]
        X = C * (1 - abs(((col[0] / 60) % 2) - 1))
        m = col[2] - C
        if col[0] >= 0.0 and col[0] < 60.0:
            ctrans = [C, X, 0]
        elif col[0] >= 60.0 and col[0] < 120.0:
            ctrans = [X, C, 0]
        elif col[0] >= 120.0 and col[0] < 180.0:
            ctrans = [0, C, X]
        elif col[0] >= 180.0 and col[0] < 240.0:
            ctrans = [0, X, C]
        elif col[0] >= 240.0 and col[0] < 300.0:
            ctrans = [X, 0, C]
        elif col[0] >= 300.0 and col[0] < 360.0:
            ctrans = [C, 0, X]
        return tuple([(v + m) * 2.0 - 1.0 for v in ctrans])

    def __hsv_to_rgb255(self, col):
        C = col[1] * col[2]
        X = C * (1 - abs(((col[0] / 60) % 2) - 1))
        m = col[2] - C
        if col[0] >= 0.0 and col[0] < 60.0:
            ctrans = [C, X, 0]
        elif col[0] >= 60.0 and col[0] < 120.0:
            ctrans = [X, C, 0]
        elif col[0] >= 120.0 and col[0] < 180.0:
            ctrans = [0, C, X]
        elif col[0] >= 180.0 and col[0] < 240.0:
            ctrans = [0, X, C]
        elif col[0] >= 240.0 and col[0] < 300.0:
            ctrans = [X, 0, C]
        elif col[0] >= 300.0 and col[0] < 360.0:
            ctrans = [C, 0, X]
        return tuple([int((v + m) * 255) for v in ctrans])

    __transformers = {('rgb255','rgb'): lambda self, col: self.__rgb255_to_rgb(col),
            ('rgb255','rgb255'): lambda self, col: col,
            ('rgb255','hsv'): lambda self, col: self.__rgb255_to_hsv(col),
            ('rgb','rgb'): lambda self, col: col,
            ('rgb','rgb255'): lambda self, col: self.__rgb_to_rgb255(col),
            ('rgb','hsv'): lambda self, col: self.__rgb_to_hsv(col),
            ('hsv','rgb'): lambda self, col: self.__hsv_to_rgb(col),
            ('hsv','rgb255'): lambda self, col: self.__hsv_to_rgb255(col),
            ('hsv','hsv'): lambda self, col: col }

    __validator = ColorValidator()

    def colorspace_to_colorspace(self, sourceColorSpace, targetColorSpace, colorValue):
        self.__validator.validateColor(sourceColorSpace, colorValue)
        self.__validator.validateColorSpace(targetColorSpace)
        return self.__transformers[(sourceColorSpace,targetColorSpace)](self, colorValue)
    