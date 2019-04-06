from abc import ABC, abstractmethod;

import glm;


class AngleABC(ABC):
    @abstractmethod
    def getViewMat(self) -> glm.tmat4x4:
        pass


class AngleEulerDegree(AngleABC):
    def __init__(self):
        self.__x = 0.0;
        self.__y = 0.0;
        self.__z = 0.0;

    def getViewMat(self):
        mat = glm.mat4(1.0);

        mat = glm.rotate(mat, -glm.radians(self.__x), (1.0, 0.0, 0.0));
        mat = glm.rotate(mat, -glm.radians(self.__y), (0.0, 1.0, 0.0));
        mat = glm.rotate(mat, -glm.radians(self.__z), (0.0, 0.0, 1.0));

        return mat;

    def getModelMat(self):
        mat = glm.mat4(1.0);

        mat = glm.rotate(mat, glm.radians(self.__z), (0.0, 0.0, 1.0));
        mat = glm.rotate(mat, glm.radians(self.__y), (0.0, 1.0, 0.0));
        mat = glm.rotate(mat, glm.radians(self.__x), (1.0, 0.0, 0.0));

        return mat;

    def getX(self) -> float:
        return self.__x;
    def getY(self) -> float:
        return self.__y;
    def getZ(self) -> float:
        return self.__z;
    def getAsVec(self) -> glm.vec3:
        return glm.vec3(self.__x, self.__y, self.__z);

    def setX(self, v:float) -> None:
        self.__x = float(v);
    def setY(self, v:float) -> None:
        self.__y = float(v);
    def setZ(self, v:float) -> None:
        self.__z = float(v);
    def setXYZ(self, x:float, y:float, z:float) -> None:
        self.__x = float(x);
        self.__y = float(y);
        self.__z = float(z);

    def addXYZ(self, x:float, y:float, z:float) -> None:
        self.__x += float(x);
        self.__y += float(y);
        self.__z += float(z);

