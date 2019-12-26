struct light
{
    vec3 position;
    vec3 color;
};

uniform light lights[4];

varying vec3 varCoord;
varying vec3 varNormal;
varying vec3 varColor;

void main()
{
    vec3 viewVector = normalize(-varCoord);
    for (int i = 0; i < 4; i++)
    {
        vec3 lightVector = normalize(lights[i].position - varCoord);
        float k = 0.8;
        float d1 = pow(max(dot(varNormal, lightVector), 0), 1 + k);
        float d2 = pow(1 - dot(varNormal, viewVector), 1 - k);
        gl_FragColor += vec4(lights[i].color * d1 * d2, 1);
    }
    gl_FragColor *= vec4(varColor, 1);
}