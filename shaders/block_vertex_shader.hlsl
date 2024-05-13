#version 430

layout(location = 0) in uint info;
//  0b11100000 00000000 00000000 00000000 -> 0XE0000000 : Face (Up, Down, Front, Back, Right, Left)
//  0b00011100 00000000 00000000 00000000 -> 0X1C000000 : Vertex (Up-Left, Up-Right, Down-Left, Down-Right)
//  0b00000011 11111111 11111111 00000000 -> 0X03FFFF00 : Position in chunk (0,0,0) to (31,31,31)
//  0b00000000 00000000 00000000 11111111 -> 0X000000FF : Texture index in atlas (0 to 255)

/*

Face vertices:

Up:     (0,1,0) (1,1,0) (0,1,1) (1,1,1)
Down:   (0,0,0) (1,0,0) (0,0,1) (1,0,1)
Front:  (0,1,1) (1,1,1) (0,0,1) (1,0,1)
Back:   (0,1,0) (1,1,0) (0,0,0) (1,0,0)
Right:  (1,1,1) (1,1,0) (1,0,1) (1,0,0)
Left:   (0,1,1) (0,1,0) (0,0,1) (0,0,0)


*/

//out vec2 TexCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;        

const vec3[6][4] vertex_cube_position = {
    {vec3(0,1,0), vec3(1,1,0), vec3(0,1,1), vec3(1,1,1)},
    {vec3(0,0,0), vec3(1,0,0), vec3(0,0,1), vec3(1,0,1)},
    {vec3(0,1,1), vec3(1,1,1), vec3(0,0,1), vec3(1,0,1)},
    {vec3(0,1,0), vec3(1,1,0), vec3(0,0,0), vec3(1,0,0)},
    {vec3(1,1,1), vec3(1,1,0), vec3(1,0,1), vec3(1,0,0)},
    {vec3(0,1,1), vec3(0,1,0), vec3(0,0,1), vec3(0,0,0)}
}; 

const uint width = 16*16;
const uint height = 16*16;

const vec2[4] vertex_texture_position = {
    vec2(0,1),
    vec2(16/float(width),1),
    vec2(0,1-16/float(height)),
    vec2(16/float(width),1-16/float(height))
}; 

const vec3[6] normals = {
    vec3(0,1,0),
    vec3(0,-1,0),
    vec3(0,0,1),
    vec3(0,0,-1),
    vec3(1,0,0),
    vec3(-1,0,0)
}; 

out vec2 TexCoord;
out vec3 Normal;
out vec3 FragPos;

void main(){

    uint face             = (info>>29)&0x7;
    uint vertex           = (info>>26)&0x7;
    float position_x      = float((info>>21)&0x1F);
    float position_y      = float((info>>13)&0xFF);
    float position_z      = float((info>>8)&0x1F);
    uint texture_index   = info&0xFF;
    
    position_x += vertex_cube_position[face][vertex].x;
    position_y += vertex_cube_position[face][vertex].y;
    position_z += vertex_cube_position[face][vertex].z;

    vec3 position = vec3(position_x,position_y,position_z);

    TexCoord = vertex_texture_position[vertex] + vec2(int(texture_index%16)*(16.0/float(width)), -int(texture_index/16)*(16.0/float(height)));
    Normal = normals[face];

    gl_Position = projection * view * model * vec4(position,1.0);
    FragPos = vec3(model * vec4(position,1.0));
}