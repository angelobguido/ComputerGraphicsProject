#version 330

uniform vec4 color;

in vec2 TexCoord;
out vec4 fragColor;

uniform sampler2D samplerTexture;

void main(){
    fragColor = texture(samplerTexture, TexCoord);
    if( fragColor.a < 0.5 ){ discard; }
}