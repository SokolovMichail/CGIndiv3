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
    for (int i = 0; i < 4; i++)
    {
        vec3 lightVector = normalize(lights[i].position - varCoord);
        float diff = 0.2 + max(dot(varNormal, lightVector), 0);
        if (diff < 0.4)
            gl_FragColor += vec4(lights[i].color * 0.3, 1);
        else if (diff < 0.7)
            gl_FragColor += vec4(lights[i].color * 0.6, 1);
        else
            gl_FragColor += vec4(lights[i].color, 1);
    }
    gl_FragColor *= vec4(varColor, 1);
}