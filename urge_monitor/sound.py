# -*- coding: utf-8 -*-

from psychopy import prefs
prefs.general['audioLib'] = ['pygame']  # use pygame because of better support
from psychopy import sound


class AudioPeep:

    def __init__(self, C):
        print(('Using %s(with %s)' % (sound.audioLib, sound.audioDriver)))
        sound.init(rate=44100, stereo=False, buffer=128)
        self.peep = sound.Sound(value=C['value'], secs=C['duration'],
            sampleRate=44100, autoLog=True)
        self.peep.setVolume(C['volume'], log=False)

    def play(self):
        self.peep.play()