#version 140 core


uniform float uLeft;
uniform float uRight;
uniform float uTop;
uniform float uBottom;

out vec2 vTexCoord;


vec2 getPosition(int vertexIndex_i) {
    switch (vertexIndex_i)
    {
    case 0:
        return vec2( uLeft, uTop );
    case 1:
        return vec2( uLeft, uBottom );
    case 2:
        return vec2( uRight, uBottom );
    case 3:
        return vec2( uLeft, uTop );
    case 4:
        return vec2( uRight, uBottom );
    case 5:
        return vec2( uRight, uTop );
    default:
        return vec2(0.0);
    }

    return vec2(0.0);
}


vec2 getTexCoord(int vertexIndex_i) {
    switch (vertexIndex_i)
    {
    case 0:
        return vec2( 0.0, 1.0 );
    case 1:
        return vec2( 0.0, 0.0 );
    case 2:
        return vec2( 1.0, 0.0 );
    case 3:
        return vec2( 0.0, 1.0 );
    case 4:
        return vec2( 1.0, 0.0 );
    case 5:
        return vec2( 1.0, 1.0 );
    default:
        return vec2(0.0);
    }

    return vec2(0.0);
}


void main(void) {
    gl_Position = vec4( getPosition(gl_VertexID), 0.0, 1.0 );
    vTexCoord = getTexCoord(gl_VertexID);
}
