struct light
{
    vec3 position;
    vec3 color;
    vec3 specularColor;
    float specularIntensity;
    float rimIntensity;
};

uniform light lights[4];

varying vec3 varCoord;
varying vec3 varNormal;
varying vec3 varColor;

void main()
{
    float bias = 0;
    vec3 viewVector = normalize(-varCoord);
    for (int i = 0; i < 4; i++)
    {
        vec3 lightVector = normalize(lights[i].position - varCoord);
        vec3 reflectVector = reflect(-lightVector, varNormal);
        vec4 diff = vec4(lights[i].color, 1) * max(dot(varNormal, lightVector), 0);
        vec4 spec = vec4(lights[i].specularColor, 1) * pow(max(dot(varNormal, reflectVector), 0),
            lights[i].specularIntensity);
        float rim = pow(1 + bias - max(dot(varNormal, viewVector), 0), lights[i].rimIntensity);
        gl_FragColor += diff + rim * vec4(0.5, 0.0, 0.2, 1.0) + spec * vec4(lights[i].specularColor, 1);
    }
    gl_FragColor *= vec4(varColor, 1);
}