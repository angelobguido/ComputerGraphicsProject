#version 330

uniform vec4 color;

in vec4 positionColor;
out vec4 fragColor;

void main(){
    fragColor = positionColor;
}