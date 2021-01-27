import copy
import time

from psychopy import core, logging, event
from psychopy.iohub import launchHubServer
import visuals
import DataHandler
import sound

import devices
import threading


class UrgeRecordPulseSender(DataHandler.UrgeRecordEventListener):
    def __init__(self, pulseOutput):
        assert isinstance(pulseOutput, devices.PulseOutput.PulseOutput)
        self.__pulseOutput = pulseOutput

    def onEvent(self, urgeValue):
        self.__pulseOutput.setDataValue(int(urgeValue * 255.0))
        self.__pulseOutput.sendPulse()


def applyFiringPattern(pulseOutput, configPulse, DH):
    if ('firing_pattern' in configPulse['pulse'] and 
        configPulse['pulse']['firing_pattern'] ==
            devices.PulseOutput.PulseFiringPattern.ON_URGE_RECORD):
        DH.registerUrgeRecordListener(UrgeRecordPulseSender(pulseOutput))


class SyncMarkers:
    def __init__(self, cfg_pulse, DH):
        # defaults: no markers (possibly overwritten below)
        self.send_out_pulse = False
        self.sound_begin = None
        self.sound_end = None
        self.send_lsl_markers = False

        # initialize pulse output
        self.cfg = cfg_pulse
        if cfg_pulse['pulse']['send_out_pulse']:
            self.send_out_pulse = True
            self.pulse_out = devices.PulseOutput.createPulseOutput(cfg_pulse)
            self.pulse_out.initDevice()
            self.pulse_value = cfg_pulse['out_pulse']['data']
            applyFiringPattern(self.pulse_out, cfg_pulse, DH)

        # initialized sound objects
        if cfg_pulse['pulse']['play_sound_begin']:
            self.sound_begin = sound.AudioPeep(cfg_pulse['sound_begin'])
            logging.info('Audio Object (begin) created')

        if cfg_pulse['pulse']['play_sound_end']:
            self.sound_end = sound.AudioPeep(cfg_pulse['sound_end'])
            logging.info('Audio Object (end) created')

        # initialize LabStreamingLayer
        if cfg_pulse['pulse']['send_lsl_markers']:
            self.send_lsl_markers = True
            self.lsl_marker_begin = cfg_pulse['lsl']['marker_begin']
            self.lsl_marker_end = cfg_pulse['lsl']['marker_end']
        
    def send_begin_markers(self):
        logging.info('sending begin markers')
        if self.send_out_pulse:
            self.pulse_out.setDataValue(self.pulse_value)
            self.pulse_out.sendPulse()
        if self.sound_begin:
            self.sound_begin.play()
        if self.send_lsl_markers:
            devices.LSL.send_marker(self.lsl_marker_begin)

    def send_end_markers(self):
        logging.info('sending end markers')
        if self.send_out_pulse:
            self.pulse_out.setDataValue(self.pulse_value)
            self.pulse_out.sendPulse()
        if self.sound_end:
            self.sound_end.play()
        if self.send_lsl_markers:
            devices.LSL.send_marker(self.lsl_marker_end)


