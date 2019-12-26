varying vec3 varCoord;
varying vec3 varNormal;
varying vec3 varColor;

void main()
{
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    varCoord = gl_ModelViewMatrix * gl_Vertex;
    varNormal = normalize(gl_NormalMatrix * gl_Normal);
    varColor = gl_Color;
}