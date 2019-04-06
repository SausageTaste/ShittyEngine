from typing import List;

import OpenGL.GL as gl;


class _Shader:
    def __init__(self, programId:int):
        self.__programId = programId;

    def activate(self) -> None:
        gl.glUseProgram(self.__programId);

    def getUniloc(self, arg:str):
        a = gl.glGetUniformLocation(self.__programId, str(arg));
        if a != -1:
            return a;

        a = gl.glGetAttribLocation(self.__programId, arg);
        if a != -1:
            return a;

        return -1;


class ShaderSource:
    def __init__(self):
        self.__vertSources:List[str] = [];
        self.__fragSources:List[str] = [];
        self.__geomSources:List[str] = [];

    def attachVertSource(self, s:str) -> None:
        self.__vertSources.append(str(s));

    def attachFragSource(self, s:str) -> None:
        self.__fragSources.append(str(s));

    def attachGeomSource(self, s:str) -> None:
        self.__geomSources.append(str(s));

    def compile(self) -> _Shader:
        vertShaders:list = [];
        fragShaders:list = [];
        geomShaders:list = [];

        for vertShaderSource in self.__vertSources:
            shader = gl.glCreateShader(gl.GL_VERTEX_SHADER);
            gl.glShaderSource(shader, vertShaderSource);
            gl.glCompileShader(shader);

            if gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS) == gl.GL_FALSE:
                shaderLog = gl.glGetShaderInfoLog(shader);
                raise RuntimeError(shaderLog)

            vertShaders.append(shader);

        for fragShaderSource in self.__fragSources:
            shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER);
            gl.glShaderSource(shader, fragShaderSource);
            gl.glCompileShader(shader);

            if gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS) == gl.GL_FALSE:
                shaderLog = gl.glGetShaderInfoLog(shader);
                raise RuntimeError(shaderLog)

            fragShaders.append(shader);

        for geomShaderSource in self.__geomSources:
            shader = gl.glCreateShader(gl.GL_GEOMETRY_SHADER);
            gl.glShaderSource(shader, geomShaderSource);
            gl.glCompileShader(shader);

            if gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS) == gl.GL_FALSE:
                shaderLog = gl.glGetShaderInfoLog(shader);
                raise RuntimeError(shaderLog)

            geomShaders.append(shader);

        program = gl.glCreateProgram();

        for i in vertShaders:
            gl.glAttachShader(program, i);
        for i in fragShaders:
            gl.glAttachShader(program, i);
        for i in geomShaders:
            gl.glAttachShader(program, i);

        gl.glLinkProgram(program)

        if gl.glGetProgramiv(program, gl.GL_LINK_STATUS) == gl.GL_FALSE:
            shaderLog = gl.glGetProgramInfoLog(program);
            gl.glDeleteProgram(program);
            raise RuntimeError(shaderLog);

        for i in vertShaders:
            gl.glDetachShader(program, i);
            gl.glDeleteShader(i);
        for i in fragShaders:
            gl.glDetachShader(program, i);
            gl.glDeleteShader(i);
        for i in geomShaders:
            gl.glDetachShader(program, i);
            gl.glDeleteShader(i);

        return _Shader(program);


class Uniloc:
    def checkIntegrity(self):
        for x in self.__dir__():
            if not (x.startswith("u") or x.startswith("i")):
                if self.__getattribute__(x) == -1:
                    raise RuntimeError("{} is -1".format(x));

    def print(self):
        for x in self.__dir__():
            if not (x.startswith("u") or x.startswith("i")):
                continue;

            print(x, self.__getattribute__(x));


