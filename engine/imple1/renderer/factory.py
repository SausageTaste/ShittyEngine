import numpy as np

import OpenGL.GL as gl
from PIL import Image
import pygame as p

import engine.vital.path as pth;
import engine.imple1.renderer.primitive as pri;


def _makeTextureFromFile(path:pth.Path) -> pri.Texture:
    img:Image.Image = Image.open(path.toStr());
    imgBytes: bytes = img.tobytes("raw", "RGBX", 0, -1);
    width, height = img.size[0:2];
    byteArray = np.array([x / 255 for x in imgBytes], dtype=np.float32);

    gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1);
    texId = gl.glGenTextures(1);

    gl.glActiveTexture(gl.GL_TEXTURE0 + texId);
    gl.glBindTexture(gl.GL_TEXTURE_2D, texId);

    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, width, height, 0, gl.GL_RGBA, gl.GL_FLOAT, byteArray);

    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT);
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT);
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR);
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR);

    return pri.Texture(texId, width, height);


def _getTextMaskMapId(text:str, textSize:int) -> pri.Texture:
    font = p.font.Font("data//fonts\\NanumGothic.ttf", textSize)
    textSurface = font.render(text, True, (255, 255, 255, 255), (0, 0, 0, 255))
    image_bytes = p.image.tostring(textSurface, "RGBA", True)
    imgW_i = textSurface.get_width()
    imgH_i = textSurface.get_height()

    imgArray = np.array([x / 255 for x in image_bytes], dtype=np.float32)

    texId = int( gl.glGenTextures(1) )
    if texId is None:
        raise FileNotFoundError("Failed to get texture id.")

    gl.glBindTexture(gl.GL_TEXTURE_2D, texId)
    gl.glTexStorage2D(gl.GL_TEXTURE_2D, 1, gl.GL_RGBA32F, imgW_i, imgH_i)

    gl.glTexSubImage2D(gl.GL_TEXTURE_2D, 0, 0, 0, imgW_i, imgH_i, gl.GL_RGBA, gl.GL_FLOAT, imgArray)

    texSize_f = imgW_i * imgH_i * 4 * 4 / 1024
    whatIsThis:float = float( texSize_f + texSize_f/3.0 )

    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_BASE_LEVEL, 0)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAX_LEVEL, 1)

    #gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
    #gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)

    gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR_MIPMAP_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    #gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST_MIPMAP_NEAREST)
    #gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

    return pri.Texture( texId, imgW_i, imgH_i )


class TextureManager:
    def __init__(self):
        self.__defaultTex1 = _makeTextureFromFile(pth.Path("data\\textures\\Koreaball-cute.png"));
        self.__defaultTex2 = _makeTextureFromFile(pth.Path("data\\textures\\tile1.bmp"));

        self.__storage = {}
        self.__storageTextMask = {}

    def getDefaultTex1(self):
        return self.__defaultTex1;

    def getDefaultTex2(self):
        return self.__defaultTex2;

    def getTexture(self, name):
        if name not in self.__storage.keys():
            path = pth.Path("data\\textures\\" + name);
            self.__storage[name] = _makeTextureFromFile(path);
        return self.__storage[name];

    @staticmethod
    def getTextMask(text:str, size:int):
        return _getTextMaskMapId(text, size)
