import os
from importlib.util import find_spec;


def ensureModuleReady(moduleName, libName):
    spam_spec = find_spec(moduleName)
    if spam_spec is None:
        os.system("pip install " + libName);


def main():
    os.system("python -m pip install --upgrade pip");

    coreLibs: tuple = (
        ("numpy", "numpy"),
        ("glm", "pyglm"),
        ("PIL", "pillow"),
    );
    imple1Libs: tuple = (
        ("OpenGL", "pyopengl"),
        ("pygame", "pygame"),
    );

    for moduleName, libName in (coreLibs + imple1Libs):
        ensureModuleReady(moduleName, libName);

    input("All done successfully!");


if __name__ == '__main__':
    main();
