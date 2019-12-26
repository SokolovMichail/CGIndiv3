struct light
{
    vec3 position;
    vec3 color;
    vec3 coolColor;
    vec3 warmColor;
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
        vec3 reflectVector = normalize(reflect(-lightVector, varNormal));
        vec3 kCool = min(lights[i].coolColor + lights[i].coolColor * varColor, 1);
        vec3 kWarm = min(lights[i].warmColor + lights[i].warmColor * varColor, 1);
        vec3 kFinal = mix(kCool, kWarm, dot(varNormal, lightVector));
        float spec = pow(max(dot(reflectVector, viewVector), 0), 32);
        gl_FragColor += vec4(min(kFinal + spec, 1), 1);
    }
}