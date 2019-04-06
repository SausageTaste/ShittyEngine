import time;


class FrameCounter:
    def __init__(self):
        self.__this:float = time.time();
        self.__last:float = self.__this - (1 / 30);

    def update(self) -> None:
        self.__last = self.__this;
        self.__this: float = time.time();

    def getDeltaTime(self) -> float:
        return self.__this - self.__last;

    def getFPS(self) -> float:
        try:
            return 1.0/self.getDeltaTime();
        except ZeroDivisionError:
            return -1.0;
