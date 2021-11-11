#version 330 core

layout(location = 0) in vec3 aPos;
layout(location = 1) in vec2 aTexCoord;

out vec2 TexCoord;

uniform mat4 uProj;
uniform mat4 uView;

void main() {
	gl_Position = uProj * uView * vec4(aPos, 1.0);
	TexCoord = aTexCoord;
}
