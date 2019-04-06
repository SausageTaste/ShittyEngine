
import OpenGL.GL as gl;


def _checkBoundFramebuffer():
    status = gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER)
    if status == gl.GL_FRAMEBUFFER_COMPLETE:
        return
    elif status == gl.GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT:
        raise Exception("GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT");
    elif status == gl.GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS:
        raise Exception("GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS");
    elif status == gl.GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT:
        raise Exception("GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT");
    elif status == gl.GL_FRAMEBUFFER_UNSUPPORTED:
        raise Exception("GL_FRAMEBUFFER_UNSUPPORTED");
    else:
        raise Exception(status);


class DepthMap:
    def __init__(self, width:int=128, height:int=128):
        self.__fbo = gl.glGenFramebuffers(1);

        self.__width:int = int(width);
        self.__height:int = int(height);

        self.__tex = gl.glGenTextures(1)
        gl.glActiveTexture(gl.GL_TEXTURE0 + self.__tex);
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__tex)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_DEPTH_COMPONENT, self.__width, self.__height, 0,  gl.GL_DEPTH_COMPONENT, gl.GL_FLOAT, None);

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_BORDER)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_BORDER)
        gl.glTexParameterfv(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_BORDER_COLOR, (1.0, 1.0, 1.0, 1.0))

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.__fbo);
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, gl.GL_TEXTURE_2D, self.__tex, 0)
        gl.glDrawBuffer(gl.GL_NONE)
        gl.glReadBuffer(gl.GL_NONE)

        _checkBoundFramebuffer();
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    def getTexId(self):
        return self.__tex;

    def startRender(self):
        gl.glDisable(gl.GL_CULL_FACE);
        gl.glViewport(0, 0, self.__width, self.__height);
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.__fbo);
        gl.glClear(gl.GL_DEPTH_BUFFER_BIT);

    @staticmethod
    def finishRender():
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        gl.glEnable(gl.GL_CULL_FACE);
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT);


class DepthCubeMap:
    def __init__(self):
        self.__fbo = gl.glGenFramebuffers(1)
        self.__depthCubeMap = gl.glGenTextures(1);
        self.__width = 1024;
        self.__height = 1024;

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__depthCubeMap)
        gl.glActiveTexture(gl.GL_TEXTURE0 + self.__depthCubeMap);
        for i in range(6):
            gl.glTexImage2D(
                gl.GL_TEXTURE_CUBE_MAP_POSITIVE_X + i,
                0,
                gl.GL_DEPTH_COMPONENT,
                self.__width,
                self.__height,
                0,
                gl.GL_DEPTH_COMPONENT,
                gl.GL_FLOAT,
                None
            );

        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST);
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST);
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE);
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE);
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_R, gl.GL_CLAMP_TO_EDGE);

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.__fbo);
        gl.glFramebufferTexture(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, self.__depthCubeMap, 0);
        gl.glDrawBuffer(gl.GL_NONE);
        gl.glReadBuffer(gl.GL_NONE);

        if gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) != gl.GL_FRAMEBUFFER_COMPLETE:
            raise Exception(
                "ERROR::FRAMEBUFFER:: Framebuffer is not complete! -> {:02X}".format(gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER))
            )
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    def getTexSize(self) -> tuple:
        return self.__width, self.__height;

    def startRender(self):
        gl.glDisable(gl.GL_CULL_FACE);
        gl.glViewport(0, 0, self.__width, self.__height);
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.__fbo);
        gl.glClear(gl.GL_DEPTH_BUFFER_BIT);

    @staticmethod
    def finishRender():
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0);
        gl.glEnable(gl.GL_CULL_FACE);
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT);
