#version 430

in vec2 TexCoord;
in vec3 Normal;
in vec3 FragPos;
out vec4 FragColor;

uniform sampler2D samplerTexture;
uniform vec3 lightPos;
uniform vec3 lightColor;
uniform float ambientStrength;

void main(){
    FragColor = texture(samplerTexture, TexCoord);
    if( FragColor.a < 0.5 ){ discard; }

    vec3 ambient = ambientStrength * lightColor;

    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(Normal, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;
    
    FragColor = vec4(ambient + diffuse, 1) * FragColor;

}