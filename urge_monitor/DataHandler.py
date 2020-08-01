# class for data-recording and storing
#
# TODO:
#    csvWriter or DictWriter?
#    try on file access?

import os.path
import warnings
import errno
import math
import csv
import psychopy.info
from psychopy import data
import configparser


# Status Constants
class STATE:
    STARTED = 'Started'
    RUNNING = 'Running'
    FINISHED = 'Finished'
    ERROR = 'Aborted due to Error'
    ABORT_USER = 'Aborted by User'
    ABORT = 'Abort'  # yet undefined, captures all other abort reasons


class ERROR_CODE:
    NONE = 'None'  # still running
    SUCCESS = 'Success'
    ERROR_OTHER = 'Error'  # captures all errors not defined above


class DataHandler:

    def __init__(self, info, runName, expConfig, runConfig):
        '''Generates DataHandler for all Experiment-Data'''
        self.__expConfig = expConfig
        self.__runConfig = runConfig
        self.__identifier = info['subj']
        self.__runName = runName
        self.__info = info
        direc = (os.path.dirname(__file__) + os.sep +
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
        self.__csvFilename = (direc + self.__runName + '.csv')
        i = 0
        while (os.path.isfile(self.__infFilename) or
            os.path.isfile(self.__csvFilename)):
                i += 1
                self.__infFilename = (
                    direc + self.__runName + '_' + str(i) + '.info')
                self.__csvFilename = (
                    direc + self.__runName + '_' + str(i) + '.csv')
        if i > 0:
            warnings.warn('Found conflivting log files, wrote on files ' +
                self.__infFilename + ' and ' + self.__csvFilename)
        # states
        self.__currentState = None
        self.__currentErrorCode = None
        self.setState(state=STATE.STARTED, error_code=ERROR_CODE.NONE)
        # Set First Inf
        self.__infWriter = None
        self.__gatherInitialInf__()
        # initialise data struct (urge, time, lag)
        self.nButtons = len(self.__expConfig['log_buttons'])
        self.nSamples = int(math.floor(1 +
           self.__runConfig['control']['run_time'] *
              self.__runConfig['control']['urge_sample_rate']))
        self.__csvData = [[float('nan')] * (3 + self.nButtons)] * self.nSamples
        self.__currSample = 0

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
        self.__baseInfo['software'] = 'UrgeRating fMRI'
        self.__baseInfo['author'] = 'Christian Beck'
        self.__baseInfo['version'] = '1.0'
        self.__baseInfo['started'] = True
        self.__baseInfo['finished'] = False
        self.__baseInfo['start_time'] = data.getDateStr(
            format="%Y_%m_%d %H:%M (Year_Month_Day Hour:Min)")
        self.__baseInfo['end_time'] = 'Not reached'
        self.__baseInfo['status'] = self.__currentState
        self.__baseInfo['error_code'] = self.__currentErrorCode
        self.__baseInfo['data_file'] = self.__csvFilename
        self.__baseInfo['data_file_written'] = False

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

    def __writeData__(self):
        with (open(self.__csvFilename, 'w')) as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            writer.writerows(self.__csvData)  # test this write methode

    def setState(self, state=None, error_code=None):
        if state is not None:
            self.__currentState = state
        if error_code is not None:
            self.__currentErrorCode = error_code

    def getState(self):
        return self.__currentState

    def recordUrge(self, urgevalue, rec_time, lag, buttons=[]):
        self.__csvData[self.__currSample] = [urgevalue, rec_time, lag] + buttons
        self.__currSample = self.__currSample + 1

    def passError(self, excep):
        self.__baseInfo['exception'] = excep
        self.__baseInfo['exception_str'] = excep.__str__()

    def endRecording(self, state=None, error_code=None, msg=''):
        '''write everything down, record states and errors'''
        self.setState(state, error_code)
        # write raw data
        self.__writeData__()
        self.__baseInfo['data_file_written'] = True
        # report inf
        self.__baseInfo['status'] = self.__currentState
        self.__baseInfo['error_code'] = self.__currentErrorCode
        self.__baseInfo['end_message'] = msg
        self.__baseInfo['finished'] = True
        self.__baseInfo['end_time'] = data.getDateStr(
            format="%Y_%m_%d %H:%M (Year_Month_Day Hour:Min)")
        self.__baseInfo['data_file'] = self.__csvFilename
        self.__baseInfo['data_file_written'] = False

        self.__writeInfo__()
        if error_code not in [ERROR_CODE.NONE,
            ERROR_CODE.SUCCESS]:
            print(error_code)
        print(msg)
