vec2 rotate(vec2 uv, float th) {
  return mat2(cos(th), sin(th), -sin(th), cos(th)) * uv;
}

vec3 sdfCircle(vec2 uv, float r, vec2 c) {
    float d = length(uv - c) - r;
    return d > 0. ? vec3(1.) : vec3(0., 0., 1.);
}

vec3 sdfSquare(vec2 uv, float size, vec2 c) {
  float x = uv.x - c.x;
  float y = uv.y - c.y;
  vec2 rotated = rotate(vec2(x,y), iTime);
  float d = max(abs(rotated.x), abs(rotated.y)) - size;
  return d > 0. ? vec3(1.) : vec3(1., 0., 0.);
}


void mainImage( out vec4 fragColor, in vec2 fragCoord ) {
    vec2 uv = fragCoord/iResolution.xy;
    uv -= 0.5;
    uv.x *= iResolution.x/iResolution.y;
    //vec3 col = sdfCircle(uv, .2, vec2(-0.3, 0.2));
    vec3 col = sdfSquare(uv, 0.2, vec2(0.0, 0.0));
    fragColor = vec4(col,1.0);
}
