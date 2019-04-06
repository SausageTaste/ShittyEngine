

class Path:
    def __init__(self, arg):
        self.__data = str(arg);

    def toStr(self):
        return self.__data;


def getFileContents(path:Path) -> str:
    with open(path.toStr(), "r") as file:
        return file.read();
