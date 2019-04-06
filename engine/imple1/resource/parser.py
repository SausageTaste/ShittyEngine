from typing import Dict;
import os;


class ObjFile:
    def __init__(self):
        self.objects:Dict[str,ObjectData] = {};

    def check(self):
        for objName in self.objects.keys():
            self.objects[objName].check();


class MaterialData:
    def __init__(self):
        self.name = None
        self.diffuseMapName = None

    def check(self):
        if self.name is None:
            raise Exception();
        if self.diffuseMapName is None:
            raise Exception(self.name);


class ObjectData:
    def __init__(self):
        self.name:str = None;
        self.vertices:list = [];
        self.texCoords:list = [];
        self.normals:list = [];
        self.material:MaterialData = None;

    def check(self):
        if not (len(self.vertices) == len(self.texCoords) == len(self.normals)):
            raise Exception("Number of vertex datas is different. {} : {} : {}".format(
                len(self.vertices), len(self.texCoords), len(self.normals)
            ));
        if len(self.normals) == 0:
            raise Exception();

        if self.material is None:
            raise Exception();
        if self.name is None:
            raise Exception();


def _parseMtlFile(objPath:str, mtlName:str, container:Dict[str,MaterialData]):
    mtlPath = os.path.split(objPath)[0] + "\\" + mtlName;

    with open(mtlPath, "r") as file:
        curMatName = None

        for line in file:
            lineElements = line.strip('\n').split();
            if len(lineElements) < 1:
                continue;

            if lineElements[0] == "newmtl":
                curMatName = lineElements[1]
                if curMatName in container.keys():
                    raise Exception("Material duplaicated in {}: {}".format(mtlPath, curMatName));
                container[curMatName] = MaterialData()
                container[curMatName].name = curMatName
            elif lineElements[0] == "map_Kd":
                container[curMatName].diffuseMapName = lineElements[1]

    for mat in container.values():
        mat.check();


def loadObjFile(path:str):
    objFile = ObjFile();

    currentObjName = "";
    materials:Dict[str,MaterialData] = {}

    gVertices:list = [];
    gTexCoords:list = [];
    gNormals:list = [];

    with open(path, "r") as file:
        for line in file:
            line = line.strip("\n");
            lineElements = line.split(" ");
            if lineElements[0] == "v":
                _, x, y, z = lineElements
                gVertices.append((float(x), float(y), float(z)));
            elif lineElements[0] == "vt":
                _, x, y = lineElements
                gTexCoords.append((float(x), float(y)));
            elif lineElements[0] == "vn":
                _, x, y, z = lineElements
                gNormals.append((float(x), float(y), float(z)));
            elif lineElements[0] == "o":
                currentObjName = lineElements[1];
                if currentObjName not in objFile.objects.keys():
                    objFile.objects[currentObjName] = ObjectData();
                    objFile.objects[currentObjName].name = currentObjName;
            elif lineElements[0] == "usemtl":
                objFile.objects[currentObjName].material = materials[lineElements[1]];
            elif lineElements[0] == "mtllib":
                _parseMtlFile(path, lineElements[1], materials);
            elif lineElements[0] == "f":
                vertIndices = (
                    tuple(map(lambda xx: int(xx), lineElements[1].split("/"))),
                    tuple(map(lambda xx: int(xx), lineElements[2].split("/"))),
                    tuple(map(lambda xx: int(xx), lineElements[3].split("/")))
                )

                currentObj = objFile.objects[currentObjName]
                for vertIndex in vertIndices:
                    try:
                        currentObj.vertices.append(gVertices[vertIndex[0]-1]);
                        currentObj.texCoords.append(gTexCoords[vertIndex[1]-1]);
                        currentObj.normals.append(gNormals[vertIndex[2]-1]);
                    except IndexError:
                        print("{} vert: {}, {}, vn".format(currentObjName, vertIndex[0]-1, len(gVertices)))
                        print("{} texC: {}, {}, vn".format(currentObjName, vertIndex[1]-1, len(gTexCoords)))
                        print("{} norm: {}, {}, vn".format(currentObjName, vertIndex[2]-1, len(gNormals)))
                        raise;
            elif lineElements[0] == "#":
                pass;
            elif lineElements[0] == "s":
                pass;
            else:
                raise Exception(line);

    objFile.check();
    return objFile;
