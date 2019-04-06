from typing import List;

import glm;

import OpenGL.GL as gl;

import engine.vital.path as pth;
import engine.vital.actor as act;
import engine.core.rendermaster as ren;
import engine.imple1.renderer.light as lit;
import engine.imple1.renderer.shader as sha;
import engine.imple1.renderer.factory as rfa;
import engine.imple1.renderer.primitive as rpi;
import engine.imple1.resource.parser as par;


def _renderObjectGeneral(obj:act.GameObject, uniloc:sha.UnilocGeneral) -> None:
    modelMat = obj.getModelMat();
    gl.glUniformMatrix4fv(uniloc.uModelMatrix, 1, gl.GL_FALSE, glm.value_ptr(modelMat));
    for renderer in obj.renderUnits:
        renderer.renderGeneral();

def _renderObjectDepth(obj:act.GameObject, uniloc:sha.UnilocDepth):
    modelMat = obj.getModelMat();
    gl.glUniformMatrix4fv(uniloc.uModelMat, 1, gl.GL_FALSE, glm.value_ptr(modelMat));
    for renderer in obj.renderUnits:
        renderer.renderDepth();


class RenderUnitGL(ren.RenderUnit):
    __sUnilocGeneral = None;

    def __init__(self, mesh:rpi.Mesh, material:rpi.Material, texture:rpi.Texture, unilocGeneral:sha.UnilocGeneral):
        self.__mesh = mesh;
        self.__material = material;
        self.__texture = texture;

        self.__sUnilocGeneral = unilocGeneral

    def renderGeneral(self) -> None:
        self.__material.sendUniforms(self.__sUnilocGeneral);
        self.__texture.sendUniforms(self.__sUnilocGeneral);
        self.__mesh.renderGeneral();

    def renderDepth(self) -> None:
        self.__mesh.renderDepth();

    def delete(self) -> None:
        pass;


