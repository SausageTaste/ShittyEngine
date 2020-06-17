import glm;
from typing import List;

import engine.core.rendermaster as ren;
import engine.vital.rotator as rot;


class Position:
    def __init__(self):
        self.__xPos = 0.0;
        self.__yPos = 0.0;
        self.__zPos = 0.0;

    def getPosX(self) -> float:
        return self.__xPos;

    def getPosY(self) -> float:
        return self.__yPos;

    def getPosZ(self) -> float:
        return self.__zPos;

    def setPosX(self, v:float) -> None:
        self.__xPos = float(v);

    def setPosY(self, v:float) -> None:
        self.__yPos = float(v);

    def setPosZ(self, v:float) -> None:
        self.__zPos = float(v);

    def setXYZ(self, x, y, z) -> None:
        self.__xPos = x;
        self.__yPos = y;
        self.__zPos = z;

    def getVec(self) -> glm.vec3:
        return glm.vec3(self.__xPos, self.__yPos, self.__zPos);

    def setVec(self, v:glm.vec3) -> None:
        self.__xPos = v.x;
        self.__yPos = v.y;
        self.__zPos = v.z;

    def addVec(self, v:glm.vec3) -> None:
        self.__xPos += v.x;
        self.__yPos += v.y;
        self.__zPos += v.z;


class GameObject:
    def __init__(self):
        self.pos:Position = Position();
        self.angle:rot.AngleEulerDegree = rot.AngleEulerDegree();
        self.scale = glm.vec3(1, 1, 1);

        self.renderUnits:List[ren.RenderUnit] = [];

    def getModelMat(self) -> glm.mat4:
        tranMat = glm.translate(glm.mat4(1), self.pos.getVec());
        rotMat = self.angle.getModelMat();
        scaleMat = glm.scale(glm.mat4(1), self.scale);

        return tranMat * rotMat * scaleMat;

    def getViewMat(self) -> glm.mat4:
        m = self.angle.getViewMat();
        m = glm.translate(m, -self.pos.getVec());
        return m;
