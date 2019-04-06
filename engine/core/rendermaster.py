from abc import ABC, abstractmethod;


class RenderUnit(ABC):
    @abstractmethod
    def renderGeneral(self):
        pass

    @abstractmethod
    def renderDepth(self):
        pass

    @abstractmethod
    def delete(self) -> None:
        pass;


class RenderMaster(ABC):
    @abstractmethod
    def update(self, deltaTime:float, winSize:tuple) -> None:
        pass

    @abstractmethod
    def terminate(self) -> None:
        pass;

