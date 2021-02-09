from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB']
from psychopy import sound
import time

class AudioPeep:

    def __init__(self, C):
        print(('Using %s (with %s)' % (sound.audioLib, sound.audioDriver)))
        sound.init(stereo=False, buffer=128)  # rate=44100, 
        self.peep = sound.Sound(value=C['value'], secs=C['duration'],
            autoLog=True)  # sampleRate=44100, 
        self.peep.setVolume(C['volume'], log=False)
        #self.play()
        #time.sleep(C['duration'])

    def play(self):
        self.peep.play()


# play dummy sound (vol 0)
startup_cfg = {'value': 880, 'duration': 0.2, 'volume': 0.5}
AudioPeep(startup_cfg).play()
