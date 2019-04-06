#version 140

// From Master
uniform mat4 uProjViewMat;
uniform int uDlightCount;
uniform int uSlightCount;

// From Light
uniform mat4 uDlightProjViewMat[3];
uniform mat4 uSlightProjViewMat[3];

// From GameObject
uniform mat4 uModelMatrix;//

// From Mesh
in vec3 iPosition;//
in vec2 iTexCoord;//
in vec3 iNormal;//

// From Material
uniform float uTextureVerNum;//
uniform float uTextureHorNum;//


out vec3 vFragPos;
out vec2 vTexCoordOut;
out vec3 vNormalVec;
out vec4 vFragPosInDlight[3];
out vec4 vFragPosInSlight[3];

void main(void)
{
    gl_Position = uProjViewMat * uModelMatrix * vec4(iPosition, 1.0);
    vFragPos = vec3(uModelMatrix * vec4(iPosition, 1.0));
    vTexCoordOut = vec2(iTexCoord.x * uTextureHorNum, iTexCoord.y * uTextureVerNum);
    vNormalVec = normalize(vec3(uModelMatrix * vec4(iNormal, 0.0)));

    for (int i = 0; i < uDlightCount; i++)
    {
        vFragPosInDlight[i] = uDlightProjViewMat[i] * vec4(vFragPos, 1.0);
    }
    for (int i = 0; i < uSlightCount; i++)
    {
        vFragPosInSlight[i] = uSlightProjViewMat[i] * vec4(vFragPos, 1.0);
    }
}
