import os.path
from urge_monitor.data.UrgeValueTransformator import UrgeValueTransformator
import warnings
import errno
import psychopy.info
from psychopy import data
import configparser
from enum import Enum
from .UrgeEventListener import UrgeEventListener
from .CSVDataRecorder import CSVDataRecorder
from .UrgeLogWriter import UrgeLogWriter

# Status Constants
class STATE(Enum):
    STARTED = 'Started'
    RUNNING = 'Running'
    FINISHED = 'Finished'
    ERROR = 'Aborted due to Error'
    ABORT_USER = 'Aborted by User'
    ABORT = 'Abort'  # yet undefined, captures all other abort reasons

class ERROR_CODE(Enum):
    NONE = 'None'  # still running
    SUCCESS = 'Success' # run to an end without errors
    ERROR_OTHER = 'Error'  # captures all errors not defined above

def createDataHandler(configuration, baseDirectory, currentRun):
    '''factory method that takes care of the common setup of the DataHandler'''
    DH = DataHandler(configuration['exp']['info'],
        configuration['exp']['runs'][currentRun][0],
        configuration['exp']['main'],
        configuration['runs'][currentRun],
        baseDirectory)
    DH.registerUrgeRecordListener(
        CSVDataRecorder(
            configuration['exp']['main'],
            configuration['exp']['info']['subj'],
            configuration['exp']['runs'][currentRun][0],
            configuration['runs'][currentRun],
            baseDirectory))
    DH.registerUrgeRecordListener(UrgeLogWriter())
    return DH

class DataHandler:

    def __init__(self, info, runName, expConfig, runConfig, baseDirectory):
        '''Generates DataHandler for all Experiment-Data'''
        self.__expConfig = expConfig
        self.__runConfig = runConfig
        self.__identifier = info['subj']
        self.__runName = runName
        self.__info = info
        direc = (baseDirectory + os.sep +
             self.__expConfig['log_folder'] + os.sep +
             self.__expConfig['name'] + os.sep +
             self.__identifier + os.sep)
        try:
            os.makedirs(direc)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise exception
        # Never touch an existing file
        self.__infFilename = (direc + self.__runName + '.info')
        i = 0
        while (os.path.isfile(self.__infFilename)):
                i += 1
                self.__infFilename = (
                    direc + self.__runName + '_' + str(i) + '.info')
        if i > 0:
            warnings.warn('Found conflicting log files, wrote on file ' + self.__infFilename)
        # states
        self.__currentState = None
        self.__currentErrorCode = None
        self.setState(state=STATE.STARTED, error_code=ERROR_CODE.NONE)
        # Set First Inf
        self.__infWriter = None
        self.__gatherInitialInf__()
        self.__urgeEventListeners = []
        # value transformator
        self.__transformator__ = self.__createTransformator__(runConfig)

    def __createTransformator__(self, runConfig):
        if not 'coded_urge_value_low' in runConfig['control'].keys():
            low = 1
        else:
            low = runConfig['control']['coded_urge_value_low']
        if not 'coded_urge_value_high' in runConfig['control'].keys():
            high = 1
        else:
            high = runConfig['control']['coded_urge_value_high']
        transformator = UrgeValueTransformator(low, high)
        return transformator

    def __gatherInitialInf__(self):
        # gather Infos
        SysInf = None
        # this is currenlty deactivated because it fails on german windows systems
        #psychopy.info.RunTimeInfo(
        #    win=False,
        #    refreshTest=True,
        #    userProcsDetailed=True,
        #    verbose=True)

        self.__baseInfo = {}
        self.__baseInfo['experiment'] = self.__expConfig['name']
        self.__baseInfo['identifier'] = self.__identifier
        self.__baseInfo['runName'] = self.__runName
        self.__baseInfo['software'] = 'Urge-Monitor'
        self.__baseInfo['author'] = 'Christian Beck'
        self.__baseInfo['version'] = '0.1'
        self.__baseInfo['started'] = True
        self.__baseInfo['finished'] = False
        self.__baseInfo['start_time'] = data.getDateStr(
            format="%Y_%m_%d %H:%M (Year_Month_Day Hour:Min)")
        self.__baseInfo['end_time'] = 'Not reached'
        self.__baseInfo['status'] = self.__currentState
        self.__baseInfo['error_code'] = self.__currentErrorCode

        self.__writeInfo__(SysInf=SysInf)

    def __writeInfo__(self, SysInf=None):
        if self.__infWriter is None:
            self.__infWriter = configparser.RawConfigParser()

        section_main = 'main'
        if not self.__infWriter.has_section(section_main):
            self.__infWriter.add_section(section_main)
        for key in list(self.__baseInfo.keys()):
            self.__infWriter.set(section_main, key, self.__baseInfo[key])

        section_exp = 'experiment_configuration'
        if not self.__infWriter.has_section(section_exp):
            self.__infWriter.add_section(section_exp)
        for key in list(self.__expConfig.keys()):
            self.__infWriter.set(section_exp, key, self.__expConfig[key])

        section_inf = 'info'
        if not self.__infWriter.has_section(section_inf):
            self.__infWriter.add_section(section_inf)
        for key in list(self.__info.keys()):
            self.__infWriter.set(section_inf, key, self.__info[key])

        section_run = 'run_configuration'
        if not self.__infWriter.has_section(section_run):
            self.__infWriter.add_section(section_run)
        for key in list(self.__runConfig.keys()):
            self.__infWriter.set(section_run, key, self.__runConfig[key])

        section_tech = 'technical_information'
        if not self.__infWriter.has_section(section_tech):
            self.__infWriter.add_section(section_tech)
        if SysInf is not None:
            for key in list(SysInf.keys()):
                self.__infWriter.set(section_tech, key, SysInf[key])

        with (open(self.__infFilename, 'w')) as infFile:
            self.__infWriter.write(infFile)

    def setState(self, state=None, error_code=None):
        if state is not None:
            self.__currentState = state
        if error_code is not None:
            self.__currentErrorCode = error_code

    def getState(self):
        return self.__currentState

    def registerUrgeRecordListener(self, listener):
        ''' adds a listener to be fired when an Urge gets recorded'''
        if isinstance(listener, UrgeEventListener):
            self.__urgeEventListeners.append(listener)

    def recordUrge(self, urgevalue, rec_time, lag, buttons=[]):
        ''' a urge event should be recorded - fires UrgeRecordListeners '''
        transformedUrgeValue = self.__transformator__.transform(urgevalue);
        for listener in self.__urgeEventListeners:
            listener.onEvent(transformedUrgeValue, rec_time, lag, buttons)

    def passError(self, excep):
        self.__baseInfo['exception'] = excep
        self.__baseInfo['exception_str'] = excep.__str__()

    def endRecording(self, state=None, error_code=None, msg=''):
        '''write everything down, record states and errors'''
        self.setState(state, error_code)
        # close all listeners
        for listener in self.__urgeEventListeners:
            listener.close()
        # report inf
        self.__baseInfo['status'] = self.__currentState
        self.__baseInfo['error_code'] = self.__currentErrorCode
        self.__baseInfo['end_message'] = msg
        self.__baseInfo['finished'] = True
        self.__baseInfo['end_time'] = data.getDateStr(
            format="%Y_%m_%d %H:%M (Year_Month_Day Hour:Min)")

        self.__writeInfo__()
        if error_code not in [ERROR_CODE.NONE,
            ERROR_CODE.SUCCESS]:
            print(error_code)
        print(msg)
