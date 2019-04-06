import OpenGL.GL as gl

import engine.imple1.renderer.shader as sha
import engine.imple1.renderer.primitive as pri;

class ColoredOverlay:
    def __init__(self):
        self.__left: float = -0.5
        self.__right: float = 0.5
        self.__top: float = 0.5
        self.__bottom: float = -0.5

        self.__rColor: float = 1.0
        self.__gColor: float = 1.0
        self.__bColor: float = 1.0
        self.__trancparency: float = 1.0

        self.__maskMap:pri.Texture = None

    def render(self, uniloc: sha.UnilocOverlay) -> None:
        gl.glUniform1f(uniloc.uLeft, self.__left)
        gl.glUniform1f(uniloc.uRight, self.__right)
        gl.glUniform1f(uniloc.uTop, self.__top)
        gl.glUniform1f(uniloc.uBottom, self.__bottom)

        gl.glUniform4f(uniloc.uColor, self.__rColor, self.__gColor, self.__bColor, self.__trancparency)

        if self.__maskMap is None:
            gl.glUniform1i(uniloc.uHasMaskMap, 0)
        else:
            gl.glUniform1i(uniloc.uHasMaskMap, 1)
            self.__maskMap.sendUniformsGeneral(uniloc.uMaskMap)

        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)

    def setColor(self, r, g, b):
        self.__rColor = float(r)
        self.__gColor = float(g)
        self.__bColor = float(b)

    def setTrancparency(self, v: float):
        self.__trancparency = float(v)

    def setMaskMap(self, texture: pri.Texture) -> None:
        self.__maskMap = texture

    def setSize_leftTopWidthHeight(
        self, winWidth:float, winHeight:float, left:float, top:float, width:float, height:float
    ):
        self.__left = 2 * left / winWidth - 1
        self.__top = -(2 * top / winHeight - 1)
        self.__right = 2 * (left + width) / winWidth - 1
        self.__bottom = -(2 * (top + height) / winHeight - 1)

        print(self.__left, self.__right, self.__top, self.__bottom)


class LineEdit:
    def __init__(self, winWidth, winHeight):
        self.__xPos:float = 10.0
        self.__yPos:float = 10.0
        self.__width:float = 100.0
        self.__height:float = 20.0

        self.__mainBox = ColoredOverlay()
        self.__mainBox.setColor(0.2, 0.2, 0.2)
        self.__mainBox.setTrancparency(0.9)
        self.__mainBox.setSize_leftTopWidthHeight(
            winWidth, winHeight, self.__xPos, self.__yPos, self.__width, self.__height
        )

    def render(self, uniloc:sha.UnilocOverlay):
        self.__mainBox.render(uniloc)
