#version 140


// From Master
uniform vec3 uViewPos;//
uniform vec3 uBaseAmbient;//
uniform int uDlightCount;
uniform int uPlightCount;
uniform int uSlightCount;

// From Lights
// Directional
uniform vec3 uDlightDirs[3];
uniform vec3 uDlightColors[3];
uniform sampler2D uDlightDepthMap[3];
// Point
uniform vec3 uPlightPoses[3];
uniform vec3 uPlightColors[3];
uniform float uPlightMaxDists[3];
// Spot
uniform vec3 uSlightColors[3];
uniform vec3 uSlightPoses[3];
uniform vec3 uSlightDirVec[3];
uniform float uSlightMaxDists[3];
uniform float uSlightCutoff[3];
uniform sampler2D uSlightDepthMap[3];

// From Material
uniform float uShininess;//
uniform float uSpecularStrength;//

// From Texture
uniform sampler2D uDiffuseMap;


in vec3 vFragPos;
in vec2 vTexCoordOut;
in vec3 vNormalVec;
in vec4 vFragPosInDlight[3];
in vec4 vFragPosInSlight[3];

out vec4 color;


vec3 procDlight(int index, vec3 viewDir)
{
	vec3 lightLocDir = normalize(-uDlightDirs[index]);
	vec3 lightColor = uDlightColors[index];

	float diff = max(dot(vNormalVec, lightLocDir), 0.0);
	vec3 diffuse = max(diff * lightColor, vec3(0.0));

	// Calculate specular lighting.
	if (uShininess <= 0.0)
	{
		return diffuse;
	}
	else
	{
		vec3 reflectDir = reflect(-lightLocDir, vNormalVec);
		float spec = pow(max(dot(viewDir, reflectDir), 0.0), uShininess);
		vec3 specular = max(uSpecularStrength * spec * lightColor, vec3(0.0));

		return diffuse + specular;
	}
}


float calcShadowDlight(int index)
{
    vec4 fragPosInLightSpace = vFragPosInDlight[index];
    vec3 projCoords = fragPosInLightSpace.xyz / fragPosInLightSpace.w;
    if (projCoords.z > 1.0) return 0.0;
    projCoords = projCoords * 0.5 + 0.5;
    float closestDepth = texture(uDlightDepthMap[index], projCoords.xy).r;
    float currentDepth = projCoords.z;

    //float bias = max(0.05 * (1.0 - dot(vNormalVec, -uDlightDirs[index])), 0.005);
    float bias = 0.002;
    //float bias = 0.0;
    float shadow = currentDepth - bias > closestDepth  ? 1.0 : 0.0;

    return shadow;
}


vec3 procPlight(int index, vec3 viewDir, vec3 fragNormal)
{
    float distance_f = length(uPlightPoses[index] - vFragPos);
    vec3 lightDir = normalize(uPlightPoses[index] - vFragPos);
    float distanceDecreaser = -1 / (uPlightMaxDists[index]*uPlightMaxDists[index]) * (distance_f*distance_f) + 1;

    vec3 diffuse;
    if (distance_f > uPlightMaxDists[index])
    {
        diffuse = vec3(0.0);
    }
    else
    {
        float diff_f = max(dot(fragNormal, lightDir), 0.0);
        diffuse = max(diff_f * uPlightColors[index], vec3(0.0));
    }

    // Calculate specular lighting.
    if (uShininess == 0.0)
    {
        return diffuse * distanceDecreaser;
    }
    else
    {
        vec3 reflectDir = reflect(-lightDir, fragNormal);

        //vec3 halfwayDir = normalize(lightDir + viewDir); // Blinn
        //float spec = pow(max(dot(fragNormal, halfwayDir), 0.0), 64.0); // Blinn
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), uShininess); // Phong

        vec3 specular = max(uSpecularStrength * spec * uPlightColors[index], vec3(0.0));

        return diffuse * distanceDecreaser + specular * distanceDecreaser;
    }
}


vec3 procSlightLikePlight(int index, vec3 viewDir, vec3 fragNormal)
{
    float distance_f = length(uSlightPoses[index] - vFragPos);
    vec3 lightDir = normalize(uSlightPoses[index] - vFragPos);
    float distanceDecreaser = -1 / (uSlightMaxDists[index]*uSlightMaxDists[index]) * (distance_f*distance_f) + 1;

    vec3 diffuse;
    if (distance_f > uSlightMaxDists[index])
    {
        diffuse = vec3(0.0);
    }
    else
    {
        float diff_f = max(dot(fragNormal, lightDir), 0.0);
        diffuse = max(diff_f * uSlightColors[index], vec3(0.0));
    }

    // Calculate specular lighting.
    if (uShininess == 0.0)
    {
        return diffuse * distanceDecreaser;
    }
    else
    {
        vec3 reflectDir = reflect(-lightDir, fragNormal);

        //vec3 halfwayDir = normalize(lightDir + viewDir); // Blinn
        //float spec = pow(max(dot(fragNormal, halfwayDir), 0.0), 64.0); // Blinn
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), uShininess); // Phong

        vec3 specular = max(uSpecularStrength * spec * uSlightColors[index], vec3(0.0));

        return diffuse * distanceDecreaser + specular;
    }
}


vec3 procSlight(int index, vec3 viewDir, vec3 fragNormal)
{
    float distance_f = length(uSlightPoses[index] - vFragPos);
    vec3 lightDir = normalize(uSlightPoses[index] - vFragPos);
    float theta = dot(lightDir, normalize(-uSlightDirVec[index]));

    if (theta > uSlightCutoff[index])
        return procSlightLikePlight(index, viewDir, fragNormal) * 10*(theta - uSlightCutoff[index]);
    else
        return vec3(0.0);
}


float calcShadowSlight(int index)
{
    vec4 fragPosInLightSpace = vFragPosInSlight[index];
    vec3 projCoords = fragPosInLightSpace.xyz / fragPosInLightSpace.w;
    if (projCoords.z > 1.0) return 0.0;
    projCoords = projCoords * 0.5 + 0.5;
    float closestDepth = texture(uSlightDepthMap[index], projCoords.xy).r;
    float currentDepth = projCoords.z;

    float bias = 0.00005;
    float shadow = currentDepth - bias > closestDepth  ? 1.0 : 0.0;

    return shadow;
}


void main(void)
{
    vec3 viewDir = normalize(uViewPos - vFragPos);
    float fragDistance = abs(length(vFragPos - uViewPos));
    vec3 fragNormal = vNormalVec;

    vec3 accumLight = uBaseAmbient;

    int i;
    for (i = 0; i < uDlightCount; i++)
    {
        accumLight += max(procDlight(i, viewDir) * (1-calcShadowDlight(i)), vec3(0.0));
    }
    for (i = 0; i < uPlightCount; i++)
    {
        accumLight += max(procPlight(i, viewDir, fragNormal), vec3(0.0));
    }
    for (i = 0; i < uSlightCount; i++)
    {
        accumLight += max(procSlight(i, viewDir, fragNormal) * (1-calcShadowSlight(i)), vec3(0.0));
    }

    color = texture(uDiffuseMap, vTexCoordOut) * vec4(accumLight, 1.0);
}
