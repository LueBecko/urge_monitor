# -*- coding: utf-8 -*-

from psychopy import visual
from . import helpers

lines = []
texts = []


def CreateScale(win, conf):
    # asserts
    assert isinstance(conf['scales_text'], list)
    assert isinstance(conf['scales_text_pos'], list)
    assert isinstance(conf['scales_text_size'], list)
    l = len(conf['scales_text'])
    assert (len(conf['scales_text_pos']) == l and
            len(conf['scales_text_size']) == l)
    assert all([isinstance(conf['scales_text'][i], str)
            for i in range(l)])
    assert all([isinstance(conf['scales_text_pos'][i], str)
            for i in range(l)])
    assert all([conf['scales_text_pos'][i] in ['a', 'b', 'c', 'l', 'r']
            for i in range(l)])
    assert all([isinstance(conf['scales_text_size'][i], (float, int))
            for i in range(l)])
    colorValidator = helpers.ColorValidator()
    colorValidator.validateColor(win.colorSpace, conf['scales_text_col'])
    colorValidator.validateColor(win.colorSpace, conf['scales_col'])
    assert isinstance(conf['scales_widthl'], (int, float))
    assert isinstance(conf['scales_widthr'], (int, float))
    assert isinstance(conf['scales_thickness'], (int, float))
    # create scales
    if l == 1:
        y = [0.0]
    else:
        y = [-0.5 + float(i) / float(l - 1) for i in range(l)]
    w = float(conf['bg_width']) / 2.0
    for si in range(l):
        # lines
        lines.append(visual.Line(win,
            start=(-conf['scales_widthl'] - w, y[si] * conf['bg_height']),
            end=(conf['scales_widthr'] + w, y[si] * conf['bg_height']),
            lineColor=conf['scales_col'],
            lineColorSpace=win.colorSpace,
            lineWidth=conf['scales_thickness'],
            opacity=1.0,
            autoLog=False,
            pos=conf['pos'],
            interpolate=False))
        lines[-1].setAutoDraw(True)
        # texts
        p = conf['scales_text_pos'][si].lower()
        if p == 'c':  # center
            pos = (conf['pos'][0],
                conf['pos'][1] + y[si] * conf['bg_height'])
            av = 'center'
        elif p == 'a':  # above
            pos = (conf['pos'][0],
                conf['pos'][1] + y[si] * conf['bg_height']
                + conf['scales_text_size'][si])
            av = 'center'
        elif p == 'b':  # below
            pos = (conf['pos'][0],
                conf['pos'][1] + y[si] * conf['bg_height']
                - conf['scales_text_size'][si])
            av = 'center'
        elif p == 'l':  # left
            pos = (conf['pos'][0] - conf['scales_widthl'] - w,
                conf['pos'][1] + y[si] * conf['bg_height'])
            av = 'right'
        elif p == 'r':  # right
            pos = (conf['pos'][0] + conf['scales_widthr'] + w,
                conf['pos'][1] + y[si] * conf['bg_height'])
            av = 'left'
        texts.append(visual.TextStim(win,
            text=conf['scales_text'][si],
            font='',  # use window font
            pos=pos,
            color=conf['scales_text_col'],
            height=conf['scales_text_size'][si],
            colorSpace=win.colorSpace,
            opacity=1.0,
            contrast=1.0,
            ori=0.0,
            antialias=True,
            bold=False,
            italic=False,
            anchorHoriz=av,
            anchorVert='center',
            wrapWidth=None,
            flipHoriz=False,
            flipVert=False,
            autoLog=False))
        texts[-1].setAutoDraw(True)
