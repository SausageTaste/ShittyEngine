from abc import ABC, abstractmethod;

import engine.vital.control as con;

class OsInterface(ABC):
    @abstractmethod
    def showWindow(self):
        pass

    @abstractmethod
    def hideWindow(self):
        pass

    @abstractmethod
    def clearFrame(self):
        pass

    @abstractmethod
    def blit(self):
        pass;

    @abstractmethod
    def terminate(self):
        pass

    @abstractmethod
    def getWinSize(self):
        pass

    @abstractmethod
    def updateControl(self, controlData:con.ControlStates):
        pass;
