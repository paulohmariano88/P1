
from abc import ABC, abstractmethod
class Signal(ABC):


    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass




class SoundSignal(Signal):

    def stop(self):
        pass

    def start(self):
        pass

