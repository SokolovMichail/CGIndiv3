struct light
{
    vec3 position;
    vec3 color;
};

uniform light lights[2];

varying vec3 varCoord;
varying vec3 varNormal;
varying vec3 varColor;

void main()
{
    for (int i = 0; i < 2; i++)
    {
        vec3 lightVector = normalize(lights[i].position - varCoord);
        gl_FragColor += vec4(max(dot(varNormal, lightVector), 0) * lights[i].color, 1);
    }
    gl_FragColor *= vec4(varColor, 1);
}