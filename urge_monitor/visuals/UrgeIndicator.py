from psychopy import visual
from . import helpers
from .ConfigurableVisualElement import ConfigurableVisualElement
from .validators import PositiveNumericValueValidator, PositionValidator
from .UrgeIndicatorScales import UrgeIndicatorScales
from .UrgeIndicatorScalesText import UrgeIndicatorScalesText

class UrgeIndicator(ConfigurableVisualElement):
    '''manages the lifecycle of the urge indicator bars'''
    __backgroundBar: None
    __indicatorBar: None
    __window: None
    __urgeIndicatorScales: None
    __urgeIndicatorScalesText: None

    def __init__(self, window, visualConfig):
        self.__window = window
        self.__createDefaultConfigurationValues()
        super().__init__(visualConfig)
        self.__urgeIndicatorScales = UrgeIndicatorScales(self.__window, visualConfig)
        self.__backgroundBar = self.__createBackgroundBar()
        self.__urgeIndicatorScalesText = UrgeIndicatorScalesText(self.__window, visualConfig)
        self.__indicatorBar = self.__createIndicatorBar()

    def __createDefaultConfigurationValues(self):
        colorspaceTransformator = helpers.ColorspaceTransformator()
        grey = colorspaceTransformator.colorspace_to_colorspace('rgb255', self.__window.colorSpace, [127, 127, 127])
        darkgrey = colorspaceTransformator.colorspace_to_colorspace('rgb255', self.__window.colorSpace, [95, 95, 95])
        self.__defaultConfig = {'pos': [0.0, 0.0],
            'bg_height': 7,
            'bg_width': 1,
            'bg_col': grey,
            'bg_frame_col': grey,
            'bg_frame_width': 2,
            'fg_height': 0.5,
            'fg_width': 1.25,
            'fg_col': darkgrey,
            'fg_frame_col': darkgrey,
            'fg_frame_width': 2,
            'fg_opacity': 1}

    def getConfigurationItemDefault(self, item):
        return self.__defaultConfig.get(item)

    def validateConfiguration(self):
        positiveNumericValidator = PositiveNumericValueValidator.PositiveNumericValueValidator()
        colorValidator = helpers.ColorValidator()
        positionValidator = PositionValidator.PositionValidator()
        positionValidator.validate(self.getConfigurationValue('pos'))
        # validate background bar config
        positiveNumericValidator.validate(self.getConfigurationValue('bg_height'))
        positiveNumericValidator.validate(self.getConfigurationValue('bg_width'))
        colorValidator.validateColor(self.__window.colorSpace, self.getConfigurationValue('bg_col'))
        colorValidator.validateColor(self.__window.colorSpace, self.getConfigurationValue('bg_frame_col'))
        positiveNumericValidator.validate(self.getConfigurationValue('bg_frame_width'))
        # validate foreground bar config
        positiveNumericValidator.validate(self.getConfigurationValue('fg_height'))
        positiveNumericValidator.validate(self.getConfigurationValue('fg_width'))
        colorValidator.validateColor(self.__window.colorSpace, self.getConfigurationValue('fg_col'))
        colorValidator.validateColor(self.__window.colorSpace, self.getConfigurationValue('fg_frame_col'))
        positiveNumericValidator.validate(self.getConfigurationValue('fg_frame_width'))
        assert isinstance(self.getConfigurationValue('fg_opacity'), (int, float))
        assert self.getConfigurationValue('fg_opacity') >= 0
        assert self.getConfigurationValue('fg_opacity') <= 1

    def __createBackgroundBar(self):
        bg_height = self.getConfigurationValue('bg_height')
        bg_width = self.getConfigurationValue('bg_width')

        # create bg_bar object
        bg_bar = visual.ShapeStim(self.__window,
                units='deg',
                fillColorSpace=self.__window.colorSpace,
                lineColorSpace=self.__window.colorSpace,
                fillColor=self.getConfigurationValue('bg_col'),
                lineColor=self.getConfigurationValue('bg_frame_col'),
                lineWidth=self.getConfigurationValue('bg_frame_width'),
                closeShape=True,
                pos=self.getConfigurationValue('pos'),
                interpolate=False,
                opacity=1,
                autoLog=False,
                vertices=self.__createVertices(bg_width, bg_height))

        bg_bar.bg_height = bg_height # make bg_height available for update methode
        bg_bar.draw()
        bg_bar.setAutoDraw(True)
        return bg_bar

    def __createIndicatorBar(self):
        fg_height = self.getConfigurationValue('fg_height')
        fg_width = self.getConfigurationValue('fg_width')

        # create fg_bar object
        fg_bar = visual.ShapeStim(self.__window,
                units='deg',
                fillColorSpace=self.__window.colorSpace,
                lineColorSpace=self.__window.colorSpace,
                fillColor=self.getConfigurationValue('fg_col'),
                lineColor=self.getConfigurationValue('fg_frame_col'),
                lineWidth=self.getConfigurationValue('fg_frame_width'),
                closeShape=True,
                pos=self.getConfigurationValue('pos'),
                interpolate=False,
                opacity=self.getConfigurationValue('fg_opacity'),
                autoLog=False,
                vertices=self.__createVertices(fg_width, fg_height))

        fg_bar.draw()
        fg_bar.setAutoDraw(True)
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
