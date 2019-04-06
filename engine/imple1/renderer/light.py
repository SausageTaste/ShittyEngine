import math;
from typing import Tuple;
from abc import ABC, abstractmethod;

import glm;
import OpenGL.GL as gl;

import engine.vital.actor as act;
import engine.imple1.renderer.shader as sha;
import engine.imple1.renderer.globject as glo;


DEPTHMAP_WIDTH:int = 2**10


class AbcLight(ABC):
    def __init__(self):
        self.__rColor:float = 1.0;
        self.__gColor:float = 1.0;
        self.__bColor:float = 1.0;

    def setColorRGB(self, r:float, g:float, b:float) -> None:
        self.__rColor = r;
        self.__gColor = g;
        self.__bColor = b;

    def getColorRGB(self) -> Tuple[float, float, float]:
        return self.__rColor, self.__gColor, self.__bColor;

    @abstractmethod
    def sendUniforms(self, uniloc: sha.UnilocGeneral, index: int) -> None:
        pass


class DirectionalLight(AbcLight):
    def __init__(self):
        super().__init__();

        self.__direction = glm.normalize(glm.vec3(10.0, -10.0, 10.0));
        self.__shadowMap = glo.DepthMap(DEPTHMAP_WIDTH, DEPTHMAP_WIDTH);
        self.__edgeSize = 500.0;

    def setDirection(self, x, y, z):
        self.__direction.x = x;
        self.__direction.y = y;
        self.__direction.z = z;
        self.__direction = glm.normalize(self.__direction);

    def transformDirection(self, mat:glm.tmat4x4):
        self.__direction = glm.normalize(glm.vec3(mat * glm.vec4(self.__direction, 1.0)));

    def sendUniforms(self, uniloc:sha.UnilocGeneral, index:int) -> None:
        color:tuple = self.getColorRGB();
        gl.glUniform3f(uniloc.uDlightColors[index], color[0], color[1], color[2]);
        gl.glUniform3f(uniloc.uDlightDirs[index], self.__direction.x, self.__direction.y, self.__direction.z);

        projViewMat = self.getProjViewMat();
        gl.glUniformMatrix4fv(uniloc.uDlightProjViewMat[index], 1, gl.GL_FALSE, glm.value_ptr(projViewMat));

        gl.glActiveTexture(gl.GL_TEXTURE0 + self.__shadowMap.getTexId());
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__shadowMap.getTexId());
        gl.glUniform1i(uniloc.uDlightDepthMap[index], self.__shadowMap.getTexId());

    def startRenderShadowMap(self, uniloc:sha.UnilocDepth):
        self.__shadowMap.startRender();
        viewMat = self.getProjViewMat();
        gl.glUniformMatrix4fv(uniloc.uProjViewMat, 1, gl.GL_FALSE, glm.value_ptr(viewMat));

    def finishRenderShadowMap(self):
        self.__shadowMap.finishRender();

    def getShadowMap(self):
        return self.__shadowMap;

    def getProjViewMat(self):
        return glm.ortho(-self.__edgeSize, self.__edgeSize,
                         -self.__edgeSize, self.__edgeSize,
                         -self.__edgeSize, self.__edgeSize) * glm.lookAt(-self.__direction, (0, 0, 0), (0, 1, 0));


class PointLight(AbcLight):
    def __init__(self):
        super().__init__();

        self.pos = act.Position();
        self.__maxDistance:float = 5.0;

    def sendUniforms(self, uniloc:sha.UnilocGeneral, index:int) -> None:
        color: tuple = self.getColorRGB();
        gl.glUniform3f(uniloc.uPlightColors[index], color[0], color[1], color[2]);
        gl.glUniform3f(uniloc.uPlightPoses[index], self.pos.getPosX(), self.pos.getPosY(), self.pos.getPosZ());
        gl.glUniform1f(uniloc.uPlightMaxDists[index], self.__maxDistance);

    def setMaxDist(self, v:float):
        self.__maxDistance = v;


class SpotLight(AbcLight):
    def __init__(self):
        super().__init__();

        self.pos = act.Position();
        self.__degrees = glm.vec3(0, 0, 0);

        self.__maxDistance:float = 30.0;

        self.__cutoffDegree = 30.0;
        self.__cutoff = math.cos(glm.radians(self.__cutoffDegree))

        self.__shadowMap = glo.DepthMap(DEPTHMAP_WIDTH, DEPTHMAP_WIDTH);

    def sendUniforms(self, uniloc: sha.UnilocGeneral, index: int):
        color:tuple = self.getColorRGB();
        gl.glUniform3f(uniloc.uSlightColors[index], color[0], color[1], color[2]);
        gl.glUniform3f(uniloc.uSlightPoses[index], self.pos.getPosX(), self.pos.getPosY(), self.pos.getPosZ());
        dirVec = self.getDirVec();
        gl.glUniform3f(uniloc.uSlightDirVec[index], dirVec.x, dirVec.y, dirVec.z);

        gl.glUniform1f(uniloc.uSlightMaxDists[index], self.__maxDistance);
        gl.glUniform1f(uniloc.uSlightCutoff[index], self.__cutoff);

        # Shadow

        projViewMat = self.getProjViewMat();
        gl.glUniformMatrix4fv(uniloc.uSlightProjViewMat[index], 1, gl.GL_FALSE, glm.value_ptr(projViewMat));

        gl.glActiveTexture(gl.GL_TEXTURE0 + self.__shadowMap.getTexId());
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__shadowMap.getTexId());
        gl.glUniform1i(uniloc.uSlightDepthMap[index], self.__shadowMap.getTexId());

    def startRenderShadowMap(self, uniloc:sha.UnilocDepth):
        self.__shadowMap.startRender();
        viewMat = self.getProjViewMat();
        gl.glUniformMatrix4fv(uniloc.uProjViewMat, 1, gl.GL_FALSE, glm.value_ptr(viewMat));

    def finishRenderShadowMap(self):
        self.__shadowMap.finishRender();

    def setDegreeXYZ(self, x:float, y:float, z:float) -> None:
        self.__degrees.x = x;
        self.__degrees.y = y;
        self.__degrees.z = z;

    def setMaxDist(self, v:float):
        self.__maxDistance = v;

    def getProjMat(self) -> glm.mat4:
        return glm.perspective(glm.radians(self.__cutoffDegree)*2.0, 1.0, 0.1, self.__maxDistance*1.0);

    def getViewMat(self) -> glm.mat4:
        mat = glm.mat4(1);
        mat = glm.rotate(mat, glm.radians(self.__degrees.x), glm.vec3(1, 0, 0));
        mat = glm.rotate(mat, glm.radians(self.__degrees.y), glm.vec3(0, 1, 0));
        mat = glm.translate(mat, -self.pos.getVec());

        return mat;

    def getProjViewMat(self) -> glm.mat4:
        return self.getProjMat() * self.getViewMat();

    def getDirVec(self):
        vec = glm.vec4(0, 0, -1, 0);
        vec = glm.rotate(glm.mat4(1), glm.radians(-self.__degrees.x), (1, 0, 0)) * vec;
        vec = glm.rotate(glm.mat4(1), glm.radians(-self.__degrees.y), (0,1,0)) * vec;

        return glm.normalize(vec);

    def getShadowMap(self):
        return self.__shadowMap;
