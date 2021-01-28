from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB']
from psychopy import sound


class AudioPeep:

    def __init__(self, C):
        print(('Using %s (with %s)' % (sound.audioLib, sound.audioDriver)))
        sound.init(stereo=False, buffer=128)  # rate=44100, 
        self.peep = sound.Sound(value=C['value'], secs=C['duration'],
            autoLog=True)  # sampleRate=44100, 
        self.peep.setVolume(C['volume'], log=False)

    def play(self):
        self.peep.play()