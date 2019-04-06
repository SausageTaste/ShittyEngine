import glm;

from engine.imple1.interface import PygameInterface;
import engine.imple1.rendermaster as rma;
import engine.vital.control as con;
import engine.vital.utils as uti;
import engine.vital.rotator as rot;
import engine.imple1.resource.parser as par;
import engine.imple1.renderer.factory as fac;
import engine.imple1.renderer.overlay as ove;


class MainLoop:
    def __init__(self):
        self.frameMan = uti.FrameCounter();
        self.interface = PygameInterface(800, 450);
        width, height = self.interface.getWinSize();
        self.texMan = fac.TextureManager()
        self.renderMaster = rma.RenderMasterGL(width, height, self.texMan);
        self.overlayMaster = ove.OverlayMaster(self.texMan, width, height);
        self.camera = self.renderMaster.getCamera();
        self.controlStruct = con.ControlStates();

    def update(self):
        self.frameMan.update();

        self.interface.updateControl(self.controlStruct);
        self.controlObj();

        self.interface.clearFrame();
        self.renderMaster.update(self.frameMan.getDeltaTime(), self.interface.getWinSize());
        self.overlayMaster.render()
        self.interface.blit();

    def controlObj(self):
        deltaTime:float = self.frameMan.getDeltaTime();
        ang:rot.AngleEulerDegree = self.camera.angle;

        xLook: int = 0;
        yLook: int = 0;
        if self.controlStruct.up:
            yLook += 1;
        if self.controlStruct.down:
            yLook -= 1;
        if self.controlStruct.left:
            xLook -= 1;
        if self.controlStruct.right:
            xLook += 1;

        if xLook:
            ang.addXYZ(0, -xLook * deltaTime * 100, 0);
        if yLook:
            ang.addXYZ(yLook * deltaTime * 100, 0, 0);

            if ang.getX() > 90:
                ang.setX(90);
            elif ang.getX() < -90:
                ang.setX(-90);

        moveVec = glm.vec3();
        if self.controlStruct.w:
            moveVec.z -= 1;
        if self.controlStruct.s:
            moveVec.z += 1;
        if self.controlStruct.a:
            moveVec.x -= 1;
        if self.controlStruct.d:
            moveVec.x += 1;
        if self.controlStruct.spacebar:
            moveVec.y += 1;
        if self.controlStruct.shiftLeft:
            moveVec.y -= 1;

        if glm.length(moveVec) != 0:
            moveVec = glm.normalize(moveVec);
            rotMat = glm.rotate(glm.mat4(1), glm.radians(ang.getY()), (0, 1, 0));
            moveVec = glm.vec3(rotMat * glm.vec4(moveVec, 0));
            self.camera.pos.addVec(moveVec * deltaTime * 10);

        for x in self.controlStruct.eventQueue:
            if x == con.EventType.WIN_RESIZE:
                self.renderMaster.updateProjMat(*self.interface.getWinSize());


def main():
    mainLoop = MainLoop()
    while True:
        mainLoop.update();


def test():
    file = par.loadObjFile("data\\models\\seoul_v2.obj");


if __name__ == '__main__':
    main();
