import sys;

import pygame as p;
import pygame.locals as pl;

import engine.core.interface as inter;
import engine.vital.control as con;


class PygameInterface(inter.OsInterface):
    def __init__(self, winWidth, winHeight):
        assert isinstance(winWidth, int);
        assert isinstance(winHeight, int);

        p.init()

        self.__mDSurf:p.Surface = p.display.set_mode(
            (winWidth, winHeight),
            pl.DOUBLEBUF | pl.OPENGL | pl.RESIZABLE
        );

        self.__mWinWidth:int = winWidth;
        self.__mWinHeight:int = winHeight;

    def showWindow(self):
        raise NotImplemented;

    def hideWindow(self):
        raise NotImplemented;

    def terminate(self) -> None:
        p.quit();

    def clearFrame(self):
        pass

    def blit(self):
        p.display.flip();

    def getWinSize(self):
        return self.__mWinWidth, self.__mWinHeight;

    def updateControl(self, controlData:con.ControlStates):
        for event in p.event.get():
            if event.type == pl.QUIT:
                self.terminate()
                sys.exit();

            elif event.type == pl.VIDEORESIZE:
                self.__mWinWidth = event.dict['w']
                self.__mWinHeight = event.dict['h']
                controlData.eventQueue.append(con.EventType.WIN_RESIZE);

            elif event.type == pl.KEYDOWN:
                if event.key == pl.K_w:
                    controlData.w = True;
                elif event.key == pl.K_s:
                    controlData.s = True;
                elif event.key == pl.K_a:
                    controlData.a = True;
                elif event.key == pl.K_d:
                    controlData.d = True;

                elif event.key == pl.K_SPACE:
                    controlData.spacebar = True;
                elif event.key == pl.K_LSHIFT:
                    controlData.shiftLeft = True;

                elif event.key == pl.K_UP:
                    controlData.up = True;
                elif event.key == pl.K_DOWN:
                    controlData.down = True;
                elif event.key == pl.K_LEFT:
                    controlData.left = True;
                elif event.key == pl.K_RIGHT:
                    controlData.right = True;

            elif event.type == pl.KEYUP:
                if event.key == pl.K_w:
                    controlData.w = False;
                elif event.key == pl.K_s:
                    controlData.s = False;
                elif event.key == pl.K_a:
                    controlData.a = False;
                elif event.key == pl.K_d:
                    controlData.d = False;

                elif event.key == pl.K_SPACE:
                    controlData.spacebar = False;
                elif event.key == pl.K_LSHIFT:
                    controlData.shiftLeft = False;

                elif event.key == pl.K_UP:
                    controlData.up = False;
                elif event.key == pl.K_DOWN:
                    controlData.down = False;
                elif event.key == pl.K_LEFT:
                    controlData.left = False;
                elif event.key == pl.K_RIGHT:
                    controlData.right = False;
