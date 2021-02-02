from psychopy import core
from psychopy import parallel
import serial
from abc import ABC, abstractmethod

class PulseListener(ABC):
    '''interface for various pulse listeners'''

    __config__: None;

    def __init__(self, config):
        self.__config__ = config;

    @abstractmethod
    def initDevice(self):
        '''initialize the specified device'''
        pass

    @abstractmethod
    def pulseReceived(self):
        '''checks if a pulse was received'''
        pass

class ParallelPulseListener(PulseListener):
    '''receive pulses via parallel port'''

    def initDevice(self):
        '''initialize the specified device'''
        self.__pin__ = self.__config__['pin']
        self.__address__ = self.__config__['address']
        self.__port__ = parallel.ParallelPort(address=self.__address__)
        self.__base__ = self.__port__.readPin(self.__pin__)

    def pulseReceived(self):
        '''checks if a pulse was received'''
        return self.__port__.readPin(self.__pin__) != self.__base__


class SerialPulseListener(PulseListener):
    '''receive pulses via serial port'''

    def initDevice(self):
        '''initialize the specified device'''
        self.__portname__ = self.__config__['port']
        self.__baudrate__ = self.__config__['baudrate']
        self.__bytesize__ = self.__config__['bytesize']
        self.__parity__ = self.__config__['parity']
        self.__stopbits__ = self.__config__['stopbits']
        self.__timeout__ = self.__config__['timeout']
        self.__xonxoff__ = self.__config__['xonxoff']
        self.__rtscts__ = self.__config__['rtscts']
        self.__dsrdtr__ = self.__config__['dsrdtr']
        self.__inter_byte_timeout__ = self.__config__['inter_byte_timeout']
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

    def pulseReceived(self):
        '''checks if a pulse was received'''
        return len(self.__port__.read(1)) != 0

    def __del__(self):
        if not self.__port__ is None:
            self.__port__.close()


class KeyboardPulseListener(PulseListener):
    '''receive pulses via specified keyboard key'''

    def __init__(self, config, inputListener):
        self.__config__ = config;
        self.__InputListener__ = inputListener;

    def initDevice(self):
        '''initialize the specified device'''
        self.__key__ = self.__config__['key']
        self.__InputListener__.RegisterKey(self.__key__)

    def pulseReceived(self):
        '''checks if a pulse was received'''
        return self.__key__ in self.__InputListener__.GetPressedKeys()

    def __del__(self):
        '''clear specified device'''
        self.__InputListener__.UnregisterKey(self.__key__)


class SimulatedPulseListener(PulseListener):
    '''simulate receiving a pulse after a fixed amount of time (1,5 s)'''

    def __init__(self):
        pass

    def initDevice(self):
        '''initialize the specified device'''
        self.__clock__ = core.Clock()
        self.__clock__.add(1.5)  # 1.5 s time before simulated pulse

    def pulseReceived(self):
        '''checks if a pulse was received'''
        return self.__clock__.getTime() >= 0.0


class NonePulseListener(PulseListener):
    '''no waiting to receive a pulse'''

    def __init__(self):
        pass

    def initDevice(self):
        '''initialize the specified device'''
        pass

    def pulseReceived(self):
        '''checks if a pulse was received'''
        return True


def createPulseListener(config, inputListener):
    '''factory method for PulseListener specified by configuration in pulse.ini'''
    if config['pulse']['simulation']:
        return SimulatedPulseListener()
    else:
        interface = __extractInterface(config)

        if interface == 'parallel':
            return ParallelPulseListener(__extractInterfaceConfiguration(config))
        elif interface == 'serial':
            return SerialPulseListener(__extractInterfaceConfiguration(config))
        elif interface == 'keyboard':
            return KeyboardPulseListener(__extractInterfaceConfiguration(config), inputListener=inputListener)
        else:
            return NonePulseListener()

def __extractInterface(config):
    interface = config['pulse']['interface']
    if (isinstance(interface, str)):
        interface = interface.lower()
    else:
        interface = 'none'
    return interface

def __extractInterfaceConfiguration(config):
    interface = __extractInterface(config)
    assert interface in config
    return config[interface]