class RenderMasterGL(ren.RenderMaster):
    def __init__(self, winWidth:int, winHeight:int, __texMan:rfa.TextureManager):
        self.__texMan = __texMan

        print("Initiate RenderMasterGL");
        print(gl.glGetString(gl.GL_VERSION));

        gl.glEnable(gl.GL_CULL_FACE);
        gl.glEnable(gl.GL_DEPTH_TEST);

        self.__progMat = None;
        self.updateProjMat(winWidth, winHeight);

        sourceGeneral = sha.ShaderSource()
        sourceGeneral.attachVertSource( pth.getFileContents(pth.Path("data\\glsl\\general_v.glsl")) );
        sourceGeneral.attachFragSource( pth.getFileContents(pth.Path("data\\glsl\\general_f.glsl")) );
        self.__shaderGeneral = sourceGeneral.compile();
        self.__unilocGeneral = sha.UnilocGeneral(self.__shaderGeneral);

        sourceDepth = sha.ShaderSource()
        sourceDepth.attachVertSource( pth.getFileContents(pth.Path("data\\glsl\\depth_v.glsl")) );
        sourceDepth.attachFragSource( pth.getFileContents(pth.Path("data\\glsl\\depth_f.glsl")) );
        self.__shaderDepth = sourceDepth.compile();
        self.__unilocDepth = sha.UnilocDepth(self.__shaderDepth);

        self.__renderObjects:list = [];

        self.__sunlight = lit.DirectionalLight();
        self.__moonlight = lit.DirectionalLight();

        self.__dlights:List[lit.DirectionalLight] = [];
        self.__plights:List[lit.PointLight] = [];
        self.__slights:List[lit.SpotLight] = [];
        self.__createLights();

        self.__createMeshes();

        self.__camera = act.GameObject();

        self.__renderAllShadows((winHeight,winWidth));

    def update(self, deltaTime:float, winSize:tuple) -> None:
        self.__sunlight.transformDirection(glm.rotate(glm.mat4(1), 0.5*deltaTime, (1, 0, 0)))

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT);
        gl.glClearBufferfv(gl.GL_COLOR, 0, (0.0, 0.0, 0.0, 1.0));

        self.__renderAllShadows(winSize);

        self.__shaderGeneral.activate();

        projViewMat = self.__progMat * self.__camera.getViewMat();
        #projViewMat = self.__slights[0].getProjViewMat();
        gl.glUniformMatrix4fv(self.__unilocGeneral.uProjViewMat, 1, gl.GL_FALSE, glm.value_ptr(projViewMat));

        gl.glUniform3f( self.__unilocGeneral.uViewPos, self.__camera.pos.getPosX(), self.__camera.pos.getPosY(),
                        self.__camera.pos.getPosZ() );
        gl.glUniform3f(self.__unilocGeneral.uBaseAmbient, 0.1, 0.1, 0.1);

        gl.glUniform1i(self.__unilocGeneral.uDlightCount, len(self.__dlights));
        gl.glUniform1i(self.__unilocGeneral.uPlightCount, len(self.__plights));
        gl.glUniform1i(self.__unilocGeneral.uSlightCount, len(self.__slights));
        for i, dlight in enumerate(self.__dlights):
            dlight.sendUniforms(self.__unilocGeneral, i);
        for i, plight in enumerate(self.__plights):
            plight.sendUniforms(self.__unilocGeneral, i);
        for i, slight in enumerate(self.__slights):
            slight.sendUniforms(self.__unilocGeneral, i);

        for obj in self.__renderObjects:
            _renderObjectGeneral(obj, self.__unilocGeneral);

    def terminate(self) -> None:
        pass;

    def setCameraObj(self, obj:act.GameObject) -> None:
        self.__camera = obj;

    def getCamera(self) -> act.GameObject:
        return self.__camera;

    def updateProjMat(self, winWidth:int, winHeight:int) -> None:
        self.__progMat = glm.perspective(90, winWidth / winHeight, 0.1, 1000);
        gl.glViewport(0, 0, winWidth, winHeight);

    def _createGameObjectWithOpj(self, objFile:par.ObjFile) -> act.GameObject:
        gameObject = act.GameObject();
        for obj in objFile.objects.values():
            mesh = rpi.createMeshWithArray(self.__unilocGeneral, obj.vertices, obj.texCoords, obj.normals);
            material = rpi.Material()
            aRenderUnit = RenderUnitGL(mesh, material, self.__texMan.getTexture(obj.material.diffuseMapName), self.__unilocGeneral);
            gameObject.renderUnits.append(aRenderUnit);

        return gameObject;

    def __renderAllShadows(self, winSize:tuple):
        self.__shaderDepth.activate();

        for dlight in self.__dlights:
            dlight.startRenderShadowMap(self.__unilocDepth);
            for obj in self.__renderObjects:
                _renderObjectDepth(obj, self.__unilocDepth);
            dlight.finishRenderShadowMap();
        for slight in self.__slights:
            slight.startRenderShadowMap(self.__unilocDepth);
            for obj in self.__renderObjects:
                _renderObjectDepth(obj, self.__unilocDepth);
            slight.finishRenderShadowMap();

        gl.glViewport(0, 0, winSize[0], winSize[1])

    def __createLights(self) -> None:
        self.__sunlight.setColorRGB(1, 1, 0.95);
        self.__moonlight.setDirection(3, -1, 0.5)
        self.__moonlight.setColorRGB(0.1, 0.1, 0.2)

        #self.__dlights.append(self.__sunlight);
        #self.__dlights.append(self.__moonlight);

        aplight = lit.PointLight();
        aplight.pos.setXYZ(10, 2, 2);
        aplight.setMaxDist(10);
        #self.__plights.append(aplight);

        spot = lit.SpotLight();
        spot.pos.setXYZ(10, 20, -60)
        spot.setDegreeXYZ(30, 180, 0)
        spot.setMaxDist(800);
        spot.setColorRGB(0.6, 0.6, 0.6);
        self.__slights.append(spot);

        spot2 = lit.SpotLight();
        spot2.pos.setXYZ(-2.87442,      4.45451,     -31.5766)
        spot2.setDegreeXYZ(38.7022,     115.807,            0)
        spot2.setMaxDist(80);
        spot2.setColorRGB(0.4, 0.4, 0.4);
        self.__slights.append(spot2);

    def __createMeshes(self) -> None:
        mesh = rpi.createMeshAabb(self.__unilocGeneral, -500, 500, -10, -1, -500, 500);
        material = rpi.Material()
        material.setTexSize(250, 250)
        box1 = act.GameObject();
        box1.renderUnits.append(RenderUnitGL(mesh, material, self.__texMan.getDefaultTex2(), self.__unilocGeneral));
        #self.__renderObjects.append(box1);

        mesh = rpi.createMeshAabb(self.__unilocGeneral, 0, 3, -1, 2, 0, 3);
        material = rpi.Material()
        aRenderUnit = RenderUnitGL(mesh, material, self.__texMan.getDefaultTex1(), self.__unilocGeneral);
        for x in range(2):
            for y in range(3):
                for z in range(2):
                    box = act.GameObject();
                    box.pos.setPosX(box.pos.getPosX() + 5 * x);
                    box.pos.setPosY(box.pos.getPosY() + 5 * y);
                    box.pos.setPosZ(box.pos.getPosZ() + 5 * z);
                    box.renderUnits.append(aRenderUnit);
                    #self.__renderObjects.append(box);

        seoul = self._createGameObjectWithOpj(par.loadObjFile("data\\models\\seoul_v2.obj"));
        seoul.pos.setPosX(2)
        seoul.pos.setPosZ(20)
        seoul.scale.x = 10
        seoul.scale.y = 10
        seoul.scale.z = 10
        self.__renderObjects.append(seoul)

        dva = self._createGameObjectWithOpj(par.loadObjFile("data\\models\\palanquin.obj"));
        dva.pos.setPosY(0)
        dva.pos.setPosZ(-30)
        dva.angle.setY(180);
        dva.scale.x = 2
        dva.scale.y = 2
        dva.scale.z = 2
        self.__renderObjects.append(dva)
