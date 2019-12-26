struct light
{
    vec3 position;
    vec3 color;
    vec3 specularColor;
    float specularIntensity;
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
        vec3 h = normalize(lightVector + viewVector);
        float n = 16;
        gl_FragColor += vec4(lights[i].specularColor * lights[i].specularIntensity * pow(dot(varNormal, h), n), 1);
    }
    gl_FragColor *= vec4(varColor, 1);
}