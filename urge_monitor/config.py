# reads config files and validates them

import configparser
import os
import warnings

from serial import (EIGHTBITS, FIVEBITS, PARITY_EVEN, PARITY_MARK, PARITY_NONE,
                    PARITY_ODD, PARITY_SPACE, SEVENBITS, SIXBITS, STOPBITS_ONE,
                    STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO)

from .InvalidConfigurationException import InvalidConfigurationException
from .visuals import helpers 
from .visuals.validators.ResolutionValidator import ResolutionValidator
from .visuals.validators.PositionValidator import PositionValidator
from .visuals.validators.ColorSpaceValidator import ColorSpaceValidator
from .devices.PulseOutput import PulseFiringPattern
NONE = PulseFiringPattern.NONE
ON_URGE_RECORD = PulseFiringPattern.ON_URGE_RECORD

class ExperimentConfig:
    """interface to read parameters from config files (RFC 822 compatible)"""

# TODO: factory methods for read experiment and read defaults
    def __init__(self, expName, baseDir):
        """reads experiment config and fills missing values with default values"""
        # setup
        self.configExp = {}
        self.configMon = {}
        self.configInp = {}
        self.configPul = {}
        self.configDef = {}
        self.configRuns = []
        # the experiment uses this config field to track runtime informations
        self.runtimeInfos = {}
        self.baseDir = baseDir
        self.expName = expName
        self.expFolder = ''
        self.expFile = ''
        self.monFile = ''
        self.inpFile = ''
        self.pulFile = ''
        self.defFile = ''
        # start reading
        self.ReadExperiment()
        self.ReadMonitor()
        self.ReadInputDevice()
        self.ReadPulseInfo()
        self.ReadDefaults()
        self.ReadRuns()

    def ReadExperiment(self):
        '''reads experiment configuration and checks for validity'''
        # checks
        self.expFolder = (self.baseDir + os.sep + 'exp' +
            os.sep + self.expName)
        if not os.path.isdir(self.expFolder):
            raise InvalidConfigurationException(self.expFolder,
                'The folder of the experiment is not a folder.')
        self.expFile = self.expFolder + os.sep + 'exp.ini'
        if not os.path.isfile(self.expFile):
            raise InvalidConfigurationException(self.expFolder,
                'The folder does not contain exp.ini.')
        # start reading the experiment
        cp = configparser.RawConfigParser()
        cp.read(self.expFile)
        for se in cp.sections():
            self.configExp[se] = {}
            if se != 'runs':
                for it in cp.options(se):
                    self.configExp[se][it] = eval(cp.get(se, it))
            else:  # read runs as tupel to keep input order
                self.configExp[se] = cp.items(se)
        # validate the experiment configuration
        if not 'main' in self.configExp:
            raise InvalidConfigurationException(self.expFile, 'main section missing')
        if not 'name' in self.configExp['main']:
            raise InvalidConfigurationException(self.expFile, 'name entry missing')
        if not isinstance(self.configExp['main']['name'], str):
            raise InvalidConfigurationException(self.expFile,
                'name entry is not a string')
        if not 'log_folder' in self.configExp['main']:
            raise InvalidConfigurationException(self.expFile, 'log_folder missing')
        if not isinstance(self.configExp['main']['log_folder'], str):
            raise InvalidConfigurationException(self.expFile,
                'log_folder entry is not a string')
        if not 'abort_key' in self.configExp['main']:
            raise InvalidConfigurationException(self.expFile, 'abort_key missing')
        if not isinstance(self.configExp['main']['abort_key'], str):
            raise InvalidConfigurationException(self.expFile,
                'abort_key entry is not a string (key-code descriptor)')
        if not 'log_buttons' in self.configExp['main']:
            warnings.warn('exp.ini: main-log_buttons missing. Set to []')
            self.configExp['main']['log_buttons'] = []
        if not isinstance(self.configExp['main']['log_buttons'], (list, tuple)):
            raise InvalidConfigurationException(self.expFile,
                'log_buttons entry is not a list or tuple')
        for key in self.configExp['main']['log_buttons']:
            if not isinstance(key, str):
                raise InvalidConfigurationException(self.expFile,
                'log_buttons key entry is not a string (key-code descriptor)')
        if not 'info' in self.configExp:
            raise InvalidConfigurationException(self.expFile, 'info section missing')
        if not 'subj' in self.configExp['info']:
            self.configExp['info']['subj'] = 'Subject-Code'
            warnings.warn('Experiment configuration did not contain a subj.' +
            'Subj-Field was added by the programm.')
        if not 'runs' in self.configExp:
            raise InvalidConfigurationException(self.expFile, 'runs section missing')
        if len(self.configExp['runs']) == 0:
            raise InvalidConfigurationException(self.expFile, 'runs section is empty')
        for run in self.configExp['runs']:
            if not isinstance(eval(run[1]), str):
                raise InvalidConfigurationException(self.expFile,
                    ('entry for run ' + run[0] + ' has to be either empty or' +
                     ' a filename string (current value: ' + run[1] + ')'))
            if len(eval(run[1])) > 0:
                if not os.path.isfile((self.expFolder + os.sep + eval(run[1]))):
                    raise InvalidConfigurationException(self.expFile,
                        ('file ' + eval(run[1]) + ' of run ' + run[0] +
                        ' does not exist'))

    def ReadMonitor(self):
        # setup
        self.monFile = self.expFolder + os.sep + 'monitor.ini'
        if not os.path.isfile(self.monFile):
            self.monFile = self.baseDir + os.sep + 'monitor.ini'
            warnings.warn('Experiment did not contain a monitor file ' +
            '(monitor.ini). The default monitor file will be used (' +
            self.monFile + ')')
        # read
        cp = configparser.RawConfigParser()
        cp.read(self.monFile)
        for se in cp.sections():
            self.configMon[se] = {}
            for it in cp.options(se):
                self.configMon[se][it] = eval(cp.get(se, it))
        # validate
        if not 'monitor' in self.configMon:
            raise InvalidConfigurationException(self.monFile, 'no monitor section')
        if not 'name' in self.configMon['monitor']:
            self.configMon['monitor']['name'] = 'Monitor'
            warnings.warn('Monitor configuration was without monitor name.' +
                'default monitor name "Monitor" was set.')
        if not 'distance' in self.configMon['monitor']:
            raise InvalidConfigurationException(self.monFile,
                'monitor needs distance item')
        if not 'width' in self.configMon['monitor']:
            raise InvalidConfigurationException(self.monFile,
                'monitor needs width item')
        if not 'resolution' in self.configMon['monitor']:
            raise InvalidConfigurationException(self.monFile,
                'monitor needs resolution item')
        if not __is_numeric_pos__(self.configMon['monitor']['distance']):
            raise InvalidConfigurationException(self.monFile,
                'monitor distance needs to be a positive numerical')
        if not __is_numeric_pos__(self.configMon['monitor']['width']):
            raise InvalidConfigurationException(self.monFile,
                'monitor width needs to be a positive numerical')
        ResolutionValidator().validate(self.configMon['monitor']['resolution'])
        if not 'window' in self.configMon:
            self.configMon['window'] = {}
            warnings.warn('No window section given, it is generated ' +
                'automatically and will be filled with default values.')
        if not 'fullscr' in self.configMon['window']:
            self.configMon['window']['fullscr'] = True
            warnings.warn('missing window fullscr. Set to True.')
        elif not isinstance(self.configMon['window']['fullscr'], bool):
            raise InvalidConfigurationException(self.monFile,
                'window fullscr needs to be a boolean (True or False)')
        if not 'screen' in self.configMon['window']:
            self.configMon['window']['screen'] = 1
            warnings.warn('missing window screen. Set to 1.')
        elif not (isinstance(self.configMon['window']['screen'], int) and
                self.configMon['window']['screen'] >= 0):
            raise InvalidConfigurationException(self.monFile,
                'window screen needs to be a non-negative integer')
        if not 'color_space' in self.configMon['window']:
            self.configMon['window']['color_space'] = 'rgb255'
            warnings.warn('missing window color_space. Set to "rgb255".')
        ColorSpaceValidator().validate(self.configMon['window']['color_space'])
        if not 'col' in self.configMon['window']:
            self.configMon['window']['col'] = helpers.ColorspaceTransformator().colorspace_to_colorspace("rgb255",self.configMon['window']['color_space'], [0,0,0])
        if not 'resolution' in self.configMon['window']:
            self.configMon['window']['resolution'] = (
                self.configMon['monitor']['resolution'])
            warnings.warn('missing window resolution. ' +
                'Set to resolution of monitor.')
        ResolutionValidator().validate(self.configMon['window']['resolution'])

    def ReadInputDevice(self):
        # setup
        self.inpFile = self.expFolder + os.sep + 'input.ini'
        if not os.path.isfile(self.inpFile):
            self.inpFile = self.baseDir + os.sep + 'input.ini'
            warnings.warn('Experiment did not contain a input file ' +
            '(input.ini). The default input file will be used (' +
            self.inpFile + ')')
        # read
        cp = configparser.RawConfigParser()
        cp.read(self.inpFile)
        for se in cp.sections():
            self.configInp[se] = {}
            for it in cp.options(se):
                self.configInp[se][it] = eval(cp.get(se, it))
        if 'input' in self.configInp:
            self.configInp = self.configInp['input']
        else:
            raise InvalidConfigurationException(self.inpFile,
                'input.ini must contain one "input" section.')
        # validate
        if not isinstance(self.configInp['device'], str):
            raise InvalidConfigurationException(self.inpFile,
                'input.ini [input] must contain device item.')
        if not isinstance(self.configInp['sensitivity'], (int, float)):
            raise InvalidConfigurationException(self.inpFile,
                'input.ini [input] must contain sensitivity item.')
        if not self.configInp['device'] in ['Keyboard', 'KeyboardHub',
            'MousePosAbs', 'MousePosRel', 'MouseWheel', 'Auto',
            'Joystick', 'JoystickAbs']:
            raise InvalidConfigurationException(self.inpFile,
                'input.ini [input] device must be a string name of one of' +
                ' the supported device controls.')
        # validate keyboard control
        if self.configInp['device'] in ['Keyboard', 'KeyboardHub']:
            if not ('key_up' in self.configInp
                and 'key_down' in self.configInp):
                raise InvalidConfigurationException(self.inpFile,
                    'input.ini [input] keyboard needs items: key_up, key_down.')
            if not (isinstance(self.configInp['key_up'], str)
                and isinstance(self.configInp['key_down'], str)):
                raise InvalidConfigurationException(self.inpFile,
                    'input.ini [input] keyboard key values are strings.')
        # validate joystick control
        elif self.configInp['device'] in ['Joystick', 'JoystickAbs']:
            if not 'name' in self.configInp:
                raise InvalidConfigurationException(self.inpFile,
                    'input.ini [input] joystick needs item: name.')
            if not isinstance(self.configInp['name'], str):
                raise InvalidConfigurationException(self.inpFile,
                    'input.ini [input] joystick name must be a string.')
            if not 'channel_id' in self.configInp:
                raise InvalidConfigurationException(self.inpFile,
                    'input.ini [input] joystick needs item: channel_id.')
            if not isinstance(self.configInp['channel_id'], int):
                raise InvalidConfigurationException(self.inpFile,
                    'input.ini [input] joystick channel_id must be an integer.')
            if not self.configInp['channel_id'] >= 0:
                raise InvalidConfigurationException(self.inpFile,
                    'input.ini [input] joystick channel_id must be positive.')
            if not 'axis_hat' in self.configInp:
                raise InvalidConfigurationException(self.inpFile,
                    'input.ini [input] joystick needs item: axis_hat.')
            if not isinstance(self.configInp['axis_hat'], bool):
                raise InvalidConfigurationException(self.inpFile,
                    'input.ini [input] joystick axis_hat needs to be boolean.')

    def ReadPulseInfo(self):
        # setup
        self.pulFile = self.expFolder + os.sep + 'pulse.ini'
        if not os.path.isfile(self.pulFile):
            self.pulFile = self.baseDir + os.sep + 'pulse.ini'
            warnings.warn('Experiment did not contain a pulse file ' +
            '(pulse.ini). The default pulse file will be used (' +
            self.pulFile + ')')
        # read
        cp = configparser.RawConfigParser()
        cp.read(self.pulFile)
        for se in cp.sections():
            self.configPul[se] = {}
            for it in cp.options(se):
                self.configPul[se][it] = eval(cp.get(se, it))
        # validate
        if not 'pulse' in list(self.configPul.keys()):
            raise InvalidConfigurationException(self.pulFile,
                'no pulse section')
        if not 'simulation' in list(self.configPul['pulse'].keys()):
            self.configPul['pulse']['simulation'] = False
            warnings.warn('pulse-simulation not given! Set simulation=False')
        if not isinstance(self.configPul['pulse']['simulation'], bool):
            raise InvalidConfigurationException(self.pulFile,
                'pulse-simulation must be boolean (True, False)')
        if not 'play_sound_begin' in list(self.configPul['pulse'].keys()):
            self.configPul['pulse']['play_sound_begin'] = False
            warnings.warn('pulse-play_sound_begin not given! Set play_sound_begin=False')
        if not 'play_sound_end' in list(self.configPul['pulse'].keys()):
            self.configPul['pulse']['play_sound_end'] = False
            warnings.warn('pulse-play_sound_end not given! Set play_sound_end=False')
        if not 'send_out_pulse' in list(self.configPul['pulse'].keys()):
            self.configPul['pulse']['send_out_pulse'] = False
            warnings.warn('pulse-send_out_pulse not given! Set send_out_pulse=False')
        if not isinstance(self.configPul['pulse']['play_sound_begin'], bool):
            raise InvalidConfigurationException(self.pulFile,
                'pulse-play_sound_begin must be boolean (True, False)')
        if not isinstance(self.configPul['pulse']['play_sound_end'], bool):
            raise InvalidConfigurationException(self.pulFile,
                'pulse-play_sound_end must be boolean (True, False)')
        if not isinstance(self.configPul['pulse']['send_out_pulse'], bool):
            raise InvalidConfigurationException(self.pulFile,
                'pulse-send_out_pulse must be boolean (True, False)')
        # TODO: extract the interface specific validation into separate validators
        # parallel port
        if self.configPul['pulse']['interface'] == 'parallel':
            if not 'address' in list(self.configPul['parallel'].keys()):
                raise InvalidConfigurationException(self.pulFile,
                    'no pulse-parallel-address entry')
            if not isinstance(self.configPul['parallel']['address'], int):
                raise InvalidConfigurationException(self.pulFile,
                   'pulse-parallel-address must be integer & valid LPT address')
            if not 'pin' in list(self.configPul['parallel'].keys()):
                raise InvalidConfigurationException(self.pulFile,
                    'no pulse-parallel-pin entry')
            if not isinstance(self.configPul['parallel']['pin'], int):
                raise InvalidConfigurationException(self.pulFile,
                    'pulse-parallel-pin must be an integer')
        # serial
        elif self.configPul['pulse']['interface'] == 'serial':
            if not 'port' in list(self.configPul['serial'].keys()):
                raise InvalidConfigurationException(self.pulFile,
                    'no pulse-serial-port entry')
            if not isinstance(self.configPul['serial']['port'], str):
                raise InvalidConfigurationException(self.pulFile,
                   'pulse-serial-port must be port identifier string')
            if not 'baudrate' in list(self.configPul['serial'].keys()):
                raise InvalidConfigurationException(self.pulFile,
                    'no pulse-serial-baudrate entry')
            if not __is_numeric_pos__(self.configPul['serial']['baudrate']):
                raise InvalidConfigurationException(self.pulFile,
                   'pulse-serial-baudrate must be positive number')
            if not 'bytesize' in list(self.configPul['serial'].keys()):
                raise InvalidConfigurationException(self.pulFile,
                    'no pulse-serial-bytesize entry')
            if not self.configPul['serial']['bytesize'] in [
                FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS]:
                raise InvalidConfigurationException(self.pulFile,
                   'pulse-serial-bytesize must be one of: ' +
                   'FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS')
            if not 'parity' in list(self.configPul['serial'].keys()):
                raise InvalidConfigurationException(self.pulFile,
                    'no pulse-serial-parity entry')
            if not self.configPul['serial']['parity'] in [
                PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK,
                PARITY_SPACE]:
                raise InvalidConfigurationException(self.pulFile,
                   'pulse-serial-parity must be one of: ' +
                   'PARITY_NONE, PARITY_EVEN, PARITY_ODD PARITY_MARK, ' +
                   'PARITY_SPACE')
            if not 'stopbits' in list(self.configPul['serial'].keys()):
                raise InvalidConfigurationException(self.pulFile,
                    'no pulse-serial-stopbits entry')
            if not self.configPul['serial']['stopbits'] in [
                STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO]:
                raise InvalidConfigurationException(self.pulFile,
                   'pulse-serial-stopbits must be one of: ' +
                   'STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO')
            if not 'timeout' in list(self.configPul['serial'].keys()):
                raise InvalidConfigurationException(self.pulFile,
                    'no pulse-serial-timeout entry')
            if not self.configPul['serial']['timeout'] is None:
                if not (__is_numeric_pos__(self.configPul['serial']['timeout'])
                    or self.configPul['serial']['timeout'] == 0):
                    raise InvalidConfigurationException(self.pulFile,
                       'pulse-serial-timeout must be positive number')
            if not 'xonxoff' in list(self.configPul['serial'].keys()):
                warnings.warn('pulse-serial-xonxoff is missing, set to False')
                self.configPul['serial']['xonxoff'] = False
            if not isinstance(self.configPul['serial']['xonxoff'], bool):
                raise InvalidConfigurationException(self.pulFile,
                    'pulse-serial-xonxoff must be boolean (True, False)')
            if not 'rtscts' in list(self.configPul['serial'].keys()):
                warnings.warn('pulse-serial-rtscts is missing, set to False')
                self.configPul['serial']['rtscts'] = False
            if not isinstance(self.configPul['serial']['rtscts'], bool):
                raise InvalidConfigurationException(self.pulFile,
                    'pulse-serial-rtscts must be boolean (True, False)')
            if not 'dsrdtr' in list(self.configPul['serial'].keys()):
                warnings.warn('pulse-serial-dsrdtr is missing, set to False')
                self.configPul['serial']['dsrdtr'] = False
            if not isinstance(self.configPul['serial']['dsrdtr'], bool):
                raise InvalidConfigurationException(self.pulFile,
                    'pulse-serial-dsrdtr must be boolean (True, False)')
            if not 'inter_byte_timeout' in list(
                self.configPul['serial'].keys()):
                raise InvalidConfigurationException(self.pulFile,
                    'no pulse-serial-inter_byte_timeout entry')
            if not self.configPul['serial']['inter_byte_timeout'] is None:
                if not __is_numeric_pos__(self.configPul['serial'][
                    'inter_byte_timeout']):
                    raise InvalidConfigurationException(self.pulFile,
                       'pulse-serial-inter_byte_timeout must be ' +
                       ' positive number')
        # keyboard
        elif self.configPul['pulse']['interface'] == 'keyboard':
            if not 'key' in list(self.configPul['keyboard'].keys()):
                raise InvalidConfigurationException(self.pulFile,
                    'no pulse-keyboard-key entry')
            if not isinstance(self.configPul['keyboard']['key'], str):
                raise InvalidConfigurationException(self.pulFile,
                   'pulse-keyboard-key must be keyboard key identifier string')
        # sound_begin config
        if self.configPul['pulse']['play_sound_begin']:
            if not 'sound_begin' in list(self.configPul.keys()):
                warnings.warn('pulse-play_sound_begin set to True,' +
                    'but no sound_begin configuration given' +
                    'Default values will be used.')
                self.configPul['sound_begin'] = {}
            if not 'duration' in list(self.configPul['sound_begin'].keys()):
                self.configPul['sound_begin']['duration'] = 1.0
                warnings.warn('sound_begin-duration not given! Set duration=1.0 (s)')
            if not __is_numeric_pos__(self.configPul['sound_begin']['duration']):
                raise InvalidConfigurationException(self.pulFile,
                    'sound_begin-duration must be a positive number')
            if not 'volume' in list(self.configPul['sound_begin'].keys()):
                self.configPul['sound_begin']['volume'] = 1.0
                warnings.warn('sound_begin-volume not given! Set volume=1.0')
            if not __is_01interval__(self.configPul['sound_begin']['volume']):
                raise InvalidConfigurationException(self.pulFile,
                    'sound_begin-volume must be a number in [0,1]')
            if not 'value' in list(self.configPul['sound_begin'].keys()):
                self.configPul['sound_begin']['value'] = 440.0
                warnings.warn('sound_begin-value not given! Set value=440.0 Hz')
            if not __is_numeric_pos__(self.configPul['sound_begin']['value']):
                raise InvalidConfigurationException(self.pulFile,
                    'sound_begin-value must be a positive number')
        # sound_end config
        if self.configPul['pulse']['play_sound_end']:
            if not 'sound_end' in list(self.configPul.keys()):
                warnings.warn('pulse-play_sound_end set to True,' +
                    'but no sound_end configuration given' +
                    'Default values will be used.')
                self.configPul['sound_end'] = {}
            if not 'duration' in list(self.configPul['sound_end'].keys()):
                self.configPul['sound_end']['duration'] = 1.0
                warnings.warn('sound_end-duration not given! Set duration=1.0 (s)')
            if not __is_numeric_pos__(self.configPul['sound_end']['duration']):
                raise InvalidConfigurationException(self.pulFile,
                    'sound_end-duration must be a positive number')
            if not 'volume' in list(self.configPul['sound_end'].keys()):
                self.configPul['sound_end']['volume'] = 1.0
                warnings.warn('sound_end-volume not given! Set volume=1.0')
            if not __is_01interval__(self.configPul['sound_end']['volume']):
                raise InvalidConfigurationException(self.pulFile,
                    'sound_end-volume must be a number in [0,1]')
            if not 'value' in list(self.configPul['sound_end'].keys()):
                self.configPul['sound_end']['value'] = 440.0
                warnings.warn('sound_end-value not given! Set value=440.0 Hz')
            if not __is_numeric_pos__(self.configPul['sound_end']['value']):
                raise InvalidConfigurationException(self.pulFile,
                    'sound_end-value must be a positive number')

    def __ValidateRunConf__(self, conf, filename):
        colorValidator = helpers.ColorValidator()
        # validate control
        if not 'control' in list(conf.keys()):
            raise InvalidConfigurationException(filename,
                'no control section')
        if not 'run_time' in list(conf['control'].keys()):
            raise InvalidConfigurationException(filename,
                'no control-run_time entry')
        elif not __is_numeric_pos__(conf['control']['run_time']):
            raise InvalidConfigurationException(filename,
                'control-run_time needs to be a positive number')
        if not 'frame_rate' in list(conf['control'].keys()):
            raise InvalidConfigurationException(filename,
                'no control-frame_rate entry')
        elif not __is_numeric_pos__(conf['control']['frame_rate']):
            raise InvalidConfigurationException(filename,
                'control-frame_rate needs to be a positive number')
        if not 'hist_rate' in list(conf['control'].keys()):
            raise InvalidConfigurationException(filename,
                'no control-hist_rate entry')
        elif not __is_numeric_pos__(conf['control']['hist_rate']):
            raise InvalidConfigurationException(filename,
                'control-hist_rate needs to be a positive number')
        if not 'urge_sample_rate' in list(conf['control'].keys()):
            raise InvalidConfigurationException(filename,
                'no control-urge_sample_rate entry')
        elif not __is_numeric_pos__(conf['control']['urge_sample_rate']):
            raise InvalidConfigurationException(filename,
                'control-urge_sample_rate needs to be a positive number')
        # validate visuals
        cs = self.configMon['window']['color_space']
        colorTransformator = helpers.ColorspaceTransformator()
        black = colorTransformator.colorspace_to_colorspace('rgb255', cs, (0,0,0))
        darkgrey = colorTransformator.colorspace_to_colorspace('rgb255', cs, (95,95,95))
        grey = colorTransformator.colorspace_to_colorspace('rgb255', cs, (127,127,127))
        white = colorTransformator.colorspace_to_colorspace('rgb255', cs, (255,255,255))
        if not 'visuals' in list(conf.keys()):
            raise InvalidConfigurationException(filename,
                'no visuals section')
        if not 'col' in list(conf['visuals'].keys()):
            conf['visuals']['col'] = black
            warnings.warn(filename + ': no visuals-col, set to default black')
        colorValidator.validateColor(cs, conf['visuals']['col'])
        if not 'pos' in list(conf['visuals'].keys()):
            conf['visuals']['pos'] = [0, 0]
            warnings.warn(filename + ': no visuals-pos, set to center pos')
        PositionValidator().validate(conf['visuals']['pos'])
        # validate visuals-bg_*
        if not 'bg_height' in list(conf['visuals'].keys()):
            conf['visuals']['bg_height'] = 7
            warnings.warn(filename + ': no visuals-bg_height, set to 7')
        elif not __is_numeric_pos__(conf['visuals']['bg_height']):
            raise InvalidConfigurationException(filename,
                'visuals-bg_height must be a positive number')
        if not 'bg_width' in list(conf['visuals'].keys()):
            conf['visuals']['bg_width'] = 1
            warnings.warn(filename + ': no visuals-bg_width, set to 1')
        elif not __is_numeric_pos__(conf['visuals']['bg_width']):
            raise InvalidConfigurationException(filename,
                'visuals-bg_width must be a positive number')
        if not 'bg_col' in list(conf['visuals'].keys()):
            conf['visuals']['bg_col'] = grey
            warnings.warn(filename + ': no visuals-bg_col, set to grey')
        colorValidator.validateColor(cs, conf['visuals']['bg_col'])
        if not 'bg_frame_col' in list(conf['visuals'].keys()):
            conf['visuals']['bg_frame_col'] = grey
            warnings.warn(filename + ': no visuals-bg_frame_col, set to grey')
        colorValidator.validateColor(cs, conf['visuals']['bg_frame_col'])
        if not 'bg_frame_width' in list(conf['visuals'].keys()):
            conf['visuals']['bg_frame_width'] = 2
            warnings.warn(filename + ': no visuals-bg_frame_width, set to 2pt')
        elif not __is_numeric_pos__(conf['visuals']['bg_frame_width']):
            raise InvalidConfigurationException(filename,
                'visuals-bg_frame_width must be a positive number')
        # validate visuals-fg_*
        if not 'fg_height' in list(conf['visuals'].keys()):
            conf['visuals']['fg_height'] = 0.5
            warnings.warn(filename + ': no visuals-fg_height, set to 0.5')
        elif not __is_numeric_pos__(conf['visuals']['fg_height']):
            raise InvalidConfigurationException(filename,
                'visuals-fg_height must be a positive number')
        if not 'fg_width' in list(conf['visuals'].keys()):
            conf['visuals']['fg_width'] = 1.25
            warnings.warn(filename + ': no visuals-fg_width, set to 1.25')
        elif not __is_numeric_pos__(conf['visuals']['fg_width']):
            raise InvalidConfigurationException(filename,
                'visuals-fg_width must be a positive number')
        if not 'fg_col' in list(conf['visuals'].keys()):
            conf['visuals']['fg_col'] = darkgrey
            warnings.warn(filename + ': no visuals-fg_col, set to dark grey')
        colorValidator.validateColor(cs, conf['visuals']['fg_col'])
        if not 'fg_frame_col' in list(conf['visuals'].keys()):
            conf['visuals']['fg_frame_col'] = darkgrey
            warnings.warn(filename + ': no visuals-fg_frame_col, ' +
            'set to dark grey')
        colorValidator.validateColor(cs, conf['visuals']['fg_frame_col'])
        if not 'fg_frame_width' in list(conf['visuals'].keys()):
            conf['visuals']['fg_frame_width'] = 2
            warnings.warn(filename + ': no visuals-fg_frame_width, set to 2pt')
        elif not __is_numeric_pos__(conf['visuals']['fg_frame_width']):
            raise InvalidConfigurationException(filename,
                'visuals-fg_frame_width must be a positive number')
        if not 'fg_opacity' in list(conf['visuals'].keys()):
            conf['visuals']['fg_opacity'] = 1
            warnings.warn(filename + ': no visuals-fg_opacity, set to 1')
        elif not __is_01interval__(conf['visuals']['fg_opacity']):
            raise InvalidConfigurationException(filename,
                'visuals-fg_opacity must be a number from [0 ... 1]')
        # validate visuals-hist_*
        if not 'hist_samples' in list(conf['visuals'].keys()):
            conf['visuals']['hist_samples'] = 100
            warnings.warn(filename + ': no visuals-hist_samples, set to 100')
        elif not __is_numeric_pos__(conf['visuals']['hist_samples']):
            raise InvalidConfigurationException(filename,
                'visuals-hist_samples must be a positive number')
        if not 'hist_width' in list(conf['visuals'].keys()):
            conf['visuals']['hist_width'] = 3
            warnings.warn(filename + ': no visuals-hist_width, set to 3')
        elif not __is_numeric_pos__(conf['visuals']['hist_width']):
            raise InvalidConfigurationException(filename,
                'visuals-hist_width must be a positive number')
        if not 'hist_line_width' in list(conf['visuals'].keys()):
            conf['visuals']['hist_line_width'] = 2
            warnings.warn(filename + ': no visuals-hist_line_width, set to 2pt')
        elif not __is_numeric_pos__(conf['visuals']['hist_line_width']):
            raise InvalidConfigurationException(filename,
                'visuals-hist_line_width must be a positive number')
        if not 'hist_fade' in list(conf['visuals'].keys()):
            conf['visuals']['hist_fade'] = False
            warnings.warn(filename + ': no visuals-hist_fade, set to False')
        elif not isinstance(conf['visuals']['hist_fade'], bool):
            raise InvalidConfigurationException(filename,
                'visuals-hist_fade must be a boolean')
        if not 'hist_col' in list(conf['visuals'].keys()):
            conf['visuals']['hist_col'] = white
            warnings.warn(filename + ': no visuals-hist_col, set to white')
        colorValidator.validateColor(cs, conf['visuals']['hist_col'])
        if not 'hist_side' in list(conf['visuals'].keys()):
            conf['visuals']['hist_side'] = 'both'
            warnings.warn(filename + ': no visuals-hist_side, set to both')
        elif not conf['visuals']['hist_side'] in ['left', 'right', 'both']:
            raise InvalidConfigurationException(filename,
                'visuals-hist_side must be one of [left right both]')
        # validate visuals-scales_*
        if not 'scales_thickness' in list(conf['visuals'].keys()):
            conf['visuals']['scales_thickness'] = 4
            warnings.warn(filename + ':no visuals-scales_thickness, set to 4pt')
        elif not __is_numeric_pos__(conf['visuals']['scales_thickness']):
            raise InvalidConfigurationException(filename,
                'visuals-scales_thickness must be a positive number')
        if not 'scales_widthl' in list(conf['visuals'].keys()):
            conf['visuals']['scales_widthl'] = 0.25
            warnings.warn(filename + ':no visuals-scales_widthl, set to 0.25pt')
        elif not __is_numeric_pos__(conf['visuals']['scales_widthl']):
            raise InvalidConfigurationException(filename,
                'visuals-scales_widthl must be a positive number')
        if not 'scales_widthr' in list(conf['visuals'].keys()):
            conf['visuals']['scales_widthr'] = 0.25
            warnings.warn(filename + ':no visuals-scales_widthr, set to 0.25pt')
        elif not __is_numeric_pos__(conf['visuals']['scales_widthr']):
            raise InvalidConfigurationException(filename,
                'visuals-scales_widthr must be a positive number')
        if not 'scales_col' in list(conf['visuals'].keys()):
            conf['visuals']['scales_col'] = white
            warnings.warn(filename + ': no visuals-scales_col, set to white')
        colorValidator.validateColor(cs, conf['visuals']['scales_col'])
        if not 'scales_text_col' in list(conf['visuals'].keys()):
            conf['visuals']['scales_text_col'] = white
            warnings.warn(filename + ':no visuals-scales_text_col set to white')
        colorValidator.validateColor(cs, conf['visuals']['scales_text_col'])
        # validate visuals-scales_text_* lists
        if not 'scales_text' in list(conf['visuals'].keys()):
            conf['visuals']['scales_text'] = []
            conf['visuals']['scales_text_pos'] = []
            conf['visuals']['scales_text_size'] = []
            warnings.warn(filename + ': no visuals-scales_text,' +
                'set empty scale data')
        if not isinstance(conf['visuals']['scales_text'], (list, tuple)):
            raise InvalidConfigurationException(filename,
                'visuals-scales_text must be a list of strings' +
                '(use empty strings for no label)')
        l = len(conf['visuals']['scales_text'])
        if not all([isinstance(conf['visuals']['scales_text'][i], str)
            for i in range(l)]):
                raise InvalidConfigurationException(filename,
                    'visuals-scales_text must be a list of strings' +
                    '(use empty strings for no label)')
        if not 'scales_text_pos' in list(conf['visuals'].keys()):
            conf['visuals']['scales_text_pos'] = ['c'] * l
            warnings.warn(filename + ': no visuals-scales_text_pos,' +
                ' all labels will be displayed centered (c)')
        if not isinstance(conf['visuals']['scales_text_pos'], (list, tuple)):
            conf['visuals']['scales_text_pos'] = [
                conf['visuals']['scales_text_pos']]
        if len(conf['visuals']['scales_text_pos']) == 1:
            conf['visuals']['scales_text_pos'] = (l *
                [conf['visuals']['scales_text_pos']])
        if len(conf['visuals']['scales_text_pos']) != l:
            raise InvalidConfigurationException(filename,
                'visuals-scales_text_pos length does not match scales_text')
        elif not all([entry in ['a', 'b', 'c', 'l', 'r']
            for entry in conf['visuals']['scales_text_pos']]):
            raise InvalidConfigurationException(filename,
                'visuals-scales_text_pos must be a list containing items ' +
                ' from [a, b, c, l, r]')
        if not 'scales_text_size' in list(conf['visuals'].keys()):
            conf['visuals']['scales_text_size'] = [10] * l
            warnings.warn(filename + ': no visuals-scales_text_size,' +
                ' all labels got size 10')
        if not isinstance(conf['visuals']['scales_text_size'], (list, tuple)):
            conf['visuals']['scales_text_size'] = [
                conf['visuals']['scales_text_size']]
        if len(conf['visuals']['scales_text_size']) == 1:
            conf['visuals']['scales_text_size'] = (l *
                [conf['visuals']['scales_text_pos']])
        if len(conf['visuals']['scales_text_size']) != l:
            raise InvalidConfigurationException(filename,
                'visuals-scales_text_size length does not match scales_text')
        elif not all([__is_numeric_pos__(entry)
            for entry in conf['visuals']['scales_text_size']]):
            raise InvalidConfigurationException(filename,
                'visuals-scales_text_size must be a list of positive numbers')
        # validate visuals-a* (annotations)
        if not 'aname' in list(conf['visuals'].keys()):
            conf['visuals']['aname'] = []
            conf['visuals']['atext'] = []
            conf['visuals']['apos'] = []
            conf['visuals']['asize'] = []
            conf['visuals']['acol'] = []
            warnings.warn(filename + ': visuals-aname missing, no annotations')
        if not isinstance(conf['visuals']['aname'], (list, tuple)):
            raise InvalidConfigurationException(filename,
                'visuals-aname must be a list of strings')
        l = len(conf['visuals']['aname'])
        if len(set(conf['visuals']['aname'])) != l:
            raise InvalidConfigurationException(filename,
                'visuals-aname must unique names')
        if not all([isinstance(entry, str)
            for entry in conf['visuals']['aname']]):
                raise InvalidConfigurationException(filename,
                    'visuals-aname must be a list of strings')
        if not 'atext' in list(conf['visuals'].keys()):
            conf['visuals']['aname'] = []
            conf['visuals']['atext'] = []
            conf['visuals']['apos'] = []
            conf['visuals']['asize'] = []
            conf['visuals']['acol'] = []
            warnings.warn(filename + ': visuals-atext missing, no annotations')
        if not isinstance(conf['visuals']['atext'], (list, tuple)):
            raise InvalidConfigurationException(filename,
                'visuals-atext must be a list of strings')
        if len(conf['visuals']['atext']) != l:
            raise InvalidConfigurationException(filename,
                'visuals-atext length mismatch with aname')
        if not all([isinstance(entry, str)
            for entry in conf['visuals']['atext']]):
                raise InvalidConfigurationException(filename,
                    'visuals-atext must be a list of strings')
        if not 'apos' in list(conf['visuals'].keys()):
            conf['visuals']['aname'] = []
            conf['visuals']['atext'] = []
            conf['visuals']['apos'] = []
            conf['visuals']['asize'] = []
            conf['visuals']['acol'] = []
            warnings.warn(filename + ': visuals-apos missing, no annotations')
        if not isinstance(conf['visuals']['apos'], (list, tuple)):
            raise InvalidConfigurationException(filename,
                'visuals-apos must be a list of x,y pairs')
        if len(conf['visuals']['apos']) != l:
            raise InvalidConfigurationException(filename,
                'visuals-apos length mismatch with aname')
        for entry in conf['visuals']['apos']:
            PositionValidator().validate(entry)
        if not 'asize' in list(conf['visuals'].keys()):
            conf['visuals']['asize'] = [10] * l
            warnings.warn(filename + ': visuals-asize missing,' +
                ' all texts will be rendered at size 10')
        if not isinstance(conf['visuals']['asize'], (list, tuple)):
            conf['visuals']['asize'] = [conf['visuals']['asize']] * l
        if len(conf['visuals']['asize']) != l:
            raise InvalidConfigurationException(filename,
                'visuals-asize length mismatch with aname')
        if not all([__is_numeric_pos__(entry)
            for entry in conf['visuals']['asize']]):
                raise InvalidConfigurationException(filename,
                    'visuals-asize must be a list of positive numbers')
        if not 'acol' in list(conf['visuals'].keys()):
            conf['visuals']['acol'] = (l *
                [white])
            warnings.warn(filename + ': visuals-acol missing,' +
                ' all texts will be rendered in white')
        if not isinstance(conf['visuals']['acol'], (list, tuple)):
            raise InvalidConfigurationException(filename,
                'visuals-acol must be a list of color tupels')
        if len(conf['visuals']['acol']) == 1:
            if isinstance(conf['visuals']['acol'][0], (list, tuple)):
                conf['visuals']['acol'] = [conf['visuals']['acol'][0]] * l
        if len(conf['visuals']['acol']) != l:
            raise InvalidConfigurationException(filename,
                'visuals-acol length mismatch with aname')
        for entry in conf['visuals']['acol']:
            colorValidator.validateColor(cs, entry)

    def ReadDefaults(self):
        # setup
        self.defFile = self.expFolder + os.sep + 'defaults.ini'
        if not os.path.isfile(self.defFile):
            self.defFile = self.baseDir + os.sep + 'defaults.ini'
            warnings.warn('Experiment did not contain a defaults file ' +
            '(defaults.ini). The default defaults file will be used (' +
            self.defFile + ')')
        # read
        cp = configparser.RawConfigParser()
        cp.read(self.defFile)
        for se in cp.sections():
            self.configDef[se] = {}
            for it in cp.options(se):
                self.configDef[se][it] = eval(cp.get(se, it))
        # validate
        self.__ValidateRunConf__(self.configDef, self.defFile)

    def ReadRuns(self):
        # read
        for run in self.configExp['runs']:
            self.configRuns.append({})
            for se in self.configDef.keys():
                self.configRuns[-1][se] = {}
                self.configRuns[-1][se].update(self.configDef[se])
            if len(eval(run[1])) > 0:
                cp = configparser.RawConfigParser()
                cp.read(self.expFolder + os.sep + eval(run[1]))
                for se in cp.sections():
                    for it in cp.options(se):
                        self.configRuns[-1][se][it] = eval(cp.get(se, it))
            # validate
            self.__ValidateRunConf__(self.configRuns[-1], eval(run[1]))

    def __getitem__(self, key):
        key = key.lower()
        if key in ['exp', 'experiment']:
            return self.configExp
        elif key in ['mon', 'monitor']:
            return self.configMon
        elif key in ['inp', 'input']:
            return self.configInp
        elif key in ['def', 'default', 'defaults']:
            return self.configDef
        elif key in ['run', 'runs']:
            return self.configRuns
        elif key in ['pulse']:
            return self.configPul
        elif key in ['runtime']:
            return self.runtimeInfos
        else:
            return []


##### HELPER FUNCTIONS #####
def __is_numeric_pos__(n):
    test = isinstance(n, (int, float))
    if not test:
        return test
    test = test and n > 0
    return test


def __is_01interval__(n):
    test = isinstance(n, (int, float))
    if not test:
        return test
    test = test and n >= 0 and n <= 1
    return test
