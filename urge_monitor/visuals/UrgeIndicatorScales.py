from psychopy import visual
from . import helpers
from .ConfigurableVisualElement import ConfigurableVisualElement
from .validators import PositiveNumericValueValidator
from .validators import NotNegativeNumericValueValidator

class UrgeIndicatorScales(ConfigurableVisualElement):
    '''manages the lifecycle of the scales of the urge indicator'''

    def __init__(self, window, visualConfiguration):
        self.__window = window
        self.__createDefaultConfigurationValues()
        super().__init__(visualConfiguration)
        self.createScales()

    def __createDefaultConfigurationValues(self):
        colorspaceTransformator = helpers.ColorspaceTransformator()
        white = colorspaceTransformator.colorspace_to_colorspace('rgb255', self.__window.colorSpace, [255, 255, 255])

        # TODO: central instance for default values used in several classes?
        self.__defaultConfig = {'pos': [0.0, 0.0],
            'scales_col': white,
            'scales_thickness': 4,
            'scales_widthl': 0.25,
            'scales_widthr': 0.25,
            'scales_text': [],
            'bg_width': 1,
            'bg_height': 7
            }

    def getConfigurationItemDefault(self, item):
        return self.__defaultConfig.get(item)

    def validateConfiguration(self):
        positiveNumericValidator = PositiveNumericValueValidator.PositiveNumericValueValidator()
        notNegativeNumericValidator = NotNegativeNumericValueValidator.NotNegativeNumericValueValidator()
        colorValidator = helpers.ColorValidator()
        positionValidator = helpers.PositionValidator()
        positionValidator.validatePosition(self.getConfigurationValue('pos'))
        colorValidator.validateColor(self.__window.colorSpace, self.getConfigurationValue('scales_col'))
        positiveNumericValidator.validate(self.getConfigurationValue('scales_thickness'))
        notNegativeNumericValidator.validate(self.getConfigurationValue('scales_widthl'))
        notNegativeNumericValidator.validate(self.getConfigurationValue('scales_widthr'))
        positiveNumericValidator.validate(self.getConfigurationValue('bg_width'))
        positiveNumericValidator.validate(self.getConfigurationValue('bg_height'))
        assert isinstance(self.getConfigurationValue('scales_text'), (list, tuple))
        assert all([isinstance(text, str) for text in self.getConfigurationValue('scales_text')])

    def createScales(self):
        # TODO: this probably needs some tests
        numberOfScales = len(self.getConfigurationValue('scales_text'))
        if numberOfScales == 1:
            yPositions = [0.0]
        else:
            yPositions = [-0.5 + float(i) / float(numberOfScales - 1) for i in range(numberOfScales)]

        baseWidth = float(self.getConfigurationValue('bg_width')) / 2.0
        for indexOfScale in range(numberOfScales):
            line = visual.Line(self.__window,
                start=(-self.getConfigurationValue('scales_widthl') - baseWidth, yPositions[indexOfScale] * self.getConfigurationValue('bg_height')),
                end=(self.getConfigurationValue('scales_widthr') + baseWidth, yPositions[indexOfScale] * self.getConfigurationValue('bg_height')),
                lineColor=self.getConfigurationValue('scales_col'),
                lineColorSpace=self.__window.colorSpace,
                lineWidth=self.getConfigurationValue('scales_thickness'),
                opacity=1.0,
                autoLog=False,
                pos=self.getConfigurationValue('pos'),
                interpolate=False)
            line.setAutoDraw(True)
