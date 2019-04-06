from typing import Iterable;

import numpy as np;
import glm;

import OpenGL.GL as gl;

import engine.imple1.renderer.shader as sha;


class Texture:
    def __init__(self, texId, width=1, height=1):
        self.__texId = texId;
        self.__width = width;
        self.__height = height;

    def sendUniforms(self, uniloc:sha.UnilocGeneral):
        gl.glActiveTexture(gl.GL_TEXTURE0 + self.__texId);
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__texId);
        gl.glUniform1i(uniloc.uDiffuseMap, self.__texId);

        #gl.glUniform1i(uniloc.uDiffuseMap, gl.GL_TEXTURE0)
        #gl.glActiveTexture(gl.GL_TEXTURE0)
        #gl.glBindTexture(gl.GL_TEXTURE_2D, self.__texId);

    def sendUniformsGeneral(self, unilocValue):
        gl.glActiveTexture(gl.GL_TEXTURE0 + self.__texId);
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__texId);
        gl.glUniform1i(unilocValue, self.__texId);


class Material:
    def __init__(self):
        self.__textureVerNum:float = 1.0;
        self.__textureHorNum:float = 1.0;

        self.__shininess:float = 32.0;
        self.__specularStrength:float = 1.0;

    def sendUniforms(self, uniloc:sha.UnilocGeneral):
        gl.glUniform1f(uniloc.uTextureVerNum, self.__textureVerNum);
        gl.glUniform1f(uniloc.uTextureHorNum, self.__textureHorNum);

        gl.glUniform1f(uniloc.uShininess, self.__shininess);
        gl.glUniform1f(uniloc.uSpecularStrength, self.__specularStrength);

    def setTexSize(self, x:float, y:float) -> None:
        self.__textureHorNum = x;
        self.__textureVerNum = y;

    def setShininess(self, v:float):
        assert isinstance(v, float);
        self.__shininess = v;

    def setSpecularStrength(self, v:float):
        assert isinstance(v, float);
        self.__specularStrength = v;


class Mesh:
    def __init__(self, uniloc:sha.UnilocGeneral, vertices:np.ndarray, texCoords:np.ndarray, normals:np.ndarray):
        self.__initialized:bool = False;

        self.__mVao:int = 0;

        self.__mVertexArrayBuffer = 0;
        self.__mTexCoordArrayBuffer = 0;
        self.__mNormalArrayBuffe = 0;

        self.__mVertexNum:int = 0;
        self.__mVramUsage:int = 0;

        self.__createBuffer();
        self.__buildBuffer(uniloc, vertices, texCoords, normals);

    def __createBuffer(self):
        self.__mVao = int(gl.glGenVertexArrays(1));
        if self.__mVao <= 0:
            raise RuntimeError;

        self.__mVertexArrayBuffer = int(gl.glGenBuffers(1));
        if self.__mVertexArrayBuffer <= 0:
            raise RuntimeError;

        self.__mTexCoordArrayBuffer = int(gl.glGenBuffers(1));
        if self.__mTexCoordArrayBuffer <= 0:
            raise RuntimeError;

        self.__mNormalArrayBuffe = int(gl.glGenBuffers(1));
        if self.__mNormalArrayBuffe <= 0:
            raise RuntimeError;

    def __bindVao(self):
        assert self.__mVao > 0;

        gl.glBindVertexArray(self.__mVao);

    @staticmethod
    def __unbindVao():
        gl.glBindVertexArray(0);

    def __buildBuffer(self, uniloc:sha.UnilocGeneral, vertices:np.ndarray, texCoords:np.ndarray, normals:np.ndarray):
        if self.__initialized:
            raise RuntimeError;

        self.__bindVao();

        # Vertices

        size:int = vertices.size * vertices.itemsize;
        self.__mVertexNum = int(vertices.size / 3);
        self.__mVramUsage += size;

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.__mVertexArrayBuffer);
        gl.glBufferData(gl.GL_ARRAY_BUFFER, size, vertices, gl.GL_STATIC_DRAW);

        gl.glEnableVertexAttribArray(uniloc.iPosition);
        gl.glVertexAttribPointer(uniloc.iPosition, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None);

        # TexCoords

        size = texCoords.size * texCoords.itemsize;
        self.__mVramUsage += size;
        if self.__mVertexNum != int(texCoords.size / 2):
            raise RuntimeError;

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.__mTexCoordArrayBuffer);
        gl.glBufferData(gl.GL_ARRAY_BUFFER, size, texCoords, gl.GL_STATIC_DRAW);

        gl.glEnableVertexAttribArray(uniloc.iTexCoord);
        gl.glVertexAttribPointer(uniloc.iTexCoord, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None);

        # Normals

        size = int(normals.size * normals.itemsize);
        self.__mVramUsage += size;
        if self.__mVertexNum != int(normals.size / 3):
            raise RuntimeError;

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.__mNormalArrayBuffe);
        gl.glBufferData(gl.GL_ARRAY_BUFFER, size, normals, gl.GL_STATIC_DRAW);

        gl.glVertexAttribPointer(uniloc.iNormal, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None);
        gl.glEnableVertexAttribArray( uniloc.iNormal );

        #

        self.__unbindVao();
        self.__initialized = True;

    def renderGeneral(self):
        self.__bindVao()
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.__mVertexNum);

    def renderDepth(self):
        self.__bindVao()
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.__mVertexNum);