class UrgeMonitor:
    def __init__(self, C):
        self.cfg = copy.deepcopy(C)
        self.CurrRun = C['runtime']['curr_run']
        self.DH = DataHandler.DataHandler(C['exp']['info'],
                                          C['exp']['runs'][self.CurrRun][0],
                                          C['exp']['main'],
                                          C['runs'][self.CurrRun])
        self.graphics = None

        try:
            self.init_devices()
            self._ready = True
        except Exception as e:
            self._ready = False
            self.handle_exception(e)

    def init_devices(self):
        C = self.cfg

        # generate visual elements
        self.graphics = visuals.Visuals.Visuals(C['monitor']['monitor'],
                                                C['monitor']['window'],
                                                C['runs'][self.CurrRun]['visuals'])

        logging.info(msg='graphical objects generated')

        # initialize sync markers
        self.sync = SyncMarkers(C['pulse'], self.DH)

        # initialize clocks
        self.init_clocks()

        # init input devices
        logging.info('Initializing devices')
        self.init_input_listener()
        self.PL = devices.PulseListener.PulseListener(C['pulse'], self.IL)
        logging.info('PulseListener created')

        self._ready = True

    def init_input_listener(self):
        self.IL = devices.InputListener.InputListener(self.cfg['input'],
                                                      self.graphics.getWindow())
        logging.info('Input listener created')
        self.KeyAbort = self.cfg['exp']['main']['abort_key']
        self.IL.RegisterKey(self.KeyAbort)
        keyPos = {}
        for c, key in enumerate(self.cfg['exp']['main']['log_buttons']):
            self.IL.RegisterKey(key)
            keyPos[key] = c
        self.IL.GetBufferedKeys()
        logging.info('Initialized keyboard')
        logging.info('Reset urge value')

    def init_clocks(self):
        control = self.cfg['runs'][self.CurrRun]['control']
        self.frameclock_increment = 1.0 / control['frame_rate']
        self.frameclock = core.Clock()
        self.plotclock_increment = 1.0 / control['hist_rate']
        self.plotclock = core.Clock()
        self.sampleclock_increment = 1.0 / control['urge_sample_rate']
        self.sampleclock = core.Clock()
        self.t_run = float(control['run_time'])
        self.rtclock = core.Clock()
        self.idle_time = min(self.plotclock_increment,
                             self.sampleclock_increment,
                             self.frameclock_increment)/2

    def reset_clocks(self):
        self.frameclock.reset()
        self.plotclock.reset()
        self.sampleclock.reset()
        self.rtclock.reset()

    @property
    def ready(self):
        return self._ready

    def run(self):
        if self.ready:
            try:
                self.reset_clocks()
                self.recording_complete = threading.Event()
                self.aborted = threading.Event()
                self.urge_value = 0.5
                self.DH.setState(state=DataHandler.STATE.RUNNING)
                self.graphics.flip()  # this seems to be relevant for resetting the rel mouse pos...
                self.start_data_thread()
                self.plot_loop()
                self.data_thread.join()
                self.finish()
            except Exception as e:
                self.handle_exception(e)


    def start_data_thread(self):
        self.data_thread = threading.Thread(target=self.data_loop_wrapper)
        self.data_thread.start()

    def data_loop_wrapper(self):
        try:
            self.data_loop()
        except Exception as e:
            #self.handle_exception(e)
            logging.error('error in data loop: '+str(e))
            self.recording_complete.set()
            #self.sync.send_end_markers()

    def data_loop(self):
        logging.info('Starting data loop')
        self.recording = False
        self.IL.ResetUrge()
        self.urge_value = 0.5
        t = 0.0
       
        while not (self.PL.Pulse() or self.aborted.isSet()):
            self.IL.ReadUrge()  # update urge value
            self.urge_value = self.IL.GetUrge()
            self.check_kb_quit()
            self.dummy_wait()

        if not self.aborted.isSet(): 
            logging.info('Starting recording')
            self.recording = True
            self.sync.send_begin_markers()
            self.sampleclock.reset()
            self.rtclock.reset()

        while (not self.aborted.isSet()) and (t < self.t_run):
            self.IL.ReadUrge()  # update urge value
            self.urge_value = self.IL.GetUrge()
            t = self.rtclock.getTime()
            
            st = self.sampleclock.getTime()
            if st >= 0.0:  # recording freq
                buf_keys = self.IL.GetBufferedKeys()
                self.DH.recordUrge(self.urge_value, t, st, buf_keys[1:])
                self.sampleclock.add(self.sampleclock_increment)
            self.check_kb_quit()
            self.dummy_wait()

        #else:
        #    if self.DH.getState() == DataHandler.STATE.RUNNING:
        #        self.DH.setState(state=DataHandler.STATE.FINISHED)
        
        logging.info('leaving data loop')
        self.sync.send_end_markers()
        self.recording_complete.set()
                
    def plot_loop(self):
        logging.info('starting plot loop')
        while not (self.recording_complete.isSet() or self.aborted.isSet()):
            if self.plotclock.getTime() >= 0.0:  # update plot
                self.graphics.updateHistoriePlot(self.urge_value)
                self.plotclock.add(self.plotclock_increment)

            if self.frameclock.getTime() >= 0.0:  # flip screen
                self.frameclock.add(self.frameclock_increment)
                self.graphics.updateUrgeIndicator(self.urge_value)
                self.graphics.flip()

            self.check_kb_quit()
            self.dummy_wait()

            #if not self.data_thread.isAlive():
            #    break
        logging.info('ending plot loop')

    def check_kb_quit(self):
        if self.KeyAbort in self.IL.GetPressedKeys():
            self.DH.setState(state=DataHandler.STATE.ABORT_USER,
                             error_code=DataHandler.ERROR_CODE.SUCCESS)
            logging.info('ABORTED (q)')
            self.aborted.set()
        
    def dummy_wait(self):
        time.sleep(self.idle_time)

    def handle_exception(self, e):
        logging.error(e.__str__())
        self.DH.setState(state=DataHandler.STATE.ERROR,
                         error_code=DataHandler.ERROR_CODE.ERROR_OTHER)
        self.DH.passError(e)
        self.DH.endRecording()
        if (self.graphics is not None):
            del self.graphics
        raise e

    def finish(self):    
        if self.DH.getState() == DataHandler.STATE.RUNNING:
            self.DH.setState(state=DataHandler.STATE.FINISHED)
        self.DH.endRecording()
        del self.graphics
        self.graphics = None


def MainLoop(C):
    UM = UrgeMonitor(C)
    UM.run()

