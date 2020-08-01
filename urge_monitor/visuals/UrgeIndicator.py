# -*- coding: utf-8 -*-

from psychopy import visual
from . import helpers

class UrgeIndicator:
    '''manages the lifecycle of the urge indicator bar'''
    __backgroundBar: None
    __indicatorBar: None

    def __init__(self, window, visualConfig):
        self.__validateVisualConfig(window, visualConfig)
        self.__backgroundBar = self.__createBackgroundBar(window, visualConfig)
        self.__indicatorBar = self.__createIndicatorBar(window, visualConfig)

    def __validateVisualConfig(self, window, visualConfig):
        colorValidator = helpers.ColorValidator()
        positionValidator = helpers.PositionValidator()
        if 'pos' in visualConfig:
            positionValidator.validatePosition(visualConfig['pos'])
        # validate background bar config
        if 'bg_height' in visualConfig:
            assert isinstance(visualConfig['bg_height'], (int, float))
        if 'bg_width' in visualConfig:
            assert isinstance(visualConfig['bg_width'], (int, float))
        if 'bg_col' in visualConfig:
            colorValidator.validateColor(window.colorSpace, visualConfig['bg_col'])
        if 'bg_frame_col' in visualConfig:
            colorValidator.validateColor(window.colorSpace, visualConfig['bg_frame_col'])
        if 'bg_frame_width' in visualConfig:
            assert isinstance(visualConfig['bg_frame_width'], int)
        # validate foreground bar config
        if 'fg_height' in visualConfig:
            assert isinstance(visualConfig['fg_height'], (int, float))
        if 'fg_width' in visualConfig:
            assert isinstance(visualConfig['fg_width'], (int, float))
        if 'fg_col' in visualConfig:
            colorValidator.validateColor(window.colorSpace, visualConfig['fg_col'])
        if 'fg_frame_col' in visualConfig:
            colorValidator.validateColor(window.colorSpace, visualConfig['fg_frame_col'])
        if 'fg_frame_width' in visualConfig:
            assert isinstance(visualConfig['fg_frame_width'], int)
        if 'fg_opacity' in visualConfig:
            assert isinstance(visualConfig['fg_opacity'], (int, float))
            assert visualConfig['fg_opacity'] >= 0
            assert visualConfig['fg_opacity'] <= 1

    def __createBackgroundBar(self, window, visualConfig):
        # extract config data and fill with defaults if anything is missing
        position = visualConfig.get('pos', [0.0, 0.0])
        bg_height = visualConfig.get('bg_height', 7)
        bg_width = visualConfig.get('bg_width', 1)

        grey = helpers.ColorspaceTransformator().colorspace_to_colorspace('rgb255', window.colorSpace, [127, 127, 127])
        bg_col = visualConfig.get('bg_col', grey)
        bg_frame_col = visualConfig.get('bg_frame_col', grey)
        bg_frame_width = visualConfig.get('bg_frame_width', 2)

        # create bg_bar object
        bg_bar = visual.ShapeStim(window,
                units='deg',
                fillColorSpace=window.colorSpace,
                lineColorSpace=window.colorSpace,
                fillColor=bg_col,
                lineColor=bg_frame_col,
                lineWidth=bg_frame_width,
                closeShape=True,
                pos=position,
                interpolate=False,
                opacity=1,
                autoLog=False,
                vertices=self.__createVertices(bg_width, bg_height))

        # finish
        bg_bar.bg_height = bg_height # make bg_height available for update methode
        bg_bar.draw()
        bg_bar.setAutoDraw(True)
        return bg_bar

    def __createIndicatorBar(self, window, visualConfig):
        # extract config data and fill with defaults if anything is missing
        position = visualConfig.get('pos', [0.0, 0.0])
        fg_height = visualConfig.get('fg_height', 0.5)
        fg_width = visualConfig.get('fg_width', 1.25)

        darkgrey = helpers.ColorspaceTransformator().colorspace_to_colorspace('rgb255', window.colorSpace, [95, 95, 95])
        fg_col = visualConfig.get('fg_col', darkgrey)
        fg_frame_col = visualConfig.get('fg_frame_col', darkgrey)
        fg_frame_width = visualConfig.get('fg_frame_width', 2)
        fg_opacity = visualConfig.get('fg_opacity', 1)

        # create fg_bar object
        fg_bar = visual.ShapeStim(window,
                units='deg',
                fillColorSpace=window.colorSpace,
                lineColorSpace=window.colorSpace,
                fillColor=fg_col,
                lineColor=fg_frame_col,
                lineWidth=fg_frame_width,
                closeShape=True,
                pos=position,
                interpolate=False,
                opacity=fg_opacity,
                autoLog=False,
                vertices=self.__createVertices(fg_width, fg_height))

        # finish
        fg_bar.draw()
        return fg_bar

    def __createVertices(self, width, height):
        return [[width / 2.0, -height / 2.0],
            [-width / 2.0, -height / 2.0],
            [-width / 2.0, height / 2.0],
            [width / 2.0, height / 2.0]]

    def updateUrge(self, urgeValue):
        """refresh indicator position, redraw happens automatically"""
        self.__indicatorBar.setPos(newPos=(self.__backgroundBar.pos[0],
            self.__backgroundBar.pos[1] + self.__backgroundBar.bg_height * (urgeValue - 0.5)))

    def fixDrawOrder(self):
        '''indicator must always be above all other non-annotation elements'''
        self.__indicatorBar.setAutoDraw(True)
