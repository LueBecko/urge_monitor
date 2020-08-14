from psychopy import core
from psychopy import parallel
import serial

class PulseListener:
    '''simple class for parallel port pulse reading, support simulation'''
    # TODO: polymorphic PulseListener (simulation, parallel, serial, keyboard)
    def __init__(self, C, IL):
        self.__InputListener__ = IL
        self.__sim__ = C['pulse']['simulation']
        if self.__sim__:
            self.__clock__ = core.Clock()
            self.__clock__.add(1.5)  # 1.5 s time before simulated pulse
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
