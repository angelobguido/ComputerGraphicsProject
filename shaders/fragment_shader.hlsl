#version 330

uniform vec4 color;

in vec4 positionColor;
in vec2 TexCoord;
out vec4 fragColor;

uniform sampler2D samplerTexture;

void main(){
    fragColor = texture(samplerTexture, TexCoord) * positionColor;
}