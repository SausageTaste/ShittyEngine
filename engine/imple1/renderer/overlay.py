import OpenGL.GL as gl

import engine.imple1.renderer.shader as sha
import engine.vital.path as pth
import engine.imple1.renderer.factory as fac
import engine.imple1.renderer.overlayWidgets as ovw


class OverlayMaster:
    def __init__(self, textureMaster:fac.TextureManager, width:int, height:int):
        self.__texMaster = textureMaster

        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        sourceDepth = sha.ShaderSource()
        sourceDepth.attachVertSource(pth.getFileContents(pth.Path("data\\glsl\\overlay_v.glsl")))
        sourceDepth.attachFragSource(pth.getFileContents(pth.Path("data\\glsl\\overlay_f.glsl")))
        self.__shader = sourceDepth.compile()
        self.__uniloc = sha.UnilocOverlay(self.__shader)

        self.__sample = ovw.LineEdit(width, height)

    def render(self):
        gl.glEnable(gl.GL_BLEND)

        self.__shader.activate()
        self.__sample.render(self.__uniloc)
        gl.glDisable(gl.GL_BLEND)
