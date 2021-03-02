from psychopy import core, visual, event, logging
import sound
from devices import LSL

# some settings
quit_key = 'q'
start_trigger = 'start_recording'
end_trigger = 'end_recording'
sound_cfg = dict(value=880, duration=0.2, volume=1.0)
start_txt = "Mit Tastendruck geht es los."
end_txt = "Vielen Dank!"
pre_dur = 3
exp_dur = 300

# logging
logging.console.setLevel(logging.INFO)


class QuitException(Exception):
    pass


class DummyExp:
    def __init__(self):

        LSL.init('UrgeMonitor')
        self.win = visual.Window([1920, 1080], monitor="dummy", fullscr=True, color='black')
        self.win.mouseVisible = False
        self.sound_cue = sound.AudioPeep(sound_cfg)
        self.state = 'none'

    def start_cue(self):
        logging.info('start cue')
        LSL.send_marker(start_trigger)
        self.sound_cue.play()
        
    def end_cue(self):
        logging.info('end cue')
        LSL.send_marker(end_trigger)
        self.sound_cue.play()

    def show_msg_wait(self, txt):
        logging.info('show message')
        message = visual.TextStim(self.win, text=txt)
        message.draw()
        self.win.flip()
        event.waitKeys()
        self.win.flip()

    def wait_period(self, state):
        logging.info('waiting: ' + state)
        self.state = state
        dur = pre_dur if state == 'pre' else exp_dur
        if event.waitKeys(maxWait=dur, keyList=[quit_key]):
            raise QuitException()

    def run(self):
        try:
            self.show_msg_wait(start_txt)
            self.wait_period('pre')
            self.start_cue()
            self.wait_period('exp')
        except QuitException:
            logging.info('quit exception')
        except Exception as e:
            logging.error('some other exception')
            print(e)    
        finally:
            if self.state == 'exp':
                self.end_cue()
            self.show_msg_wait(end_txt)

DummyExp().run()