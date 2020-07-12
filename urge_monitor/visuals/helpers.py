# -*- coding: utf-8 -*-


# Assertion helper functions
__assert_color__ = {'rgb': lambda col: __assert_color_rgb__(col),
                    'rgb255': lambda col: __assert_color_rgb255__(col),
                    'hsv': lambda col: __assert_color_hsv__(col)}


def __assert_color_rgb255__(col):
    assert isinstance(col, (list, tuple))
    assert len(col) == 3
    assert isinstance(col[0], (int, float))
    assert isinstance(col[1], (int, float))
    assert isinstance(col[2], (int, float))
    assert col[0] >= 0 and col[0] <= 255
    assert col[1] >= 0 and col[1] <= 255
    assert col[2] >= 0 and col[2] <= 255


def __assert_color_rgb__(col):
    assert isinstance(col, (list, tuple))
    assert len(col) == 3
    assert isinstance(col[0], (int, float))
    assert isinstance(col[1], (int, float))
    assert isinstance(col[2], (int, float))
    assert col[0] >= -1 and col[0] <= 1
    assert col[1] >= -1 and col[1] <= 1
    assert col[2] >= -1 and col[2] <= 1


def __assert_color_hsv__(col):
    assert isinstance(col, (list, tuple))
    assert len(col) == 3
    assert isinstance(col[0], (int, float))
    assert isinstance(col[1], (int, float))
    assert isinstance(col[2], (int, float))
    assert col[0] >= 0 and col[0] <= 360  # hue
    assert col[1] >= 0 and col[1] <= 1  # saturation
    assert col[2] >= 0 and col[2] <= 1  # value


def __assert_resolution__(res):
    assert isinstance(res, (list, tuple))
    assert len(res) == 2
    assert isinstance(res[0], int)
    assert isinstance(res[1], int)
    assert res[0] > 0
    assert res[1] > 0


def __assert_position__(pos):
    assert isinstance(pos, (list, tuple))
    assert len(pos) == 2
    assert isinstance(pos[0], (int, float))
    assert isinstance(pos[1], (int, float))


## TRANSFORMATIONS
__rgb_to_colspace = {'rgb': lambda col: col,
                    'rgb255': lambda col: __rgb_to_rgb255(col),
                    'hsv': lambda col: __rgb_to_hsv(col)}

__rgb255_to_colspace = {'rgb': lambda col: __rgb255_to_rgb(col),
                    'rgb255': lambda col: col,
                    'hsv': lambda col: __rgb255_to_hsv(col)}

__hsv_to_colspace = {'rgb': lambda col: __hsv_to_rgb(col),
                    'rgb255': lambda col: __hsv_to_rgb255(col),
                    'hsv': lambda col: col}

__colspace_to_rgb = {'rgb': lambda col: col,
                    'rgb255': lambda col: __rgb255_to_rgb(col),
                    'hsv': lambda col: __hsv_to_rgb(col)}

__colspace_to_rgb255 = {'rgb': lambda col: __rgb_to_rgb255(col),
                    'rgb255': lambda col: col,
                    'hsv': lambda col: __hsv_to_rgb255(col)}

__colspace_to_hsv = {'rgb': lambda col: __rgb_to_hsv(col),
                    'rgb255': lambda col: __rgb255_to_hsv(col),
                    'hsv': lambda col: col}


def __rgb_to_rgb255(col):
    __assert_color_rgb__(col)
    return [int(255 * (v + 1.0) / 2.0) for v in col]


def __rgb_to_hsv(col):
    __assert_color_rgb__(col)
    col01 = [(v + 1.0) / 2.0 for v in col]
    cmax = max(col01)
    cmin = max(col01)
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
    return [hue, sat, value]


def __rgb255_to_rgb(col):
    __assert_color_rgb255__(col)
    return [-1.0 + 2.0 * float(v) / 255.0 for v in col]


def __rgb255_to_hsv(col):
    __assert_color_rgb255__(col)
    col01 = [v / 255.0 for v in col]
    cmax = max(col01)
    cmin = max(col01)
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
    return [hue, sat, value]


def __hsv_to_rgb(col):
    __assert_color_hsv__(col)
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
    return [(v + m) * 2.0 - 1.0 for v in ctrans]


def __hsv_to_rgb255(col):
    __assert_color_hsv__(col)
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
    return [int((v + m) * 255) for v in ctrans]
