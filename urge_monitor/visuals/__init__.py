# -*- coding: utf-8 -*-

from psychopy import visual, monitors, logging

from . import helpers, bars, hist, annote, scale

# variables of the module
__Cmon = {}
__Cwin = {}
__Cvis = {}


def CreateVisuals(Cmon, Cwin, Cvis):
    '''1. receives the config information from the main loop
    2. creates monitor and window instances
    3. adds all drawable elements'''
    SetConfig(Cmon, Cwin, Cvis)
    CreateMon()
    CreateWin()
    CreateVis()


def SetConfig(Cmon, Cwin, Cvis):
    '''receives the config information from the main loop'''
    if Cmon is not None:
        assert isinstance(Cmon, dict)
        __Cmon.update(Cmon)
    if Cwin is not None:
        assert isinstance(Cwin, dict)
        __Cwin.update(Cwin)
    if Cvis is not None:
        assert isinstance(Cvis, dict)
        __Cvis.update(Cvis)


def CreateMon(Cmon=None):
    '''creates monitor object, can overwrite monitor config'''
    if Cmon is not None:
        assert isinstance(Cmon, dict)
        __Cmon.update(Cmon)
    # asserts
    assert isinstance(__Cmon['name'], str)
    assert isinstance(__Cmon['distance'], (int, float))
    assert isinstance(__Cmon['width'], (int, float))
    helpers.__assert_resolution__(__Cmon['resolution'])
    # create monitor
    CreateMon.__mon = monitors.Monitor(__Cmon['name'],
        distance=__Cmon['distance'],
        width=__Cmon['width'])
    CreateMon.__mon.setSizePix(__Cmon['resolution'])
    logging.info(msg='monitor interface generated: ' + __Cmon['name'])
CreateMon.__mon = None


def CreateWin(Cwin=None):
    '''creates win object, can overwrite win config'''
    if Cwin is not None:
        assert isinstance(Cwin, dict)
        __Cwin.update(Cwin)
    # asserts
    assert isinstance(__Cwin['color_space'], str)
    __Cwin['color_space'] = __Cwin['color_space'].lower()
    assert __Cwin['color_space'] in ['rgb', 'rgb255', 'hsv']
    helpers.__assert_resolution__(__Cwin['resolution'])
    assert isinstance(__Cwin['fullscr'], bool)
    # create win
    CreateWin.__win = visual.Window(size=__Cwin['resolution'],
                monitor=CreateMon.__mon,
                colorSpace=__Cwin['color_space'],
                color=__Cvis['col'],
                fullscr=__Cwin['fullscr'],
                screen=__Cwin['screen'],
                allowGUI=False,
                units='deg',
                waitBlanking=False,
                winType='pyglet')
    logging.info(msg='window created')
CreateWin.__win = None


def getWin():
    return CreateWin.__win


def flip():
    CreateWin.__win.flip()


def CreateVis(Cvis=None):
    '''creates all visual objects, can overwrite vis config'''
    if Cvis is not None:
        assert isinstance(Cvis, dict)
        __Cvis.update(Cvis)
    # set bg color
    validator = helpers.ColorValidator()
    validator.validateColor(__Cwin['color_space'], __Cvis['col'])
    getWin().setColor(__Cvis['col'])
    # start doing important stuff
    scale.CreateScale(getWin(), __Cvis)
    bars.CreateBGBar(getWin(), __Cvis)
    # optimize draw order (it's a bit of a dirty hack)
    for i in range(len(scale.texts)):
        scale.texts[i].setAutoDraw(False)
        scale.texts[i].setAutoDraw(True)
    bars.CreateFGBar(getWin(), __Cvis)
    hist.CreateHist(getWin(), __Cvis)
    annote.CreateAnnotes(getWin(), __Cvis)


def CloseVisuals():
    getWin().close()
    CreateWin.__win = None
    CreateMon.__mon = None
    bars.bg_bar = None
    bars.fg_bar = None
    hist.histl = []
    hist.histr = []
    hist.updateHist = lambda urgevalue: None
    hist.hist_x = []
    hist.hist_y = []
    hist.vertical_max = 0
    annote.__win = None
    annote.drawable = {}
    scale.lines = []
    scale.texts = []