class UnilocGeneral(Uniloc):
    def __init__(self, shader:_Shader):
        ## Vert

        # From Master
        self.uProjViewMat = shader.getUniloc("uProjViewMat");

        # From GameObject
        self.uModelMatrix = shader.getUniloc("uModelMatrix");

        # From Mesh
        self.iPosition = shader.getUniloc("iPosition");
        self.iTexCoord = shader.getUniloc("iTexCoord");
        self.iNormal = shader.getUniloc("iNormal");

        # From Matarial
        self.uTextureVerNum = shader.getUniloc("uTextureVerNum");
        self.uTextureHorNum = shader.getUniloc("uTextureHorNum");

        ## Frag

        # From Master
        self.uViewPos = shader.getUniloc("uViewPos");
        self.uBaseAmbient = shader.getUniloc("uBaseAmbient");
        self.uDlightCount = shader.getUniloc("uDlightCount");
        self.uPlightCount = shader.getUniloc("uPlightCount");
        self.uSlightCount = shader.getUniloc("uSlightCount");

        # From Lights
        # Directional
        self.uDlightDirs = (
            shader.getUniloc("uDlightDirs[0]"),
            shader.getUniloc("uDlightDirs[1]"),
            shader.getUniloc("uDlightDirs[2]"),
        );
        self.uDlightColors = (
            shader.getUniloc("uDlightColors[0]"),
            shader.getUniloc("uDlightColors[1]"),
            shader.getUniloc("uDlightColors[2]"),
        );
        self.uDlightProjViewMat = (
            shader.getUniloc("uDlightProjViewMat[0]"),
            shader.getUniloc("uDlightProjViewMat[1]"),
            shader.getUniloc("uDlightProjViewMat[2]"),
        );
        self.uDlightDepthMap = (
            shader.getUniloc("uDlightDepthMap[0]"),
            shader.getUniloc("uDlightDepthMap[1]"),
            shader.getUniloc("uDlightDepthMap[2]"),
        );
        # Point
        self.uPlightPoses = (
            shader.getUniloc("uPlightPoses[0]"),
            shader.getUniloc("uPlightPoses[1]"),
            shader.getUniloc("uPlightPoses[2]"),
        );
        self.uPlightColors = (
            shader.getUniloc("uPlightColors[0]"),
            shader.getUniloc("uPlightColors[1]"),
            shader.getUniloc("uPlightColors[2]"),
        );
        self.uPlightMaxDists = (
            shader.getUniloc("uPlightMaxDists[0]"),
            shader.getUniloc("uPlightMaxDists[1]"),
            shader.getUniloc("uPlightMaxDists[2]"),
        );
        # Spot
        self.uSlightColors = (
            shader.getUniloc("uSlightColors[0]"),
            shader.getUniloc("uSlightColors[1]"),
            shader.getUniloc("uSlightColors[2]"),
        );
        self.uSlightPoses = (
            shader.getUniloc("uSlightPoses[0]"),
            shader.getUniloc("uSlightPoses[1]"),
            shader.getUniloc("uSlightPoses[2]"),
        );
        self.uSlightDirVec = (
            shader.getUniloc("uSlightDirVec[0]"),
            shader.getUniloc("uSlightDirVec[1]"),
            shader.getUniloc("uSlightDirVec[2]"),
        );
        self.uSlightMaxDists = (
            shader.getUniloc("uSlightMaxDists[0]"),
            shader.getUniloc("uSlightMaxDists[1]"),
            shader.getUniloc("uSlightMaxDists[2]"),
        );
        self.uSlightCutoff = (
            shader.getUniloc("uSlightCutoff[0]"),
            shader.getUniloc("uSlightCutoff[1]"),
            shader.getUniloc("uSlightCutoff[2]"),
        );
        self.uSlightDepthMap = (
            shader.getUniloc("uSlightDepthMap[0]"),
            shader.getUniloc("uSlightDepthMap[1]"),
            shader.getUniloc("uSlightDepthMap[2]"),
        );
        self.uSlightProjViewMat = (
            shader.getUniloc("uSlightProjViewMat[0]"),
            shader.getUniloc("uSlightProjViewMat[1]"),
            shader.getUniloc("uSlightProjViewMat[2]"),
        );

        # From Matarial
        self.uShininess = shader.getUniloc("uShininess");
        self.uSpecularStrength = shader.getUniloc("uSpecularStrength");

        # From Texture
        self.uDiffuseMap = shader.getUniloc("uDiffuseMap");

        self.checkIntegrity();


class UnilocDepth(Uniloc):
    def __init__(self, shader:_Shader):
        ## Vert

        # From Master
        self.iPosition = shader.getUniloc("iPosition");
        self.uProjViewMat = shader.getUniloc("uProjViewMat");
        self.uModelMat = shader.getUniloc("uModelMat");

        self.checkIntegrity();


class UnilocOverlay(Uniloc):
    def __init__(self, shader:_Shader):
        ## Vert

        self.uLeft   = shader.getUniloc("uLeft");
        self.uRight  = shader.getUniloc("uRight");
        self.uTop    = shader.getUniloc("uTop");
        self.uBottom = shader.getUniloc("uBottom");

        self.uColor = shader.getUniloc("uColor");

        self.uHasMaskMap = shader.getUniloc("uHasMaskMap");
        self.uMaskMap = shader.getUniloc("uMaskMap");

        self.checkIntegrity();
