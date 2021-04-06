import math
import csv
import os.path
import warnings

from .UrgeEventListener import UrgeEventListener

class CSVDataRecorder(UrgeEventListener):
    ''' record each event in an in memory data structure and write all data to csv when closing '''
    def __init__(self, experimentConfiguration, subjectName, runName, runConfiguration, baseDirectory):
        numberOfButtonsToLog = len(experimentConfiguration['log_buttons'])
        runTime = runConfiguration['control']['run_time']
        sampleRate = runConfiguration['control']['urge_sample_rate']
        nSamples = int(math.floor(1 + runTime * sampleRate))
        self.__csvData = [[float('nan')] * (3 + numberOfButtonsToLog)] * nSamples
        self.__currSample = 0
        self.__determineCSVFilename(experimentConfiguration, subjectName, runName, baseDirectory)

    def __determineCSVFilename(self, experimentConfiguration, subjectName, runName, baseDirectory):
        ## TODO: extract into separate class (e.g. filenameBuilder) and test it (mock os.path). Use this also for inf files
        logDirectory = (baseDirectory + os.sep +
             experimentConfiguration['log_folder'] + os.sep +
             experimentConfiguration['name'] + os.sep +
             subjectName + os.sep)
        self.__csvFilename = (logDirectory + runName + '.csv')
        i = 0
        while (os.path.isfile(self.__csvFilename)):
                i += 1
                self.__csvFilename = (
                    logDirectory + runName + '_' + str(i) + '.csv')
        if i > 0:
            warnings.warn('Found conflicting csv files, wrote on file ' + self.__csvFilename)


    def onEvent(self, urgeValue, recTime, lag, buttons):
        self.__csvData[self.__currSample] = [urgeValue, recTime, lag] + buttons
        self.__currSample = self.__currSample + 1

    def close(self):
        with (open(self.__csvFilename, 'w')) as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            writer.writerows(self.__csvData)

