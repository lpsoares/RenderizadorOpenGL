float sdfCircle(vec2 uv, float r, vec2 c) {
    float d = length(uv - c) - r;
    return d;
}

float sdStar5(in vec2 p, in float r, in float rf)
{
    const vec2 k1 = vec2(0.809016994375, -0.587785252292);
    const vec2 k2 = vec2(-k1.x,k1.y);
    p.x = abs(p.x);
    p -= 2.0*max(dot(k1,p),0.0)*k1;
    p -= 2.0*max(dot(k2,p),0.0)*k2;
    p.x = abs(p.x);
    p.y -= r;
    vec2 ba = rf*vec2(-k1.y,k1.x) - vec2(0,1);
    float h = clamp( dot(p,ba)/dot(ba,ba), 0.0, r );
    return length(p-ba*h) * sign(p.y*ba.x-p.x*ba.y);
}

vec3 drawScene(vec2 uv) {
  
  vec3 col = vec3(1);
  
  float res = 0.0;
  
  res = sdfCircle(uv, 0.46, vec2(0.0, 0.0));
  col = mix(vec3(1, 1, 0), col, step(0., res));
  
  res = sdfCircle(uv, 0.34, vec2(0.0, 0.0));
  col = mix(vec3(1, 1, 1), col, step(0., res));
  
  vec2 pos;
  float t = iTime;
  
  t = 2.0*3.1415*smoothstep(0.0, 5.0, mod(t, 5.0));
  
  pos.x = 0.4*sin(t);
  pos.y = 0.4*cos(t);
  res = sdStar5(uv-pos, 0.05, .4);

  col = mix(vec3(1, 0, 0), col, step(0., res));
  
  return col;
}

void mainImage( out vec4 fragColor, in vec2 fragCoord ) {
  vec2 uv = fragCoord/iResolution.xy;
  uv -= 0.5;
  uv.x *= iResolution.x/iResolution.y;
    
  vec3 col = drawScene(uv);
  fragColor = vec4(col,1.0);
}
