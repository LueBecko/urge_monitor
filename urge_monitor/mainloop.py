from psychopy import core, logging
from . import visuals
from .data import DataHandler, UrgeEventPulseSender
from . import sound
from . import devices

def MainLoop(C, baseDirectory):
    CurrRun = C['runtime']['curr_run']
    DH = DataHandler.createDataHandler(C, baseDirectory, CurrRun)

    graphics = None
    try:
        # generate visual elements
        graphics = visuals.Visuals.Visuals(C['monitor']['monitor'],
            C['monitor']['window'], C['runs'][CurrRun]['visuals'])
        logging.info(msg='graphical objects generated')

        # generate input object
        IL = devices.InputListener.InputListener(C['input'], graphics.getWindow())
        KeyAbort = C['exp']['main']['abort_key']
        IL.RegisterKey(KeyAbort)
        c = 0
        keyPos = {}
        for key in C['exp']['main']['log_buttons']:
            IL.RegisterKey(key)
            keyPos[key] = c
            c += 1
        IL.GetBufferedKeys()

        pulseListener = devices.PulseListener.createPulseListener(C['pulse'], IL)
        pulseListener.initDevice()
        logging.info('PulseListener created')
        pulseOut = devices.PulseOutput.createPulseOutput(C['pulse'])
        pulseOut.initDevice()
        logging.info('PulseOutput created')

        UrgeEventPulseSender.applyFiringPattern(pulseOut, C['pulse'], DH)

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
        graphics.flip()

        DH.setState(state=DataHandler.STATE.RUNNING)

        # generate timers
        frameclock_increment = 1.0 / C['runs'][CurrRun]['control']['frame_rate']
        frameclock = core.Clock()
        plotclock_increment = 1.0 / C['runs'][CurrRun]['control']['hist_rate']
        plotclock = core.Clock()
        sampleclock_increment = (1.0 /
            C['runs'][CurrRun]['control']['urge_sample_rate'])
        sampleclock = core.Clock()
        t_run = float(C['runs'][CurrRun]['control']['run_time'])

###############################################################
        ## Loop to wait for first pulse
        print('enter pre loop')
        abortRun = False
        while True:
            IL.ReadUrge()

            if plotclock.getTime() >= 0.0:  # update plot
                urgevalue = IL.GetUrge()
                graphics.updateHistoriePlot(urgevalue)
                plotclock.add(plotclock_increment)

            if frameclock.getTime() >= 0.0:  # draw frame
                graphics.flip()  # flip first to ensure best frame timing
                frameclock.add(frameclock_increment)
                graphics.updateUrgeIndicator(urgevalue) # minimal draw lag

            # abort by experimenter
            if KeyAbort in IL.GetPressedKeys():
                DH.setState(state=DataHandler.STATE.ABORT_USER,
                    error_code=DataHandler.ERROR_CODE.SUCCESS)
                abortRun = True
                break

            if pulseListener.pulseReceived():
                pulseListener = None;
                logging.info('Pulse received')
                if playPulseSoundbegin:
                    APb.play()
                break

        print('leaving pre loop')
########################################################
        if not abortRun:
            pulseOut.sendPulse()

            t = 0.0
            sampleclock.reset()
            rtclock = core.Clock()
            ## Loop in which experiment is performed
            while t < t_run:
                IL.ReadUrge()

                st = sampleclock.getTime()
                if st >= 0.0:  # recording freq
                    urgevalue = IL.GetUrge()
                    DH.recordUrge(urgevalue, t, st, IL.GetBufferedKeys()[1:])
                    sampleclock.add(sampleclock_increment)

                if plotclock.getTime() >= 0.0:  # update plot
                    graphics.updateHistoriePlot(urgevalue)
                    plotclock.add(plotclock_increment)

                if frameclock.getTime() >= 0.0:  # draw frame
                    graphics.flip()  # flip first to ensure best frame timing
                    frameclock.add(frameclock_increment)
                    graphics.updateUrgeIndicator(urgevalue) # minimal draw lag

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
        if (graphics is not None):
            del graphics
        raise e
    else:
        if DH.getState() == DataHandler.STATE.RUNNING:
            DH.setState(state=DataHandler.STATE.FINISHED)
        DH.endRecording()
        del graphics
