from psychopy import visual
from . import helpers
from .ConfigurableVisualElement import ConfigurableVisualElement
from .validators import PositiveNumericValueValidator
from .validators import NotNegativeNumericValueValidator

class UrgeIndicatorScalesText(ConfigurableVisualElement):
    '''manages the lifecycle of the scale annotations of the urge indicator'''

    def __init__(self, window, visualConfiguration):
        self.__window = window
        self.__createDefaultConfigurationValues()
        super().__init__(visualConfiguration)
        self.validateConfiguration()
        self.createScaleTexts()

    def __createDefaultConfigurationValues(self):
        colorspaceTransformator = helpers.ColorspaceTransformator()
        white = colorspaceTransformator.colorspace_to_colorspace('rgb255', self.__window.colorSpace, [255, 255, 255])

        self.__defaultConfig = {'pos': [0.0, 0.0],
            'bg_width': 1,
            'bg_height': 7,
            'scales_text_col': white,
            'scales_text': [],
            'scales_text_pos': [],
            'scales_text_size': [],
            'scales_widthl': 0.25,
            'scales_widthr': 0.25
            }

    def getConfigurationItemDefault(self, item):
        return self.__defaultConfig.get(item)

    def validateConfiguration(self):
        positiveNumericValidator = PositiveNumericValueValidator.PositiveNumericValueValidator()
        notNegativeNumericValidator = NotNegativeNumericValueValidator.NotNegativeNumericValueValidator()
        colorValidator = helpers.ColorValidator()
        positionValidator = helpers.PositionValidator()
        positionValidator.validatePosition(self.getConfigurationValue('pos'))
        colorValidator.validateColor(self.__window.colorSpace, self.getConfigurationValue('scales_text_col'))
        notNegativeNumericValidator.validate(self.getConfigurationValue('scales_widthl'))
        notNegativeNumericValidator.validate(self.getConfigurationValue('scales_widthr'))
        positiveNumericValidator.validate(self.getConfigurationValue('bg_width'))
        positiveNumericValidator.validate(self.getConfigurationValue('bg_height'))
        assert isinstance(self.getConfigurationValue('scales_text'), (list, tuple))
        assert all([isinstance(text, str) for text in self.getConfigurationValue('scales_text')])

    def createScaleTexts(self):
        # TODO: this code needs tests and probably some refactoring (position computation)
        position = self.getConfigurationValue('pos')
        numberOfScales = len(self.getConfigurationValue('scales_text'))
        if numberOfScales == 1:
            yPositions = [0.0]
        else:
            yPositions = [-0.5 + float(i) / float(numberOfScales - 1) for i in range(numberOfScales)]

        baseWidth = float(self.getConfigurationValue('bg_width')) / 2.0
        bg_height = self.getConfigurationValue('bg_height')
        for indexOfScale in range(numberOfScales):
            textSize = self.getConfigurationValue('scales_text_size')[indexOfScale]
            positionLabel = self.getConfigurationValue('scales_text_pos')[indexOfScale].lower()
            if positionLabel == 'c':  # center
                pos = (position[0], position[1] + yPositions[indexOfScale] * bg_height)
                anchor = 'center'
            elif positionLabel == 'a':  # above
                pos = (position[0], position[1] + yPositions[indexOfScale] * bg_height + textSize)
                anchor = 'center'
            elif positionLabel == 'b':  # below
                pos = (position[0], position[1] + yPositions[indexOfScale] * bg_height - textSize)
                anchor = 'center'
            elif positionLabel == 'l':  # left
                pos = (position[0] - self.getConfigurationValue('scales_widthl') - baseWidth, position[1] + yPositions[indexOfScale] * bg_height)
                anchor = 'right'
            elif positionLabel == 'r':  # right
                pos = (position[0] + self.getConfigurationValue('scales_widthr') + baseWidth, position[1] + yPositions[indexOfScale] * bg_height)
                anchor = 'left'

            text = visual.TextStim(self.__window,
                text=self.getConfigurationValue('scales_text')[indexOfScale],
                font='',  # use window font
                pos=pos,
                color=self.getConfigurationValue('scales_text_col'),
                height=textSize,
                colorSpace=self.__window.colorSpace,
                opacity=1.0,
                contrast=1.0,
                ori=0.0,
                antialias=True,
                bold=False,
                italic=False,
                anchorHoriz=anchor,
                anchorVert='center',
                wrapWidth=None,
                flipHoriz=False,
                flipVert=False,
                autoLog=False)
            text.setAutoDraw(True)
