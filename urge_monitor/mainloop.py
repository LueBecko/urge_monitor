# -*- coding: utf-8 -*-

from psychopy import core, logging
from psychopy.iohub import launchHubServer
import visuals
import DataHandler
import InputDevice
import InputListener
import sound

## stuff for pulse recording
from psychopy import parallel
import serial

class PulseListener:
    '''simple class for parallel port pulse reading, support simulation'''

    def __init__(self, C, IL):
        self.__InputListener__ = IL
        self.__sim__ = C['pulse']['simulation']
        if self.__sim__:
            self.__clock__ = core.Clock()
            self.__clock__.add(2.5)  # 2.5 s time before simulated pulse
        else:
            self.__interface__ = C['pulse']['interface'].lower()
            if self.__interface__ == 'parallel':
                self.__pin__ = C[self.__interface__]['pin']
                self.__address__ = C[self.__interface__]['address']
                self.__port__ = parallel.ParallelPort(address=self.__address__)
                self.__base__ = self.__port__.readPin(self.__pin__)
            elif self.__interface__ == 'serial':
                self.__portname__ = C[self.__interface__]['port']
                self.__baudrate__ = C[self.__interface__]['baudrate']
                self.__bytesize__ = C[self.__interface__]['bytesize']
                self.__parity__ = C[self.__interface__]['parity']
                self.__stopbits__ = C[self.__interface__]['stopbits']
                self.__timeout__ = C[self.__interface__]['timeout']
                self.__xonxoff__ = C[self.__interface__]['xonxoff']
                self.__rtscts__ = C[self.__interface__]['rtscts']
                self.__dsrdtr__ = C[self.__interface__]['dsrdtr']
                self.__inter_byte_timeout__ = (
                    C[self.__interface__]['inter_byte_timeout'])
                self.__port__ = None
                self.__port__ = serial.Serial(port=self.__portname__,
                    baudrate=self.__baudrate__,
                    bytesize=self.__bytesize__,
                    parity=self.__parity__,
                    stopbits=self.__stopbits__,
                    timeout=self.__timeout__,
                    xonxoff=self.__xonxoff__,
                    rtscts=self.__rtscts__,
                    dsrdtr=self.__dsrdtr__)
            elif self.__interface__ == 'keyboard':
                self.__key__ = C[self.__interface__]['key']
                self.__InputListener__.RegisterKey(self.__key__)

    def Pulse(self):
        if self.__sim__:
            return self.__clock__.getTime() >= 0.0
        elif self.__interface__ == 'parallel':
            return self.__port__.readPin(self.__pin__) != self.__base__
        elif self.__interface__ == 'serial':
            return len(self.__port__.read(1)) != 0
        elif self.__interface__ == 'keyboard':
            #print self.__InputListener__.GetPressedKeys()
            return self.__key__ in self.__InputListener__.GetPressedKeys()

    def __del__(self):
        if self.__sim__:
            pass
        else:
            if self.__interface__ == 'parallel':
                pass
            elif self.__interface__ == 'serial':
                if not self.__port__ is None:
                    self.__port__.close()
            elif self.__interface__ == 'keyboard':
                self.__InputListener__.UnregisterKey(self.__key__)


class OutPulse:
    '''simple class to send pulse at start'''

    def __init__(self, C):
        self.__sim__ = C['pulse']['simulation']
        self.__address__ = C['out_pulse']['address']
        self.__data__ = C['out_pulse']['data']
        self.__duration__ = C['out_pulse']['duration']
#        if self.__sim__:
#            self.__port__ = None
#        else:
#            self.__port__ = parallel.ParallelPort(address=self.__address__)
#            self.__port__.setData(0)
        self.__port__ = parallel.ParallelPort(address=self.__address__)
        self.__port__.setData(0)

    def SendPulse(self):
#        if not self.__sim__:
#            self.__port__.setData(self.__data__)
#            core.wait(secs=self.__duration__, hogCPUperiod=self.__duration__)
#            self.__port__.setData(0)
        self.__port__.setData(self.__data__)
        core.wait(secs=self.__duration__, hogCPUperiod=self.__duration__)
        self.__port__.setData(0)

    def __del__(self):
        if not self.__sim__:
            pass


