# -*- coding: utf-8 -*-

from psychopy import visual
from . import helpers


# both vars are static class members
__win = None
drawable = {}


def AddAnnote(name, text, pos, size, col):
    # asserts
    assert isinstance(name, str)
    assert isinstance(text, str)
    helpers.PositionValidator().validatePosition(pos)
    assert isinstance(size, (float, int))
    validator = helpers.ColorValidator()
    validator.validateColor(__win.colorSpace, col)
    assert name not in drawable
    # create graphical object
    drawable[name] = visual.TextStim(__win,
        text=text,
        font='',  # use window font
        pos=pos,
        color=col,
        colorSpace=__win.colorSpace,
        opacity=1.0,
        contrast=1.0,
        ori=0.0,
        height=size,
        antialias=True,
        bold=False,
        italic=False,
        anchorHoriz='center',
        anchorVert='center',
        wrapWidth=None,
        flipHoriz=False,
        flipVert=False,
        name=name,
        autoLog=False)
    drawable[name].setAutoDraw(True)


def DelAnnote(name):
    del drawable[name]


def CreateAnnotes(win, conf):
    # asserts
    l = len(conf['aname'])
    assert (len(conf['atext']) == l and len(conf['apos']) == l and
        len(conf['apos']) == l and len(conf['asize']) == l and
         len(conf['acol']) == l)
    # begin creating annotations
    global __win
    __win = win
    for ai in range(len(conf['aname'])):
        AddAnnote(name=conf['aname'][ai],
            text=conf['atext'][ai],
            pos=conf['apos'][ai],
            size=conf['asize'][ai],
            col=conf['acol'][ai])
