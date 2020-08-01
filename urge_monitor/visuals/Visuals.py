from psychopy import visual, monitors, logging

from . import helpers, hist, annote, scale
from .UrgeIndicator import UrgeIndicator

class Visuals:
    '''handles the lifecycle of all visual objects needed for presentation of the experiment'''

    __monitor: None
    __window: None
    __urgeIndicator: None

    def __init__(self, configMonitor, configWindow, configVisualElements):
        self.__monitor = self.__createMonitor(configMonitor)
        self.__window = self.__createWindow(configWindow)
        self.__createVisualElements(configVisualElements, configWindow['color_space'])

    def __del__(self):
        if (self.getWindow() is not None):
            self.getWindow().close()
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

    def __createMonitor(self, configMonitor):
        # asserts
        assert isinstance(configMonitor['name'], str)
        assert isinstance(configMonitor['distance'], (int, float))
        assert isinstance(configMonitor['width'], (int, float))
        helpers.ResolutionValidator().validateResolution(configMonitor['resolution'])
        # create monitor
        __mon = monitors.Monitor(configMonitor['name'],
            distance=configMonitor['distance'],
            width=configMonitor['width'])
        __mon.setSizePix(configMonitor['resolution'])
        logging.info(msg='created monitor object: ' + configMonitor['name'])
        return __mon

    def __createWindow(self, configWindow):
        # asserts
        helpers.ColorValidator().validateColorSpace(configWindow['color_space'])
        helpers.ResolutionValidator().validateResolution(configWindow['resolution'])
        assert isinstance(configWindow['fullscr'], bool)
        # create win
        __win = visual.Window(size=configWindow['resolution'],
                    monitor=self.__monitor,
                    colorSpace=configWindow['color_space'].lower(),
                    color=configWindow['col'],
                    fullscr=configWindow['fullscr'],
                    screen=configWindow['screen'],
                    allowGUI=False,
                    units='deg',
                    waitBlanking=False,
                    winType='pyglet')
        logging.info(msg='created window')
        return __win

    def __createVisualElements(self, configVisualElements, colorSpace):
        # set bg color
        helpers.ColorValidator().validateColor(colorSpace, configVisualElements['col'])
        self.getWindow().setColor(configVisualElements['col'])

        scale.CreateScale(self.getWindow(), configVisualElements)
        self.__urgeIndicator = UrgeIndicator(self.getWindow(), configVisualElements)
        # fix draw order (dirty)
        for i in range(len(scale.texts)):
            scale.texts[i].setAutoDraw(False)
            scale.texts[i].setAutoDraw(True)
        self.__urgeIndicator.fixDrawOrder()

        hist.CreateHist(self.getWindow(), configVisualElements)
        annote.CreateAnnotes(self.getWindow(), configVisualElements)

    def getWindow(self):
        return self.__window

    def flip(self):
        self.__window.flip()

    def updateUrgeIndicator(self, urgeValue):
        self.__urgeIndicator.updateUrge(urgeValue)

    def updateHistoriePlot(self, urgeValue):
        hist.updateHist(urgeValue)