def createMeshAabb(uniloc:sha.UnilocGeneral, xOne, xTwo, yOne, yTwo, zOne, zTwo) -> Mesh:
    if xOne > xTwo:
        xOne, xTwo = xTwo, xOne;
    if yOne > yTwo:
        yOne, yTwo = yTwo, yOne;
    if xOne > xTwo:
        zOne, zTwo = zTwo, zOne;

    vertices = np.array([
        xOne, yTwo, zTwo,
        xOne, yOne, zTwo,
        xTwo, yOne, zTwo,
        xOne, yTwo, zTwo,
        xTwo, yOne, zTwo,
        xTwo, yTwo, zTwo,

        xTwo, yTwo, zTwo,
        xTwo, yOne, zTwo,
        xTwo, yOne, zOne,
        xTwo, yTwo, zTwo,
        xTwo, yOne, zOne,
        xTwo, yTwo, zOne,

        xTwo, yTwo, zOne,
        xTwo, yOne, zOne,
        xOne, yOne, zOne,
        xTwo, yTwo, zOne,
        xOne, yOne, zOne,
        xOne, yTwo, zOne,

        xOne, yTwo, zOne,
        xOne, yOne, zOne,
        xOne, yOne, zTwo,
        xOne, yTwo, zOne,
        xOne, yOne, zTwo,
        xOne, yTwo, zTwo,

        xOne, yTwo, zOne,
        xOne, yTwo, zTwo,
        xTwo, yTwo, zTwo,
        xOne, yTwo, zOne,
        xTwo, yTwo, zTwo,
        xTwo, yTwo, zOne,

        xOne, yOne, zTwo,
        xOne, yOne, zOne,
        xTwo, yOne, zOne,
        xOne, yOne, zTwo,
        xTwo, yOne, zOne,
        xTwo, yOne, zTwo,
    ], np.float32);

    texCoords = np.array([
        0, 1,
        0, 0,
        1, 0,
        0, 1,
        1, 0,
        1, 1,

        0, 1,
        0, 0,
        1, 0,
        0, 1,
        1, 0,
        1, 1,

        0, 1,
        0, 0,
        1, 0,
        0, 1,
        1, 0,
        1, 1,

        0, 1,
        0, 0,
        1, 0,
        0, 1,
        1, 0,
        1, 1,

        0, 1,
        0, 0,
        1, 0,
        0, 1,
        1, 0,
        1, 1,

        0, 1,
        0, 0,
        1, 0,
        0, 1,
        1, 0,
        1, 1,
    ], np.float32)

    normals = np.array([
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,

        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,
        1, 0, 0,

        0, 0, -1,
        0, 0, -1,
        0, 0, -1,
        0, 0, -1,
        0, 0, -1,
        0, 0, -1,

        -1, 0, 0,
        -1, 0, 0,
        -1, 0, 0,
        -1, 0, 0,
        -1, 0, 0,
        -1, 0, 0,

        0, 1, 0,
        0, 1, 0,
        0, 1, 0,
        0, 1, 0,
        0, 1, 0,
        0, 1, 0,

        0, -1, 0,
        0, -1, 0,
        0, -1, 0,
        0, -1, 0,
        0, -1, 0,
        0, -1, 0,
    ], np.float32)

    return Mesh(uniloc, vertices, texCoords, normals);

def createMeshHexahedron(vertices:Iterable[glm.vec3]):
    for x in vertices:
        print(x);

def createMeshWithArray(uniloc:sha.UnilocGeneral, vertices:Iterable[float], texCoords:Iterable[float], normals:Iterable[float]):
    return Mesh(
        uniloc,
        np.array(vertices, np.float32),
        np.array(texCoords, np.float32),
        np.array(normals, np.float32)
    );