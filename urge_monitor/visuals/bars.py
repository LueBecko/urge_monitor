# -*- coding: utf-8 -*-

from psychopy import visual
from . import helpers


bg_bar = None
fg_bar = None


def CreateBGBar(win, conf):
    '''CreateBGBar creates bg bar'''
    global bg_bar
    # test parameters: pos
    if 'pos' in conf:
        helpers.PositionValidator().validatePosition(conf['pos'])
    else:
        conf['pos'] = [0.0, 0.0]

    # test parameters: bg_height
    if 'bg_height' in conf:
        assert isinstance(conf['bg_height'], (int, float))
    else:
        conf['bg_height'] = 7

    # test parameters: bg_width
    if 'bg_width' in conf:
        assert isinstance(conf['bg_width'], (int, float))
    else:
        conf['bg_width'] = 1

    verts = [[conf['bg_width'] / 2.0, -conf['bg_height'] / 2.0],
        [-conf['bg_width'] / 2.0, -conf['bg_height'] / 2.0],
        [-conf['bg_width'] / 2.0, conf['bg_height'] / 2.0],
        [conf['bg_width'] / 2.0, conf['bg_height'] / 2.0]]

    colorValidator = helpers.ColorValidator()
    grey = helpers.ColorspaceTransformator().colorspace_to_colorspace('rgb255', win.colorSpace, [127, 127, 127])
    # test parameters: bg_col
    if 'bg_col' in conf:
        colorValidator.validateColor(win.colorSpace, conf['bg_col'])
    else:
        conf['bg_col'] = grey

    # test parameters: bg_frame_col
    if 'bg_frame_col' in conf:
        colorValidator.validateColor(win.colorSpace, conf['bg_frame_col'])
    else:
        conf['bg_frame_col'] = grey

    # test parameters: bg_frame_width
    if 'bg_frame_width' in conf:
        assert isinstance(conf['bg_frame_width'], int)
    else:
        conf['bg_frame_width'] = 1

    # create bg_bar object
    bg_bar = visual.ShapeStim(win,
            units='deg',
            fillColorSpace=win.colorSpace,
            lineColorSpace=win.colorSpace,
            fillColor=conf['bg_col'],
            lineColor=conf['bg_frame_col'],
            lineWidth=conf['bg_frame_width'],
            closeShape=True,
            pos=conf['pos'],
            interpolate=False,
            opacity=1,
            autoLog=False,
            vertices=verts)

    # finish
    bg_bar.bg_height = conf['bg_height']
    bg_bar.draw()
    bg_bar.setAutoDraw(True)


def CreateFGBar(win, conf):
    '''CreateFGBar creates fg bar'''
    global fg_bar
    # test parameters: pos
    if 'pos' in conf:
        helpers.PositionValidator().validatePosition(conf['pos'])
    else:
        conf['pos'] = [0.0, 0.0]

    # test parameters: fg_height
    if 'fg_height' in conf:
        assert isinstance(conf['fg_height'], (int, float))
    else:
        conf['fg_height'] = 7

    # test parameters: fg_width
    if 'fg_width' in conf:
        assert isinstance(conf['fg_width'], (int, float))
    else:
        conf['fg_width'] = 1

    verts = [[conf['fg_width'] / 2.0, -conf['fg_height'] / 2.0],
        [-conf['fg_width'] / 2.0, -conf['fg_height'] / 2.0],
        [-conf['fg_width'] / 2.0, conf['fg_height'] / 2.0],
        [conf['fg_width'] / 2.0, conf['fg_height'] / 2.0]]

    colorValidator = helpers.ColorValidator()
    darkgrey = helpers.ColorspaceTransformator().colorspace_to_colorspace('rgb255', win.colorSpace, [95, 95, 95])
    # test parameters: fg_col
    if 'fg_col' in conf:
        colorValidator.validateColor(win.colorSpace, conf['fg_col'])
    else:
        conf['fg_col'] = darkgrey

    # test parameters: fg_frame_col
    if 'fg_frame_col' in conf:
        colorValidator.validateColor(win.colorSpace, conf['fg_frame_col'])
    else:
        conf['fg_frame_col'] = darkgrey

    # test parameters: fg_frame_width
    if 'fg_frame_width' in conf:
        assert isinstance(conf['fg_frame_width'], int)
    else:
        conf['fg_frame_width'] = 1

    # create fg_bar object
    fg_bar = visual.ShapeStim(win,
            units='deg',
            fillColorSpace=win.colorSpace,
            lineColorSpace=win.colorSpace,
            fillColor=conf['fg_col'],
            lineColor=conf['fg_frame_col'],
            lineWidth=conf['fg_frame_width'],
            closeShape=True,
            pos=conf['pos'],
            interpolate=False,
            opacity=conf['fg_opacity'],
            autoLog=False,
            vertices=verts)

    # finish
    fg_bar.draw()
    fg_bar.setAutoDraw(True)


def UpdateFGBar(urgevalue):
    """refresh bar position, redraw happens automatically"""
    global bg_bar, fg_bar
    fg_bar.setPos(newPos=(bg_bar.pos[0],
        bg_bar.pos[1] + bg_bar.bg_height * (urgevalue - 0.5)))
