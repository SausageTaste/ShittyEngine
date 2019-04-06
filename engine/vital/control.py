from enum import Enum;


class EventType(Enum):
    W = 1
    S = 2
    A = 3
    D = 4

    SPACEBAR = 5
    SHIFTLEFT = 6

    UP = 7
    DOWN = 8
    LEFT = 9
    RIGHT = 10

    WIN_RESIZE = 11


class ControlStates:
    def __init__(self):
        self.w = False;
        self.s = False;
        self.a = False;
        self.d = False;

        self.spacebar = False;
        self.shiftLeft = False;

        self.up = False;
        self.down = False;
        self.left = False;
        self.right = False;

        self.eventQueue:list = [];
