#version 330

layout(location = 0) in uint;
//  0b11100000 00000000 00000000 00000000 -> 0XE0000000 : Face (Up, Down, Front, Back, Right, Left)
//  0b00011100 00000000 00000000 00000000 -> 0X1C000000 : Vertex (Up-Left, Up-Right, Down-Left, Down-Right)
//  0b00000011 11111111 11111111 00000000 -> 0X03FFFF00 : Position in chunk (0,0,0) to (31,31,31)
//  0b00000000 00000000 00000000 11111111 -> 0X000000FF : Texture index in atlas (0 to 255)

out vec2 TexCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;        

void main(){
    gl_Position = projection * view * model * vec4(position,1.0);
    TexCoord = texCoord;
}