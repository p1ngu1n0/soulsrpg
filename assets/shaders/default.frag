#version 330 core

out vec4 FragColor;

in vec2 TexCoord;
uniform sampler2D ourTexture;

uniform float uTime;

void main() {
	FragColor = sin(uTime) * texture(ourTexture, TexCoord);
}
