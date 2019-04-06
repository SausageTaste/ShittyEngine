#version 140


uniform vec4 uColor;

uniform int uHasMaskMap;
uniform sampler2D uMaskMap;

in vec2 vTexCoord;

out vec4 color;


void main() {
    float mask_f;
    if (uHasMaskMap > 0)
        mask_f = texture(uMaskMap, vTexCoord).r;
    else
        mask_f = 1.0;

    color = vec4( 1.0, 1.0, 1.0, mask_f ) * uColor;
}
