# -*- coding: utf-8 -*-

from psychopy import visual
from . import helpers

histl = []
histr = []
updateHist = lambda urgevalue: None
hist_x = []
hist_y = []
vertical_max = 0


def CreateHist(win, conf):
    '''top creator for hist objects, calls suitable sub create functions
    first checks all conf parameters'''
    # asserts
    if 'hist_fade' in conf:
        assert isinstance(conf['hist_fade'], bool)
    else:
        conf['hist_fade'] = False
    if 'hist_samples' in conf:
        assert isinstance(conf['hist_samples'], int)
    else:
        conf['hist_samples'] = 30
    if conf['hist_width']:
        assert isinstance(conf['hist_width'], (int, float))
    else:
        conf['hist_width'] = 3.0
    if 'hist_line_width' in conf:
        assert isinstance(conf['hist_line_width'], int)
    else:
        conf['hist_line_width'] = 2
    if 'hist_col' in conf:
        helpers.__assert_color__[win.colorSpace](conf['hist_col'])
    else:
        conf['hist_col'] = (
            helpers.__rgb255_to_colspace[win.colorSpace]([255, 255, 255]))
    if 'hist_side' in conf:
        assert isinstance(conf['hist_side'], str)
        conf['hist_side'] = conf['hist_side'].lower()
        assert conf['hist_side'] in ['left', 'right', 'both', 'none']
    else:
        conf['hist_side'] = 'none'
    # dispatch
    global hist_x, hist_y
    global vertical_max
    hist_x = [float(i * conf['hist_width']) / conf['hist_samples'] +
                conf['fg_width'] / 2.0 for i in range(conf['hist_samples'])]
    hist_y = [0.0] * conf['hist_samples']
    vertical_max = conf['bg_height']
    if conf['hist_fade']:
        CreateHist_fade(win, conf)
    else:
        CreateHist_nofade(win, conf)
    global updateHist
    updateHist = updatefuncs.get(conf['hist_fade']).get(conf['hist_side'])


def CreateHist_fade(win, conf):
    '''creates fading hist objects'''
    global histl, histr, hist_x, hist_y
    opinc = -1.0 / conf['hist_samples']
    for c in range(conf['hist_samples'] - 1):
        if conf['hist_side'] in ['left', 'both']:
            histl.append(visual.Line(win,
                start=(-hist_x[c], hist_y[c]),
                end=(-hist_x[c + 1], hist_y[c + 1]),
                lineColor=conf['hist_col'],
                lineColorSpace=win.colorSpace,
                lineWidth=conf['hist_line_width'],
                opacity=1.0 + c * opinc,
                autoLog=False,
                pos=conf['pos'],
                interpolate=False))
            histl[-1].setAutoDraw(True)
        if conf['hist_side'] in ['right', 'both']:
            histr.append(visual.Line(win,
                start=(hist_x[c], hist_y[c]),
                end=(hist_x[c + 1], hist_y[c + 1]),
                lineColor=conf['hist_col'],
                lineColorSpace=win.colorSpace,
                lineWidth=conf['hist_line_width'],
                opacity=1.0 + c * opinc,
                autoLog=False,
                pos=conf['pos'],
                interpolate=False))
            histr[-1].setAutoDraw(True)


def CreateHist_nofade(win, conf):
    '''creates non-fading hist objects'''
    global histl, histr, hist_x, hist_y
    if conf['hist_side'] in ['left', 'both']:
        C = [[-hist_x[i], hist_y[i]] for i in range(conf['hist_samples'])]
        histl.append(visual.ShapeStim(win,
            vertices=C,
            closeShape=False,
            fillColor=None,
            lineColor=conf['hist_col'],
            lineColorSpace=win.colorSpace,
            lineWidth=conf['hist_line_width'],
            opacity=1.0,
            autoLog=False,
            pos=conf['pos'],
            interpolate=False))
        histl[-1].setAutoDraw(True)
    if conf['hist_side'] in ['right', 'both']:
        C = [[hist_x[i], hist_y[i]] for i in range(conf['hist_samples'])]
        histr.append(visual.ShapeStim(win,
            vertices=C,
            closeShape=False,
            fillColor=None,
            lineColor=conf['hist_col'],
            lineColorSpace=win.colorSpace,
            lineWidth=conf['hist_line_width'],
            opacity=1.0,
            autoLog=False,
            pos=conf['pos'],
            interpolate=False))
        histr[-1].setAutoDraw(True)


updatefuncs = {True: {
        'none': lambda urgevalue: None,
        'left': lambda urgevalue: updateHist_fade_l(urgevalue),
        'right': lambda urgevalue: updateHist_fade_r(urgevalue),
        'both': lambda urgevalue: updateHist_fade_b(urgevalue)},
         False: {
        'none': lambda urgevalue: None,
        'left': lambda urgevalue: updateHist_nofade_l(urgevalue),
        'right': lambda urgevalue: updateHist_nofade_r(urgevalue),
        'both': lambda urgevalue: updateHist_nofade_b(urgevalue)}
        }


def updateHist_fade_l(urgevalue):
    global hist_y, hist_x, histl
    hist_y[1:] = hist_y[0:(len(hist_y) - 1)]
    hist_y[0] = vertical_max * (urgevalue - 0.5)
    for c in range(0, len(hist_y) - 1):
        histl[c].setVertices(value=[
                    [-hist_x[c], hist_y[c]], [-hist_x[c + 1], hist_y[c + 1]]])


def updateHist_fade_r(urgevalue):
    global hist_y, hist_x, histr
    hist_y[1:] = hist_y[0:(len(hist_y) - 1)]
    hist_y[0] = vertical_max * (urgevalue - 0.5)
    for c in range(0, len(hist_y) - 1):
        histr[c].setVertices(value=[
                    [hist_x[c], hist_y[c]], [hist_x[c + 1], hist_y[c + 1]]])


def updateHist_fade_b(urgevalue):
    global hist_y, hist_x, histl, histr
    hist_y[1:] = hist_y[0:(len(hist_y) - 1)]
    hist_y[0] = vertical_max * (urgevalue - 0.5)
    for c in range(0, len(hist_y) - 1):
        histl[c].setVertices(value=[
                    [-hist_x[c], hist_y[c]], [-hist_x[c + 1], hist_y[c + 1]]])
        histr[c].setVertices(value=[
                    [hist_x[c], hist_y[c]], [hist_x[c + 1], hist_y[c + 1]]])


def updateHist_nofade_l(urgevalue):
    global hist_y, hist_x, histl
    hist_y[1:] = hist_y[0:(len(hist_y) - 1)]
    hist_y[0] = vertical_max * (urgevalue - 0.5)
    histl[0].setVertices(list(zip([-x for x in hist_x], hist_y)))


def updateHist_nofade_r(urgevalue):
    global hist_y, hist_x, histr
    hist_y[1:] = hist_y[0:(len(hist_y) - 1)]
    hist_y[0] = vertical_max * (urgevalue - 0.5)
    histr[0].setVertices(list(zip(hist_x, hist_y)))


def updateHist_nofade_b(urgevalue):
    global hist_y, hist_x, histl, histr
    hist_y[1:] = hist_y[0:(len(hist_y) - 1)]
    hist_y[0] = vertical_max * (urgevalue - 0.5)
    histr[0].setVertices(list(zip(hist_x, hist_y)))
    histl[0].setVertices(list(zip([-x for x in hist_x], hist_y)))