def MainLoop(C):
    CurrRun = C['runtime']['curr_run']
    DH = DataHandler.DataHandler(C['exp']['info'],
        C['exp']['runs'][CurrRun][0],
        C['exp']['main'], C['runs'][CurrRun])

    try:
        # generate visual elements
        visuals.CreateVisuals(Cmon=C['monitor']['monitor'],
            Cwin=C['monitor']['window'], Cvis=C['runs'][CurrRun]['visuals'])
        logging.info(msg='graphical objects generated')

        # generate input object
        IL = InputListener.InputListener(C['input'])
        KeyAbort = C['exp']['main']['abort_key']
        IL.RegisterKey(KeyAbort)
        c = 0
        keyPos = {}
        for key in C['exp']['main']['log_buttons']:
            IL.RegisterKey(key)
            keyPos[key] = c
            c += 1
        IL.GetBufferedKeys()

        # generate pulse object
        PL = PulseListener(C['pulse'], IL)
        logging.info('PulseListener created')
        sendOutPulse = C['pulse']['pulse']['send_out_pulse']
        if sendOutPulse:
            OP = OutPulse(C['pulse'])

        # create sound objects
        playPulseSoundbegin = C['pulse']['pulse']['play_sound_begin']
        if playPulseSoundbegin:
            APb = sound.AudioPeep(C['pulse']['sound_begin'])
            logging.info('Audio Object (begin) created')

        playPulseSoundend = C['pulse']['pulse']['play_sound_end']
        if playPulseSoundend:
            APe = sound.AudioPeep(C['pulse']['sound_end'])
            logging.info('Audio Object (end) created')

        urgevalue = 0.5
        visuals.flip()

        DH.setState(state=DataHandler.STATE.RUNNING)

        # generate timers
        frameclock_increment = 1.0 / C['runs'][CurrRun]['control']['frame_rate']
        frameclock = core.Clock()
        plotclock_increment = 1.0 / C['runs'][CurrRun]['control']['hist_rate']
        plotclock = core.Clock()
        sampleclock_increment = (1.0 /
            C['runs'][CurrRun]['control']['urge_sample_rate'])
        sampleclock = core.Clock()
        #  print(C['runs'][CurrRun]['control']['urge_sample_rate'])
        #  print(sampleclock_increment)
        t_run = float(C['runs'][CurrRun]['control']['run_time'])

###############################################################
        ## Loop to wait for first pulse
        print('enter pre loop')
        abortRun = False
        while True:
            IL.ReadUrge()

            if plotclock.getTime() >= 0.0:  # update plot
                urgevalue = IL.GetUrge()
                visuals.hist.updateHist(urgevalue)
                plotclock.add(plotclock_increment)

            if frameclock.getTime() >= 0.0:  # draw frame
                visuals.flip()  # flip first to ensure best frame timing
                frameclock.add(frameclock_increment)
                visuals.bars.UpdateFGBar(urgevalue)  # minimal draw lag

            # abort by experimenter
            if KeyAbort in IL.GetPressedKeys():
                DH.setState(state=DataHandler.STATE.ABORT_USER,
                    error_code=DataHandler.ERROR_CODE.SUCCESS)
                abortRun = True
                break

            if PL.Pulse():
                logging.info('Pulse received')
                print('got pulse')
                if playPulseSoundbegin:
                    APb.play()
                break

        print('leaving pre loop')
########################################################
        if not abortRun:
            if sendOutPulse:
                logging.info('sending eeg pulse')
                print('send eeg synchronisation pulse')
                OP.SendPulse()

            t = 0.0
            #frameclock.reset()
            #plotclock.reset()
            sampleclock.reset()
            rtclock = core.Clock()
            ## Loop in which experiment is performed
            while t < t_run:
                IL.ReadUrge()

                st = sampleclock.getTime()
                if st >= 0.0:  # recording freq
                    urgevalue = IL.GetUrge()
                    DH.recordUrge(urgevalue, t, st,
                        IL.GetBufferedKeys()[1:])
                    sampleclock.add(sampleclock_increment)

                if plotclock.getTime() >= 0.0:  # update plot
                    visuals.hist.updateHist(urgevalue)
                    plotclock.add(plotclock_increment)

                if frameclock.getTime() >= 0.0:  # draw frame
                    visuals.flip()  # flip first to ensure best frame timing
                    frameclock.add(frameclock_increment)
                    visuals.bars.UpdateFGBar(urgevalue)  # minimal draw lag

                # abort by experimenter
                if KeyAbort in IL.GetPressedKeys():
                    DH.setState(state=DataHandler.STATE.ABORT_USER,
                        error_code=DataHandler.ERROR_CODE.SUCCESS)
                    break

                t = rtclock.getTime()
        print('leaving main loop')
        if playPulseSoundend:
            APe.play()
############################################################
    except Exception as e:
        print('Error occured')
        print((type(e)))
        print((e))
        logging.error(e.__str__())
        DH.setState(state=DataHandler.STATE.ERROR,
            error_code=DataHandler.ERROR_CODE.ERROR_OTHER)
        DH.passError(e)
        DH.endRecording()
        visuals.CloseVisuals()
        raise e
    else:
        if DH.getState() == DataHandler.STATE.RUNNING:
            DH.setState(state=DataHandler.STATE.FINISHED)
        DH.endRecording()
        visuals.CloseVisuals()